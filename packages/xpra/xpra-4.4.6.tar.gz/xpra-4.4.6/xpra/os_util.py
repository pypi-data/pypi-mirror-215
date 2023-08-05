#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This file is part of Xpra.
# Copyright (C) 2013-2022 Antoine Martin <antoine@xpra.org>
# Xpra is released under the terms of the GNU GPL v2, or, at your option, any
# later version. See the file COPYING for details.

import re
import os
import sys
import stat
import uuid
import signal
import socket
import struct
import binascii
import threading
from time import monotonic, sleep
from subprocess import PIPE, Popen

# only mininal imports go at the top
# so that this file can be included everywhere
# without too many side-effects
# pylint: disable=import-outside-toplevel

SIGNAMES = {}
for signame in (sig for sig in dir(signal) if sig.startswith("SIG") and not sig.startswith("SIG_")):
    SIGNAMES[getattr(signal, signame)] = signame


WIN32 = sys.platform.startswith("win")
OSX = sys.platform.startswith("darwin")
LINUX = sys.platform.startswith("linux")
NETBSD = sys.platform.startswith("netbsd")
OPENBSD = sys.platform.startswith("openbsd")
FREEBSD  = sys.platform.startswith("freebsd")

POSIX = os.name=="posix"

BITS = struct.calcsize(b"P")*8


main_thread = threading.current_thread()
def is_main_thread():
    return threading.current_thread()==main_thread


def get_frame_info(ignore_threads=()):
    info = {
        "count"        : threading.active_count() - len(ignore_threads),
        }
    try:
        import traceback
        def nn(x):
            if x is None:
                return ""
            return str(x)
        thread_ident = {}
        for t in threading.enumerate():
            if t not in ignore_threads:
                thread_ident[t.ident] = t.getName()
            else:
                thread_ident[t.ident] = None
        thread_ident.update({
                threading.current_thread().ident    : "info",
                main_thread.ident                   : "main",
                })
        frames = sys._current_frames()  #pylint: disable=protected-access
        stack = None
        for i,frame_pair in enumerate(frames.items()):
            stack = traceback.extract_stack(frame_pair[1])
            tident = thread_ident.get(frame_pair[0], "unknown")
            if tident is None:
                continue
            #sanitize stack to prevent None values (which cause encoding errors with the bencoder)
            sanestack = []
            for e in stack:
                sanestack.append(tuple(nn(x) for x in e))
            info[i] = {
                ""          : tident,
                "stack"     : sanestack,
                }
        del frames, stack
    except Exception as e:
        get_util_logger().error("failed to get frame info: %s", e)
    return info

def get_info_env():
    filtered_env = os.environ.copy()
    if filtered_env.get('XPRA_PASSWORD'):
        filtered_env['XPRA_PASSWORD'] = "*****"
    if filtered_env.get('XPRA_ENCRYPTION_KEY'):
        filtered_env['XPRA_ENCRYPTION_KEY'] = "*****"
    return filtered_env

def get_sysconfig_info():
    import sysconfig
    sysinfo = {}
    log = get_util_logger()
    for attr in (
        "platform",
        "python-version",
        "config-vars",
        "paths",
        ):
        fn = "get_"+attr.replace("-", "_")
        getter = getattr(sysconfig, fn, None)
        if getter:
            try:
                sysinfo[attr] = getter()  #pylint: disable=not-callable
            except ModuleNotFoundError:
                log("sysconfig.%s", fn, exc_info=True)
                if attr=="config-vars" and WIN32:
                    continue
                log.warn("Warning: failed to collect %s sysconfig information", attr)
            except Exception:
                log.error("Error calling sysconfig.%s", fn, exc_info=True)
    return sysinfo

def strtobytes(x) -> bytes:
    if isinstance(x, bytes):
        return x
    return str(x).encode("latin1")
def bytestostr(x) -> str:
    if isinstance(x, (bytes, bytearray)):
        return x.decode("latin1")
    return str(x)
def hexstr(v) -> str:
    return bytestostr(binascii.hexlify(memoryview_to_bytes(v)))


util_logger = None
def get_util_logger():
    global util_logger
    if not util_logger:
        from xpra.log import Logger
        util_logger = Logger("util")
    return util_logger

