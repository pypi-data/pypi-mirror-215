# -*- coding: utf-8 -*-
# This file is part of Xpra.
# Copyright (C) 2010-2021 Antoine Martin <antoine@xpra.org>
# Xpra is released under the terms of the GNU GPL v2, or, at your option, any
# later version. See the file COPYING for details.

from xpra.util import get_screen_info, envint, first_time, typedict, net_utf8
from xpra.server.source.stub_source_mixin import StubSourceMixin
from xpra.log import Logger

log = Logger("av-sync")


class ClientDisplayMixin(StubSourceMixin):
    """
    Store information and manage events related to the client's display
    """

    def cleanup(self):
        self.init_state()

    def init_state(self):
        self.vrefresh = -1
        self.icc = {}
        self.display_icc = {}
        self.randr_notify = False
        self.desktop_size = None
        self.desktop_mode_size = None
        self.desktop_size_unscaled = None
        self.desktop_size_server = None
        self.screen_sizes = ()
        self.monitors = {}
        self.screen_resize_bigger = True
        self.desktops = 1
        self.desktop_names = ()
        self.show_desktop_allowed = False
        self.opengl_props = {}

    def get_info(self) -> dict:
        info = {
            "vertical-refresh"  : self.vrefresh,
            "desktop_size"  : self.desktop_size or "",
            "desktops"      : self.desktops,
            "desktop_names" : self.desktop_names,
            "randr_notify"  : self.randr_notify,
            "opengl"        : self.opengl_props,
            "monitors"      : self.monitors,
            }
        info.update(get_screen_info(self.screen_sizes))
        if self.desktop_mode_size:
            info["desktop_mode_size"] = self.desktop_mode_size
        if self.desktop_size_unscaled:
            info["desktop_size"] = {"unscaled" : self.desktop_size_unscaled}
        return info

    def parse_client_caps(self, c : typedict):
        self.vrefresh = c.intget("vrefresh", -1)
        self.randr_notify = c.boolget("randr_notify")
        self.desktop_size = c.intpair("desktop_size")
        if self.desktop_size is not None:
            w, h = self.desktop_size
            if w<=0 or h<=0 or w>=32768 or h>=32768:
                log.warn("ignoring invalid desktop dimensions: %sx%s", w, h)
                self.desktop_size = None
        self.desktop_mode_size = c.intpair("desktop_mode_size")
        self.desktop_size_unscaled = c.intpair("desktop_size.unscaled")
        self.screen_resize_bigger = c.boolget("screen-resize-bigger", True)
        self.set_screen_sizes(c.tupleget("screen_sizes"))
        self.set_monitors(c.dictget("monitors"))
        desktop_names = tuple(net_utf8(x) for x in c.tupleget("desktop.names"))
        self.set_desktops(c.intget("desktops", 1), desktop_names)
        self.show_desktop_allowed = c.boolget("show-desktop")
        self.icc = c.dictget("icc", {})
        self.display_icc = c.dictget("display-icc", {})
        self.opengl_props = c.dictget("opengl", {})

    def set_monitors(self, monitors):
        self.monitors = {}
        if monitors:
            for i, mon_def in monitors.items():
                vdef = self.monitors.setdefault(i, {})
                td = typedict(mon_def)
                for attr, conv in {
                    "geometry"  : td.inttupleget,
                    "primary"   : td.boolget,
                    "refresh-rate"  : td.intget,
                    "scale-factor"  : td.intget,
                    "width-mm"      : td.intget,
                    "height-mm"     : td.intget,
                    "manufacturer"  : td.strget,
                    "model"         : td.strget,
                    "subpixel-layout" : td.strget,
                    "workarea"      : td.inttupleget,
                    }.items():
                    v = conv(attr)
                    if v is not None:
                        vdef[attr] = conv(attr)
        log("set_monitors(%s) monitors=%s", monitors, self.monitors)

    def set_screen_sizes(self, screen_sizes):
        log("set_screen_sizes(%s)", screen_sizes)
        self.screen_sizes = list(screen_sizes)
        #validate dpi / screen size in mm
        #(ticket 2480: GTK3 on macos can return bogus values)
        MIN_DPI = envint("XPRA_MIN_DPI", 10)
        MAX_DPI = envint("XPRA_MIN_DPI", 500)
        def dpi(size_pixels, size_mm):
            if size_mm==0:
                return 0
            return round(size_pixels * 25.4 / size_mm)
        for i,screen in enumerate(list(screen_sizes)):
            if len(screen)<10:
                continue
            sw, sh, wmm, hmm, monitors = screen[1:6]
            xdpi = dpi(sw, wmm)
            ydpi = dpi(sh, hmm)
            if xdpi<MIN_DPI or xdpi>MAX_DPI or ydpi<MIN_DPI or ydpi>MAX_DPI:
                warn = first_time("invalid-screen-size-%ix%i" % (wmm, hmm))
                if warn:
                    log.warn("Warning: ignoring invalid screen size %ix%i mm", wmm, hmm)
                if monitors:
                    #[plug_name, xs(geom.x), ys(geom.y), xs(geom.width), ys(geom.height), wmm, hmm]
                    wmm = round(sum(monitor[5] for monitor in monitors))
                    hmm = round(sum(monitor[6] for monitor in monitors))
                    xdpi = dpi(sw, wmm)
                    ydpi = dpi(sh, hmm)
                if xdpi<MIN_DPI or xdpi>MAX_DPI or ydpi<MIN_DPI or ydpi>MAX_DPI:
                    #still invalid, generate one from DPI=96
                    wmm = round(sw*25.4/96)
                    hmm = round(sh*25.4/96)
                if warn:
                    log.warn(" using %ix%i mm", wmm, hmm)
                screen = list(screen)
                #make sure values are integers:
                screen[1] = round(sw)
                screen[2] = round(sh)
                screen[3] = wmm
                screen[4] = hmm
                self.screen_sizes[i] = tuple(screen)
        log("client validated screen sizes: %s", self.screen_sizes)

    def set_desktops(self, desktops, desktop_names):
        self.desktops = desktops or 1
        self.desktop_names = tuple(net_utf8(d) for d in (desktop_names or ()))

    def updated_desktop_size(self, root_w, root_h, max_w, max_h):
        log("updated_desktop_size%s randr_notify=%s, desktop_size=%s",
            (root_w, root_h, max_w, max_h), self.randr_notify, self.desktop_size)
        if not self.hello_sent:
            return False
        if self.randr_notify and (not self.desktop_size_server or tuple(self.desktop_size_server)!=(root_w, root_h)):
            self.desktop_size_server = root_w, root_h
            self.send("desktop_size", root_w, root_h, max_w, max_h)
            return True
        return False

    def show_desktop(self, show):
        if self.show_desktop_allowed and self.hello_sent:
            self.send_async("show-desktop", show)
