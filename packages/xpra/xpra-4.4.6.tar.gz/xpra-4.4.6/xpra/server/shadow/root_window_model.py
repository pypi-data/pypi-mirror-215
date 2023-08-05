# -*- coding: utf-8 -*-
# This file is part of Xpra.
# Copyright (C) 2012-2022 Antoine Martin <antoine@xpra.org>
# Xpra is released under the terms of the GNU GPL v2, or, at your option, any
# later version. See the file COPYING for details.

import socket
from collections import namedtuple

from xpra.os_util import (
    get_generic_os_name, do_get_generic_os_name,
    load_binary_file, get_linux_distribution,
    )
from xpra.platform.paths import get_icon_filename
from xpra.log import Logger

log = Logger("shadow")


def get_os_icons():
    try:
        from PIL import Image  # pylint: disable=import-outside-toplevel
    except ImportError:
        return ()
    filename = (get_generic_os_name() or "").lower()+".png"
    icon_name = get_icon_filename(filename)
    if not icon_name:
        log(f"get_os_icons() no icon matching {filename!r}")
        return ()
    try:
        img = Image.open(icon_name)
        log(f"Image({icon_name})={img}")
        if img:
            icon_data = load_binary_file(icon_name)
            if not icon_data:
                log(f"icon {icon_name} not found")
                return ()
            w, h = img.size
            img.close()
            icon = (w, h, "png", icon_data)
            icons = (icon,)
            return icons
    except Exception:   # pragma: no cover
        log.error(f"Error: failed to load window icon {icon_name!r}", exc_info=True)
    return ()


class RootWindowModel:
    __slots__ = ("window", "title", "geometry", "capture",
                 "property_names", "dynamic_property_names", "internal_property_names",
                 "signal_listeners")
    def __init__(self, root_window, capture=None, title="", geometry=None):
        self.window = root_window
        self.title = title
        self.geometry = geometry
        self.capture = capture
        self.property_names = [
            "title", "class-instance",
            "client-machine", "window-type",
            "size-hints", "icons", "shadow",
            "depth",
            ]
        self.dynamic_property_names = []
        self.internal_property_names = ["content-type"]
        self.signal_listeners = {}

    def __repr__(self):
        return f"RootWindowModel({self.capture} : {str(self.geometry):24})"

    def get_info(self) -> dict:
        info = {}
        c = self.capture
        if c:
            info["capture"] = c.get_info()
        return info

    def take_screenshot(self):
        return self.capture.take_screenshot()

    def get_image(self, x, y, width, height):
        ox, oy = self.geometry[:2]
        image = self.capture.get_image(ox+x, oy+y, width, height)
        if image and (ox>0 or oy>0):
            #adjust x and y of where the image is displayed on the client (target_x and target_y)
            #not where the image lives within the current buffer (x and y)
            image.set_target_x(x)
            image.set_target_y(y)
        return image

    def unmanage(self, exiting=False):
        pass

    def suspend(self):
        pass

    def is_managed(self):
        return True

    def is_tray(self):
        return False

    def is_OR(self):
        return False

    def has_alpha(self):
        return False

    def uses_XShm(self):
        return False

    def is_shadow(self):
        return True

    def get_default_window_icon(self, _size):
        return None

    def acknowledge_changes(self):
        pass

    def get_dimensions(self):
        #used by get_window_info only
        return self.geometry[2:4]

    def get_geometry(self):
        return self.geometry


    def get_property_names(self):
        return self.property_names

    def get_dynamic_property_names(self):
        return self.dynamic_property_names

    def get_internal_property_names(self):
        return self.internal_property_names

    def get_property(self, prop):
        #subclasses can define properties as attributes:
        attr_name = prop.replace("-", "_")
        if hasattr(self, attr_name):
            return getattr(self, attr_name)
        #otherwise fallback to default behaviour:
        if prop=="title":
            return self.title
        if prop=="client-machine":
            return socket.gethostname()
        if prop=="window-type":
            return ["NORMAL"]
        if prop=="fullscreen":
            return False
        if prop=="shadow":
            return True
        if prop=="depth":
            return 24
        if prop=="scaling":
            return None
        if prop=="opacity":
            return None
        if prop=="size-hints":
            size = self.get_dimensions()
            return {
                "maximum-size"  : size,
                "minimum-size"  : size,
                "base-size" : size,
                }
        if prop=="class-instance":
            osn = do_get_generic_os_name()
            if osn=="Linux":
                try:
                    osn += "-"+get_linux_distribution()[0].replace(" ", "-")
                except Exception:   # pragma: no cover
                    pass
            return f"xpra-{osn.lower()}", f"Xpra {osn.replace('-', ' ')}"
        if prop=="icons":
            return get_os_icons()
        if prop=="content-type":
            return "desktop"
        raise ValueError(f"invalid property {prop!r}")

    def get(self, name, default_value=None):
        try:
            return self.get_property(name)
        except ValueError as e:
            log("get(%s, %s) %s on %s", name, default_value, e, self)
            return default_value

    def notify(self, prop):
        if prop not in self.dynamic_property_names:
            log.warn(f"Warning: ignoring notify for {prop!r}")
            return
        PSpec = namedtuple("PSpec", "name")
        pspec = PSpec(name=prop)
        listeners = self.signal_listeners.get(prop)
        for listener, *args in listeners:
            try:
                listener(self, pspec, *args)
            except Exception:
                log.error(f"Error on {prop!r} signal listener {listener}", exc_info=True)

    def managed_connect(self, signal, *args):   # pragma: no cover
        self.connect(signal, *args)

    def connect(self, signal, *args):           # pragma: no cover
        prop = signal.split(":")[-1]        #notify::geometry
        if prop not in self.dynamic_property_names:
            log.warn(f"Warning: ignoring signal connect request: {args}")
            return
        self.signal_listeners.setdefault(prop, []).append(args)

    def disconnect(self, *args):        # pragma: no cover
        log.warn(f"Warning: ignoring signal disconnect request: {args}")