def memoryview_to_bytes(v) -> bytes:
    if isinstance(v, bytes):
        return v
    if isinstance(v, memoryview):
        return v.tobytes()
    if isinstance(v, bytearray):
        return bytes(v)
    return strtobytes(v)


def set_proc_title(title):
    try:
        import setproctitle  #pylint: disable=import-outside-toplevel
        setproctitle.setproctitle(title)  #@UndefinedVariable pylint: disable=c-extension-no-member
    except ImportError as e:
        get_util_logger().debug("setproctitle is not installed: %s", e)


def getuid() -> int:
    if POSIX:
        return os.getuid()
    return 0

def getgid() -> int:
    if POSIX:
        return os.getgid()
    return 0

def get_shell_for_uid(uid) -> str:
    if POSIX:
        from pwd import getpwuid
        try:
            return getpwuid(uid).pw_shell
        except KeyError:
            pass
    return ""

def get_username_for_uid(uid) -> str:
    if POSIX:
        from pwd import getpwuid
        try:
            return getpwuid(uid).pw_name
        except KeyError:
            pass
    return ""

def get_home_for_uid(uid) -> str:
    if POSIX:
        from pwd import getpwuid
        try:
            return getpwuid(uid).pw_dir
        except KeyError:
            pass
    return ""

def get_groups(username):
    if POSIX:
        import grp      #@UnresolvedImport
        return [gr.gr_name for gr in grp.getgrall() if username in gr.gr_mem]
    return []

def get_group_id(group) -> int:
    try:
        import grp      #@UnresolvedImport
        gr = grp.getgrnam(group)
        return gr.gr_gid
    except (ImportError, KeyError):
        return -1


def platform_release(release):
    if OSX:
        SYSTEMVERSION_PLIST = "/System/Library/CoreServices/SystemVersion.plist"
        try:
            import plistlib
            with open(SYSTEMVERSION_PLIST, "rb") as f:
                pl = plistlib.load(f)           #@UndefinedVariable
            return pl['ProductUserVisibleVersion']
        except Exception as e:
            get_util_logger().debug("platform_release(%s)", release, exc_info=True)
            get_util_logger().warn("Warning: failed to get release information")
            get_util_logger().warn(f" from {SYSTEMVERSION_PLIST}:")
            get_util_logger().warn(f" {e}")
    return release


def platform_name(sys_platform=sys.platform, release=None) -> str:
    if not sys_platform:
        return "unknown"
    PLATFORMS = {"win32"    : "Microsoft Windows",
                 "cygwin"   : "Windows/Cygwin",
                 "linux.*"  : "Linux",
                 "darwin"   : "Mac OS X",
                 "freebsd.*": "FreeBSD",
                 "os2"      : "OS/2",
                 }
    def rel(v):
        values = [v]
        if isinstance(release, (tuple, list)):
            values += list(release)
        else:
            values.append(release)
        return " ".join(str(x) for x in values if x and x!="unknown")
    for k,v in PLATFORMS.items():
        regexp = re.compile(k)
        if regexp.match(sys_platform):
            return rel(v)
    return rel(sys_platform)


def get_rand_chars(l=16, chars=b"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") -> bytes:
    import random
    return b"".join(chars[random.randint(0, len(chars)-1):][:1] for _ in range(l))

def get_hex_uuid() -> str:
    return uuid.uuid4().hex

def get_int_uuid() -> int:
    return uuid.uuid4().int

def get_machine_id() -> str:
    """
        Try to get uuid string which uniquely identifies this machine.
        Warning: only works on posix!
        (which is ok since we only used it on posix at present)
    """
    v = ""
    if POSIX:
        for filename in ("/etc/machine-id", "/var/lib/dbus/machine-id"):
            v = load_binary_file(filename)
            if v is not None:
                break
    elif WIN32:
        v = uuid.getnode()
    return bytestostr(v).strip("\n\r")

def get_user_uuid() -> str:
    """
        Try to generate a uuid string which is unique to this user.
        (relies on get_machine_id to uniquely identify a machine)
    """
    user_uuid = os.environ.get("XPRA_USER_UUID")
    if user_uuid:
        return user_uuid
    import hashlib
    u = hashlib.sha256()
    def uupdate(ustr):
        u.update(ustr.encode("utf-8"))
    uupdate(get_machine_id())
    if POSIX:
        uupdate("/")
        uupdate(str(os.getuid()))
        uupdate("/")
        uupdate(str(os.getgid()))
    uupdate(os.path.expanduser("~/"))
    return u.hexdigest()


