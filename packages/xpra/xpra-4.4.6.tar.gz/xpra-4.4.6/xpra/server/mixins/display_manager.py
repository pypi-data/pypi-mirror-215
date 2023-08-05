# -*- coding: utf-8 -*-
# This file is part of Xpra.
# Copyright (C) 2010-2023 Antoine Martin <antoine@xpra.org>
# Xpra is released under the terms of the GNU GPL v2, or, at your option, any
# later version. See the file COPYING for details.

from xpra.util import engs, log_screen_sizes
from xpra.os_util import bytestostr
from xpra.scripts.config import FALSE_OPTIONS, TRUE_OPTIONS
from xpra.common import get_refresh_rate_for_value, FULL_INFO
from xpra.server.mixins.stub_server_mixin import StubServerMixin
from xpra.log import Logger

log = Logger("screen")
gllog = Logger("opengl")


class DisplayManager(StubServerMixin):
    """
    Mixin for servers that handle displays.
    """
    DEFAULT_REFRESH_RATE = 0

    def __init__(self):
        self.randr = False
        self.bell = False
        self.cursors = False
        self.default_dpi = 96
        self.dpi = 0
        self.xdpi = 0
        self.ydpi = 0
        self.antialias = {}
        self.cursor_size = 0
        self.double_click_time  = -1
        self.double_click_distance = -1, -1
        self.opengl = False
        self.opengl_props = {}
        self.refresh_rate = "auto"

    def init(self, opts):
        self.opengl = opts.opengl
        self.bell = opts.bell
        self.cursors = opts.cursors
        self.default_dpi = int(opts.dpi)
        self.bit_depth = self.get_display_bit_depth()
        self.refresh_rate = opts.refresh_rate

    def get_display_bit_depth(self):
        return 0


    def get_refresh_rate_for_value(self, invalue):
        return get_refresh_rate_for_value(self.refresh_rate, invalue)

    def parse_hello(self, ss, caps, send_ui):
        if send_ui:
            self.parse_screen_info(ss)


    def last_client_exited(self):
        self.reset_icc_profile()


    def threaded_setup(self):
        self.opengl_props = self.query_opengl()


    def query_opengl(self):
        props = {}
        if self.opengl.lower()=="noprobe" or self.opengl.lower() in FALSE_OPTIONS:
            gllog("query_opengl() skipped because opengl=%s", self.opengl)
            return props
        try:
            from subprocess import Popen, PIPE
            from xpra.platform.paths import get_xpra_command
            cmd = self.get_full_child_command(get_xpra_command()+["opengl", "--opengl=yes"])
            env = self.get_child_env()
            #we want the output so we can parse it:
            env["XPRA_REDIRECT_OUTPUT"] = "0"
            proc = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, env=env)
            out,err = proc.communicate()
            gllog("out(%s)=%s", cmd, out)
            gllog("err(%s)=%s", cmd, err)
            if proc.returncode==0:
                #parse output:
                for line in out.splitlines():
                    parts = line.split(b"=")
                    if len(parts)!=2:
                        continue
                    k = bytestostr(parts[0].strip())
                    v = bytestostr(parts[1].strip())
                    props[k] = v
                gllog("opengl props=%s", props)
                if props and props.get("success", "").lower() in TRUE_OPTIONS:
                    gllog.info(f"OpenGL is supported on display {self.display_name!r}")
                    renderer = props.get("renderer")
                    if renderer:
                        gllog.info(f" using {renderer!r} renderer")
                else:
                    gllog.info("No OpenGL information available")
            else:
                props["error-details"] = str(err).strip("\n\r")
                error = "unknown error"
                for x in str(err).splitlines():
                    if x.startswith("RuntimeError: "):
                        error = x[len("RuntimeError: "):]
                        break
                    if x.startswith("ImportError: "):
                        error = x[len("ImportError: "):]
                        break
                props["error"] = error
                log.warn("Warning: OpenGL support check failed:")
                log.warn(f" {error}")
        except Exception as e:
            gllog("query_opengl()", exc_info=True)
            gllog.error("Error: OpenGL support check failed")
            gllog.error(f" {e!r}")
            props["error"] = str(e)
        gllog("OpenGL: %s", props)
        return props


    def get_caps(self, source) -> dict:
        root_w, root_h = self.get_root_window_size()
        caps = {
            "bell"          : self.bell,
            "cursors"       : self.cursors,
            "desktop_size"  : self._get_desktop_size_capability(source, root_w, root_h),
            }
        if FULL_INFO and self.opengl_props:
            caps["opengl"] = self.opengl_props
        return caps

    def get_info(self, _proto) -> dict:
        i = {
                "randr" : self.randr,
                "bell"  : self.bell,
                "cursors" : {
                    ""      : self.cursors,
                    "size"  : self.cursor_size,
                    },
                "double-click"  : {
                    "time"      : self.double_click_time,
                    "distance"  : self.double_click_distance,
                    },
                "dpi" : {
                    "default"   : self.default_dpi,
                    "value"     : self.dpi,
                    "x"         : self.xdpi,
                    "y"         : self.ydpi,
                    },
                "antialias" : self.antialias,
                "depth" : self.bit_depth,
                "refresh-rate"  : self.refresh_rate,
                }
        if self.opengl_props:
            i["opengl"] = self.opengl_props
        return {
            "display": i,
            }


    def _process_set_cursors(self, proto, packet):
        assert self.cursors, "cannot toggle send_cursors: the feature is disabled"
        ss = self.get_server_source(proto)
        if ss:
            ss.send_cursors = bool(packet[1])

    def _process_set_bell(self, proto, packet):
        assert self.bell, "cannot toggle send_bell: the feature is disabled"
        ss = self.get_server_source(proto)
        if ss:
            ss.send_bell = bool(packet[1])


    ######################################################################
    # display / screen / root window:
    def set_screen_geometry_attributes(self, w, h):
        #by default, use the screen as desktop area:
        self.set_desktop_geometry_attributes(w, h)

    def set_desktop_geometry_attributes(self, w, h):
        self.calculate_desktops()
        self.calculate_workarea(w, h)
        self.set_desktop_geometry(w, h)


    def parse_screen_info(self, ss):
        return self.do_parse_screen_info(ss, ss.desktop_size)

    def do_parse_screen_info(self, ss, desktop_size):
        log("do_parse_screen_info%s", (ss, desktop_size))
        dw, dh = None, None
        if desktop_size:
            try:
                dw, dh = desktop_size
                log.info(" client root window size is %sx%s", dw, dh)
                if ss.screen_sizes:
                    log_screen_sizes(dw, dh, ss.screen_sizes)
            except Exception:
                dw, dh = None, None
        sw, sh = self.configure_best_screen_size()
        log("configure_best_screen_size()=%s", (sw, sh))
        #we will tell the client about the size chosen in the hello we send back,
        #so record this size as the current server desktop size to avoid change notifications:
        ss.desktop_size_server = sw, sh
        #prefer desktop size, fallback to screen size:
        w = dw or sw
        h = dh or sh
        #clamp to max supported:
        maxw, maxh = self.get_max_screen_size()
        w = min(w, maxw)
        h = min(h, maxh)
        self.set_desktop_geometry_attributes(w, h)
        self.set_icc_profile()
        self.apply_refresh_rate(ss)
        return w, h


    def set_icc_profile(self):
        log("set_icc_profile() not implemented")

    def reset_icc_profile(self):
        log("reset_icc_profile() not implemented")


    def _monitors_changed(self, screen):
        self.do_screen_changed(screen)

    def _screen_size_changed(self, screen):
        self.do_screen_changed(screen)

    def do_screen_changed(self, screen):
        log("do_screen_changed(%s)", screen)
        #randr has resized the screen, tell the client (if it supports it)
        w, h = screen.get_width(), screen.get_height()
        log("new screen dimensions: %ix%i", w, h)
        self.set_screen_geometry_attributes(w, h)
        self.idle_add(self.send_updated_screen_size)

    def get_root_window_size(self):
        raise NotImplementedError()

    def send_updated_screen_size(self):
        max_w, max_h = self.get_max_screen_size()
        root_w, root_h = self.get_root_window_size()
        root_w = min(root_w, max_w)
        root_h = min(root_h, max_h)
        count = 0
        for ss in self._server_sources.values():
            if ss.updated_desktop_size(root_w, root_h, max_w, max_h):
                count +=1
        if count>0:
            log.info("sent updated screen size to %s client%s: %sx%s (max %sx%s)",
                     count, engs(count), root_w, root_h, max_w, max_h)

    def get_max_screen_size(self):
        max_w, max_h = self.get_root_window_size()
        return max_w, max_h

    def _get_desktop_size_capability(self, server_source, root_w, root_h):
        client_size = server_source.desktop_size
        log("client resolution is %s, current server resolution is %sx%s", client_size, root_w, root_h)
        if not client_size:
            #client did not specify size, just return what we have
            return root_w, root_h
        client_w, client_h = client_size
        w = min(client_w, root_w)
        h = min(client_h, root_h)
        return w, h

    def configure_best_screen_size(self):
        root_w, root_h = self.get_root_window_size()
        return root_w, root_h


    def apply_refresh_rate(self, ss):
        rrate = self.get_client_refresh_rate(ss)
        if rrate>0:
            self.set_window_refresh_rate(ss, rrate)
        return rrate

    def set_window_refresh_rate(self, ss, rrate):
        if hasattr(ss, "all_window_sources"):
            for window_source in ss.all_window_sources():
                bc = window_source.batch_config
                if bc:
                    bc.match_vrefresh(rrate)

    def get_client_refresh_rate(self, ss):
        vrefresh = []
        #use the refresh-rate value from the monitors
        #(value is pre-multiplied by 1000!)
        if ss.monitors:
            for mdef in ss.monitors.values():
                v = mdef.get("refresh-rate", 0)
                if v:
                    vrefresh.append(v)
        if not vrefresh and getattr(ss, "vrefresh", 0)>0:
            vrefresh.append(ss.vrefresh*1000)
        if not vrefresh:
            vrefresh.append(self.DEFAULT_REFRESH_RATE)
        rrate = 0
        if vrefresh:
            rrate = min(vrefresh)
            if self.refresh_rate:
                rrate = get_refresh_rate_for_value(self.refresh_rate, rrate)
            rrate //= 1000
        log("get_client_refresh_rate(%s)=%s (from %s)", ss, rrate, vrefresh)
        return rrate

    def _process_desktop_size(self, proto, packet):
        log("new desktop size from %s: %s", proto, packet)
        width, height = packet[1:3]
        ss = self.get_server_source(proto)
        if ss is None:
            return
        ss.desktop_size = (width, height)
        if len(packet)>=12:
            ss.set_monitors(packet[11])
        elif len(packet)>=11:
            #fallback to the older global attribute:
            v = packet[10]
            if 0<v<240 and hasattr(ss, "vrefresh") and getattr(ss, "vrefresh")!=v:
                ss.vrefresh = v
        if len(packet)>=10:
            #added in 0.16 for scaled client displays:
            xdpi, ydpi = packet[8:10]
            if xdpi!=self.xdpi or ydpi!=self.ydpi:
                self.xdpi, self.ydpi = xdpi, ydpi
                log("new dpi: %ix%i", self.xdpi, self.ydpi)
                self.dpi = round((self.xdpi + self.ydpi)/2)
                self.dpi_changed()
        if len(packet)>=8:
            #added in 0.16 for scaled client displays:
            ss.desktop_size_unscaled = packet[6:8]
        if len(packet)>=6:
            desktops, desktop_names = packet[4:6]
            ss.set_desktops(desktops, desktop_names)
            self.calculate_desktops()
        if len(packet)>=4:
            ss.set_screen_sizes(packet[3])
        bigger = ss.screen_resize_bigger
        log("client requesting new size: %sx%s (bigger=%s)", width, height, bigger)
        self.set_screen_size(width, height, bigger)
        if len(packet)>=4:
            log.info("received updated display dimensions")
            log.info("client display size is %sx%s",
                     width, height)
            log_screen_sizes(width, height, ss.screen_sizes)
            self.calculate_workarea(width, height)
        self.apply_refresh_rate(ss)
        #ensures that DPI and antialias information gets reset:
        self.update_all_server_settings()

    def dpi_changed(self):
        """
        The x11 servers override this method
        to also update the XSettings.
        """

    def calculate_desktops(self):
        """ seamless servers can update the desktops """

    def calculate_workarea(self, w, h):
        raise NotImplementedError()

    def set_workarea(self, workarea):
        pass


    ######################################################################
    # screenshots:
    def _process_screenshot(self, proto, _packet):
        packet = self.make_screenshot_packet()
        ss = self.get_server_source(proto)
        if packet and ss:
            ss.send(*packet)

    def make_screenshot_packet(self):
        try:
            return self.do_make_screenshot_packet()
        except Exception:
            log.error("make_screenshot_packet()", exc_info=True)
            return None

    def do_make_screenshot_packet(self):
        raise NotImplementedError("no screenshot capability in %s" % type(self))

    def send_screenshot(self, proto):
        #this is a screenshot request, handle it and disconnect
        try:
            packet = self.make_screenshot_packet()
            if not packet:
                self.send_disconnect(proto, "screenshot failed")
                return
            proto.send_now(packet)
            self.timeout_add(5*1000, self.send_disconnect, proto, "screenshot sent")
        except Exception as e:
            log.error("failed to capture screenshot", exc_info=True)
            self.send_disconnect(proto, "screenshot failed: %s" % e)


    def init_packet_handlers(self):
        self.add_packet_handlers({
            "set-cursors"   : self._process_set_cursors,
            "set-bell"      : self._process_set_bell,
            "desktop_size"  : self._process_desktop_size,
            "screenshot"    : self._process_screenshot,
            })
