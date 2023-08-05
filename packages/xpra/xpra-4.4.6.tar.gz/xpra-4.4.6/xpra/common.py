# This file is part of Xpra.
# Copyright (C) 2019-2022 Antoine Martin <antoine@xpra.org>
# Xpra is released under the terms of the GNU GPL v2, or, at your option, any
# later version. See the file COPYING for details.

import os
from xpra.util import envint, envbool, csv


RESOLUTION_ALIASES = {
    "QVGA"  : (320, 240),
    "VGA"   : (640, 480),
    "SVGA"  : (800, 600),
    "XGA"   : (1024, 768),
    "1080P" : (1920, 1080),
    "FHD"   : (1920, 1080),
    "4K"    : (3840, 2160),
    "5K"    : (5120, 2880),
    "8K"    : (7680, 4320),
    }

#X11 constants we use for gravity:
NorthWestGravity = 1
NorthGravity     = 2
NorthEastGravity = 3
WestGravity      = 4
CenterGravity    = 5
EastGravity      = 6
SouthWestGravity = 7
SouthGravity     = 8
SouthEastGravity = 9
StaticGravity    = 10

GRAVITY_STR = {
    NorthWestGravity : "NorthWest",
    NorthGravity     : "North",
    NorthEastGravity : "NorthEast",
    WestGravity      : "West",
    CenterGravity    : "Center",
    EastGravity      : "East",
    SouthWestGravity : "SouthWest",
    SouthGravity     : "South",
    SouthEastGravity : "SouthEast",
    StaticGravity    : "South",
    }

CLOBBER_UPGRADE = 0x1
CLOBBER_USE_DISPLAY = 0x2

#if you want to use a virtual screen bigger than this
#you will need to change those values, but some broken toolkits
#will then misbehave (they use signed shorts instead of signed ints..)
MAX_WINDOW_SIZE = 2**15-2**13


GROUP = os.environ.get("XPRA_GROUP", "xpra")

FULL_INFO = envint("XPRA_FULL_INFO", 1)
assert FULL_INFO>=0
LOG_HELLO = envbool("XPRA_LOG_HELLO", False)

SSH_AGENT_DISPATCH = envbool("XPRA_SSH_AGENT_DISPATCH", os.name=="posix")

#MIN_COMPRESS_SIZE = envint("XPRA_MAX_DECOMPRESSED_SIZE", 512)
MIN_COMPRESS_SIZE = envint("XPRA_MAX_DECOMPRESSED_SIZE", -1)
MAX_DECOMPRESSED_SIZE = envint("XPRA_MAX_DECOMPRESSED_SIZE", 256*1024*1024)


DEFAULT_REFRESH_RATE = envint("XPRA_DEFAULT_REFRESH_RATE", 50*1000)

SPLASH_EXIT_DELAY = envint("XPRA_SPLASH_EXIT_DELAY", 4)

DEFAULT_XDG_DATA_DIRS = ":".join(
        (
        "/usr/share",
        "/usr/local/share",
        "~/.local/share/applications",
        "~/.local/share/flatpak/exports/share",
        "/var/lib/flatpak/exports/share",
        )
    )

def noop(*_args):
    """ do nothing """

WINDOW_DECODE_SKIPPED = 0
WINDOW_DECODE_ERROR = -1
WINDOW_NOT_FOUND = -2


class KeyEvent:
    __slots__ = ("modifiers", "keyname", "keyval", "keycode", "group", "string", "pressed")

    def __repr__(self):
        return "KeyEvent(%s)" % csv("%s=%s" % (k, getattr(self, k)) for k in KeyEvent.__slots__)


def get_refresh_rate_for_value(refresh_rate_str, invalue):
    def i(v):
        try:
            return int(v)
        except ValueError:
            return None
    if refresh_rate_str.lower() in ("none", "auto"):
        #just honour whatever the client supplied:
        return i(invalue)
    v = i(refresh_rate_str)
    if v is not None:
        #server specifies an absolute value:
        if 0<v<1000:
            return v*1000
        if v>=1000:
            return v
    if refresh_rate_str.endswith("%"):
        #server specifies a percentage:
        mult = i(refresh_rate_str[:-1])  #ie: "80%" -> 80
        iv = i(invalue)
        if mult and iv:
            return iv*mult//100
    #fallback to client supplied value, if any:
    return i(invalue)


def adjust_monitor_refresh_rate(refresh_rate_str, mdef):
    adjusted = {}
    for i, monitor in mdef.items():
        #make a copy, don't modify in place!
        #(as this may be called multiple times on the same input dict)
        mprops = dict(monitor)
        if refresh_rate_str!="auto":
            value = monitor.get("refresh-rate", DEFAULT_REFRESH_RATE)
            value = get_refresh_rate_for_value(refresh_rate_str, value)
            if value:
                mprops["refresh-rate"] = value
        adjusted[i] = mprops
    return adjusted