def is_X11() -> bool:
    if OSX or WIN32:
        return False
    try:
        from xpra.x11.gtk3.gdk_bindings import is_X11_Display   #@UnresolvedImport
        return is_X11_Display()
    except ImportError:
        get_util_logger().debug("failed to load x11 bindings", exc_info=True)
        return True

def restore_script_env(env):
    # On OSX PythonExecWrapper sets various env vars to point into the bundle
    # and records the original variable contents. Here we revert them back
    # to their original state in case any of those changes cause problems
    # when running a command.
    if "_PYTHON_WRAPPER_VARS" in env:
        for v in env["_PYTHON_WRAPPER_VARS"].split():
            origv = "_" + v
            if env.get(origv):
                env[v] = env[origv]
            elif v in env:
                del env[v]
            del env[origv]
        del env["_PYTHON_WRAPPER_VARS"]
    return env


_saved_env = os.environ.copy()
def get_saved_env():
    return _saved_env.copy()

def get_saved_env_var(var, default=None):
    return _saved_env.get(var, default)

def is_Wayland() -> bool:
    return _is_Wayland(_saved_env)

def _is_Wayland(env : dict) -> bool:
    backend = env.get("GDK_BACKEND", "")
    if backend=="wayland":
        return True
    return backend!="x11" and (
        bool(env.get("WAYLAND_DISPLAY")) or env.get("XDG_SESSION_TYPE")=="wayland"
        )


def is_distribution_variant(variant=b"Debian") -> bool:
    if not POSIX:
        return False
    try:
        v = load_os_release_file()
        return any(l.find(variant)>=0 for l in v.splitlines() if l.startswith(b"NAME="))
    except Exception:
        pass
    try:
        d = get_linux_distribution()[0]
        if d==variant:
            return True
        if variant==b"RedHat" and d.startswith(variant):
            return True
    except Exception:
        pass
    return False

def get_distribution_version_id() -> str:
    if not POSIX:
        return ""
    try:
        v = load_os_release_file()
        for line in v.splitlines():
            l = line.decode()
            if l.startswith("VERSION_ID="):
                return l.split("=", 1)[1].strip('"')
    except Exception:
        pass
    return ""

os_release_file_data = False
def load_os_release_file() -> bytes:
    global os_release_file_data
    if os_release_file_data is False:
        try:
            os_release_file_data = load_binary_file("/etc/os-release")
        except OSError: # pragma: no cover
            os_release_file_data = None
    return os_release_file_data

def is_Ubuntu() -> bool:
    return is_distribution_variant(b"Ubuntu")

def is_Debian() -> bool:
    return is_distribution_variant(b"Debian")

def is_Raspbian() -> bool:
    return is_distribution_variant(b"Raspbian")

def is_Fedora() -> bool:
    return is_distribution_variant(b"Fedora")

def is_Arch() -> bool:
    return is_distribution_variant(b"Arch")

def is_CentOS() -> bool:
    return is_distribution_variant(b"CentOS")

def is_AlmaLinux() -> bool:
    return is_distribution_variant(b"AlmaLinux")

def is_RockyLinux() -> bool:
    return is_distribution_variant(b"Rocky Linux")

def is_OracleLinux() -> bool:
    return is_distribution_variant(b"Oracle Linux")

def is_RedHat() -> bool:
    return is_distribution_variant(b"RedHat")

def is_openSUSE() -> bool:
    return is_distribution_variant(b"openSUSE")


def is_arm() -> bool:
    import platform
    return platform.uname()[4].startswith("arm")


_linux_distribution = None
def get_linux_distribution():
    global _linux_distribution
    if LINUX and not _linux_distribution:
        #linux_distribution is deprecated in Python 3.5 and it causes warnings,
        #so use our own code first:
        cmd = ["lsb_release", "-a"]
        try:
            p = Popen(cmd, stdout=PIPE, stderr=PIPE)
            out = p.communicate()[0]
            assert p.returncode==0 and out
        except Exception:
            try:
                import platform
                _linux_distribution = platform.linux_distribution()  #@UndefinedVariable, pylint: disable=deprecated-method, no-member
            except Exception:
                _linux_distribution = ("unknown", "unknown", "unknown")
        else:
            d = {}
            for line in strtobytes(out).splitlines():
                line = bytestostr(line)
                parts = line.rstrip("\n\r").split(":", 1)
                if len(parts)==2:
                    d[parts[0].lower().replace(" ", "_")] = parts[1].strip()
            v = [d.get(x) for x in ("distributor_id", "release", "codename")]
            if None not in v:
                return tuple([bytestostr(x) for x in v])
    return _linux_distribution

def is_unity() -> bool:
    d = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
    return d.find("unity")>=0 or d.find("ubuntu")>=0

def is_gnome() -> bool:
    if os.environ.get("XDG_SESSION_DESKTOP", "").split("-", 1)[0] in ("i3", "ubuntu", ):
        #"i3-gnome" is not really gnome... ie: the systray does work!
        return False
    return os.environ.get("XDG_CURRENT_DESKTOP", "").lower().find("gnome")>=0

def is_kde() -> bool:
    return os.environ.get("XDG_CURRENT_DESKTOP", "").lower().find("kde")>=0


def get_loaded_kernel_modules(*modlist):
    loaded = []
    if LINUX and os.path.exists("/sys/module"):
        for mod in modlist:
            if os.path.exists(f"/sys/module/{mod}"):  # pragma: no cover
                loaded.append(mod)
    return loaded


def is_WSL() -> bool:
    if not POSIX:
        return False
    r = None
    for f in ("/proc/sys/kernel/osrelease", "/proc/version"):
        r = load_binary_file(f)
        if r:
            break
    return r is not None and r.find(b"Microsoft")>=0


def get_generic_os_name() -> str:
    return do_get_generic_os_name().lower()

def do_get_generic_os_name() -> str:
    for k,v in {
            "linux"     : "Linux",
            "darwin"    : "MacOS",
            "win"       : "Win32",
            "freebsd"   : "FreeBSD",
            }.items():
        if sys.platform.startswith(k):
            return v
    return sys.platform     # pragma: no cover


def filedata_nocrlf(filename) -> str:
    v = load_binary_file(filename)
    if v is None:
        get_util_logger().error(f"failed to load {filename!r}")
        return None
    return v.strip(b"\n\r")

def load_binary_file(filename) -> bytes:
    if not os.path.exists(filename):
        return None
    try:
        with open(filename, "rb") as f:
            return f.read()
    except Exception as e:  # pragma: no cover
        get_util_logger().debug(f"load_binary_file({filename})", exc_info=True)
        get_util_logger().warn(f"Warning: failed to load {filename!r}")
        get_util_logger().warn(f" {e}")
        return None

def get_proc_cmdline(pid):
    if pid and LINUX:
        #try to find the command via /proc:
        proc_cmd_line = os.path.join("/proc", f"{pid}", "cmdline")
        if os.path.exists(proc_cmd_line):
            return load_binary_file(proc_cmd_line).rstrip(b"\0").split(b"\0")
    return None

def parse_encoded_bin_data(data):
    if not data:
        return None
    header = bytestostr(data).lower()[:10]
    if header.startswith("0x"):
        return binascii.unhexlify(data[2:])
    import base64
    if header.startswith("b64:"):
        return base64.b64decode(data[4:])
    if header.startswith("base64:"):
        return base64.b64decode(data[7:])
    try:
        return binascii.unhexlify(data)
    except (TypeError, binascii.Error):
        try:
            return base64.b64decode(data)
        except Exception:
            pass
    return None


#here so we can override it when needed
def force_quit(status=1):
    os._exit(status)  #pylint: disable=protected-access


def no_idle(fn, *args, **kwargs):
    fn(*args, **kwargs)
def register_SIGUSR_signals(idle_add=no_idle):
    if not os.name=="posix":
        return
    from xpra.util import dump_all_frames, dump_gc_frames
    def sigusr1(*_args):
        log = get_util_logger().info
        log("SIGUSR1")
        idle_add(dump_all_frames, log)
    def sigusr2(*_args):
        log = get_util_logger().info
        log("SIGUSR2")
        idle_add(dump_gc_frames, log)
    signal.signal(signal.SIGUSR1, sigusr1)
    signal.signal(signal.SIGUSR2, sigusr2)


def livefds():
    live = set()
    try:
        MAXFD = os.sysconf("SC_OPEN_MAX")
    except (ValueError, AttributeError):
        MAXFD = 256
    for fd in range(0, MAXFD):
        try:
            s = os.fstat(fd)
        except Exception:
            continue
        else:
            if s:
                live.add(fd)
    return live


def use_tty():
    from xpra.util import envbool
    if envbool("XPRA_NOTTY", False):
        return False
    from xpra.platform.gui import use_stdin
    return use_stdin()

def use_gui_prompt():
    return WIN32 or OSX or not use_tty()


def shellsub(s, subs=None):
    """ shell style string substitution using the dictionary given """
    if subs:
        for var,value in subs.items():
            try:
                if isinstance(s, bytes):
                    s = s.replace(f"${var}".encode(), str(value).encode())
                    s = s.replace(("${%s}" % var).encode(), str(value).encode())
                else:
                    s = s.replace(f"${var}", str(value))
                    s = s.replace("${%s}" % var, str(value))
            except (TypeError, ValueError):
                raise Exception(f"failed to substitute {var!r} with value {value!r} ({type(value)}) in {s!r}") from None
    return s


def osexpand(s, actual_username="", uid=0, gid=0, subs=None):
    if not s:
        return s
    def expanduser(s):
        if actual_username and s.startswith("~/"):
            #replace "~/" with "~$actual_username/"
            return os.path.expanduser("~%s/%s" % (actual_username, s[2:]))
        return os.path.expanduser(s)
    d = dict(subs or {})
    d.update({
        "PID"   : os.getpid(),
        "HOME"  : expanduser("~/"),
        })
    if os.name=="posix":
        d.update({
            "UID"   : uid or os.geteuid(),
            "GID"   : gid or os.getegid(),
            })
        if not OSX:
            from xpra.platform.xposix.paths import get_runtime_dir
            rd = get_runtime_dir()
            if rd and "XDG_RUNTIME_DIR" not in os.environ:
                d["XDG_RUNTIME_DIR"] = rd
    if actual_username:
        d["USERNAME"] = actual_username
        d["USER"] = actual_username
    #first, expand the substitutions themselves,
    #as they may contain references to other variables:
    ssub = {}
    for k,v in d.items():
        ssub[k] = expanduser(shellsub(str(v), d))
    return os.path.expandvars(expanduser(shellsub(expanduser(s), ssub)))


def path_permission_info(filename, ftype=None):
    if not POSIX:
        return []
    info = []
    try:
        stat_info = os.stat(filename)
        if not ftype:
            ftype = "file"
            if os.path.isdir(filename):
                ftype = "directory"
        operm = oct(stat.S_IMODE(stat_info.st_mode))
        info.append(f"permissions on {ftype} {filename}: {operm}")
        # pylint: disable=import-outside-toplevel
        import pwd
        import grp      #@UnresolvedImport
        user = pwd.getpwuid(stat_info.st_uid)[0]
        group = grp.getgrgid(stat_info.st_gid)[0]
        info.append(f"ownership {user}:{group}")
    except Exception as e:
        info.append(f"failed to query path information for {filename!r}: {e}")
    return info


#code to temporarily redirect stderr and restore it afterwards, adapted from:
#http://stackoverflow.com/questions/5081657/how-do-i-prevent-a-c-shared-library-to-print-on-stdout-in-python
#used by the sound code to get rid of the stupid gst warning below:
#"** Message: pygobject_register_sinkfunc is deprecated (GstObject)"
#ideally we would redirect to a buffer so we could still capture and show these messages in debug out
class HideStdErr:
    __slots__ = ("savedstderr")
    def __init__(self, *_args):
        self.savedstderr = None

    def __enter__(self):
        if POSIX and os.getppid()==1:
            #this interferes with server daemonizing?
            return
        sys.stderr.flush() # <--- important when redirecting to files
        self.savedstderr = os.dup(2)
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, 2)
        os.close(devnull)
        sys.stderr = os.fdopen(self.savedstderr, 'w')

    def __exit__(self, *_args):
        if self.savedstderr is not None:
            os.dup2(self.savedstderr, 2)

class HideSysArgv:
    __slots__ = ("savedsysargv")
    def __init__(self, *_args):
        self.savedsysargv = None

    def __enter__(self):
        self.savedsysargv = sys.argv
        sys.argv = sys.argv[:1]

    def __exit__(self, *_args):
        if self.savedsysargv is not None:
            sys.argv = self.savedsysargv


class OSEnvContext:
    __slots__ = ("env")
    def __init__(self):
        self.env = {}
    def __enter__(self):
        self.env = os.environ.copy()
    def __exit__(self, *_args):
        os.environ.clear()
        os.environ.update(self.env)
    def __repr__(self):
        return "OSEnvContext"


class DummyContextManager:
    __slots__ = ()
    def __enter__(self):
        """ do nothing """
    def __exit__(self, *_args):
        """ do nothing """
    def __repr__(self):
        return "DummyContextManager"


#workaround incompatibility between paramiko and gssapi:
class nomodule_context:
    __slots__ = ("module_name", "saved_module")
    def __init__(self, module_name):
        self.module_name = module_name
    def __enter__(self):
        self.saved_module = sys.modules.get(self.module_name)
        sys.modules[self.module_name] = None
    def __exit__(self, *_args):
        if sys.modules.get(self.module_name) is None:
            if self.saved_module is None:
                sys.modules.pop(self.module_name, None)
            else:
                sys.modules[self.module_name] = self.saved_module
    def __repr__(self):
        return f"nomodule_context({self.module_name})"

class umask_context:
    __slots__ = ("umask", "orig_umask")
    def __init__(self, umask):
        self.umask = umask
    def __enter__(self):
        self.orig_umask = os.umask(self.umask)
    def __exit__(self, *_args):
        os.umask(self.orig_umask)
    def __repr__(self):
        return f"umask_context({self.umask})"


def disable_stdout_buffering():
    import gc
    # Appending to gc.garbage is a way to stop an object from being
    # destroyed.  If the old sys.stdout is ever collected, it will
    # close() stdout, which is not good.
    gc.garbage.append(sys.stdout)
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

def setbinarymode(fd):
    if WIN32:
        #turn on binary mode:
        try:
            import msvcrt
            msvcrt.setmode(fd, os.O_BINARY)         #@UndefinedVariable pylint: disable=no-member
        except OSError:
            get_util_logger().error("setting stdin to binary mode failed", exc_info=True)

def find_lib_ldconfig(libname):
    libname = re.escape(libname)

    arch_map = {"x86_64": "libc6,x86-64"}
    arch = arch_map.get(os.uname()[4], "libc6")

    pattern = r'^\s+lib%s\.[^\s]+ \(%s(?:,.*?)?\) => (.*lib%s[^\s]+)' % (libname, arch, libname)

    #try to find ldconfig first, which may not be on the $PATH
    #(it isn't on Debian..)
    ldconfig = "ldconfig"
    for d in ("/sbin", "/usr/sbin"):
        t = os.path.join(d, "ldconfig")
        if os.path.exists(t):
            ldconfig = t
            break
    import subprocess
    p = subprocess.Popen(f"{ldconfig} -p", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    data = bytestostr(p.communicate()[0])

    libpath = re.search(pattern, data, re.MULTILINE)        #@UndefinedVariable
    if libpath:
        libpath = libpath.group(1)
    return libpath

def find_lib(libname):
    #it would be better to rely on dlopen to find the paths
    #but I cannot find a way of getting ctypes to tell us the path
    #it found the library in
    assert POSIX
    libpaths = os.environ.get("LD_LIBRARY_PATH", "").split(":")
    if BITS==64 and os.path.exists("/usr/lib64"):
        libpaths.append("/usr/lib64")
    else:
        libpaths.append("/usr/lib")
    for libpath in libpaths:
        if not libpath or not os.path.exists(libpath):
            continue
        libname_so = os.path.join(libpath, libname)
        if os.path.exists(libname_so):
            return libname_so
    return None


def pollwait(process, timeout=5):
    start = monotonic()
    v = None
    while monotonic()-start<timeout:
        v = process.poll()
        if v is not None:
            break
        sleep(0.1)
    return v


def find_in_PATH(command):
    path = os.environ.get("PATH", None)
    if not path:
        return None
    paths = path.split(os.pathsep)
    for p in paths:
        f = os.path.join(p, command)
        if os.path.isfile(f):
            return f
    return None

def which(command):
    try:
        from shutil import which as find_executable
    except ImportError:
        try:
            from distutils.spawn import find_executable  # pylint: disable=deprecated-module
        except ImportError:
            find_executable = find_in_PATH
    try:
        return find_executable(command)
    except Exception:
        get_util_logger().debug(f"find_executable({command})", exc_info=True)
        return None

def get_status_output(*args, **kwargs):
    kwargs.update({
        "stdout"    : PIPE,
        "stderr"    : PIPE,
        "universal_newlines"    : True,
        })
    try:
        p = Popen(*args, **kwargs)
    except Exception as e:
        from xpra.log import Logger
        log = Logger("util")
        log.error(f"Error running {args},{kwargs}: {e}")
        return -1, "", ""
    stdout, stderr = p.communicate()
    return p.returncode, stdout, stderr


def is_systemd_pid1() -> bool:
    if not POSIX:
        return False
    d = load_binary_file("/proc/1/cmdline")
    return d and d.find(b"/systemd")>=0


def get_ssh_port() -> int:
    #on Linux we can run "ssh -T | grep port"
    #but this usually requires root permissions to access /etc/ssh/sshd_config
    if WIN32:
        return 0
    return 22


def setuidgid(uid, gid):
    if not POSIX:
        return
    log = get_util_logger()
    if os.getuid()!=uid or os.getgid()!=gid:
        #find the username for the given uid:
        from pwd import getpwuid
        try:
            username = getpwuid(uid).pw_name
        except KeyError:
            raise Exception(f"uid {uid} not found") from None
        #set the groups:
        if hasattr(os, "initgroups"):   # python >= 2.7
            os.initgroups(username, gid)
        else:
            import grp      #@UnresolvedImport
            groups = [gr.gr_gid for gr in grp.getgrall() if username in gr.gr_mem]
            os.setgroups(groups)
    #change uid and gid:
    try:
        if os.getgid()!=gid:
            os.setgid(gid)
    except OSError as e:
        log.error(f"Error: cannot change gid to {gid}")
        if os.getgid()==0:
            #don't run as root!
            raise
        log.estr(e)
        log.error(" continuing with gid={os.getgid()}")
    try:
        if os.getuid()!=uid:
            os.setuid(uid)
    except OSError as e:
        log.error(f"Error: cannot change uid to {uid}")
        if os.getuid()==0:
            #don't run as root!
            raise
        log.estr(e)
        log.error(f" continuing with uid={os.getuid()}")
    log(f"new uid={os.getuid()}, gid={os.getgid()}")

def get_peercred(sock):
    if LINUX:
        SO_PEERCRED = 17
        log = get_util_logger()
        try:
            creds = sock.getsockopt(socket.SOL_SOCKET, SO_PEERCRED, struct.calcsize(b'3i'))
            pid, uid, gid = struct.unpack(b'3i',creds)
            log("peer: %s", (pid, uid, gid))
            return pid, uid, gid
        except IOError as  e:
            log("getsockopt", exc_info=True)
            log.error(f"Error getting peer credentials: {e}")
            return None
    elif FREEBSD:
        log.warn("Warning: peercred is not yet implemented for FreeBSD")
        #use getpeereid
        #then pwd to get the gid?
    return None

def is_socket(sockpath, check_uid=None):
    try:
        s = os.stat(sockpath)
    except OSError as e:
        get_util_logger().debug(f"is_socket({sockpath}) path cannot be accessed: {e}")
        #socket cannot be accessed
        return False
    if not stat.S_ISSOCK(s.st_mode):
        return False
    if check_uid is not None:
        if s.st_uid!=check_uid:
            #socket uid does not match
            get_util_logger().debug(f"is_socket({sockpath}) uid {s.st_uid} does not match {check_uid}")
            return False
    return True
