# This file is part of Xpra.
# Copyright (C) 2008 Nathaniel Smith <njs@pobox.com>
# Copyright (C) 2012-2022 Antoine Martin <antoine@xpra.org>
# Xpra is released under the terms of the GNU GPL v2, or, at your option, any
# later version. See the file COPYING for details.

import os
import hashlib
from time import monotonic
from threading import Lock
from collections import deque
from PIL import Image, ImageFont, ImageDraw  #@UnresolvedImport
from gi.repository import GLib

from xpra.net.mmap_pipe import mmap_read
from xpra.net import compression
from xpra.util import typedict, csv, envint, envbool, first_time
from xpra.codecs.loader import get_codec
from xpra.codecs.video_helper import getVideoHelper
from xpra.os_util import bytestostr
from xpra.common import (
    NorthWestGravity,
    NorthGravity,
    NorthEastGravity,
    WestGravity,
    CenterGravity,
    EastGravity,
    SouthWestGravity,
    SouthGravity,
    SouthEastGravity,
    StaticGravity,
    GRAVITY_STR,
    )
from xpra.log import Logger

log = Logger("paint")
videolog = Logger("video", "paint")

INTEGRITY_HASH = envbool("XPRA_INTEGRITY_HASH", False)
PAINT_BOX = envint("XPRA_PAINT_BOX", 0) or envint("XPRA_OPENGL_PAINT_BOX", 0)
WEBP_PILLOW = envbool("XPRA_WEBP_PILLOW", False)
SCROLL_ENCODING = envbool("XPRA_SCROLL_ENCODING", True)
REPAINT_ALL = envbool("XPRA_REPAINT_ALL", False)
SHOW_FPS = envbool("XPRA_SHOW_FPS", False)


_PIL_font = None
def load_PIL_font():
    global _PIL_font
    if _PIL_font:
        return _PIL_font
    for font_file in (
        "/usr/share/fonts/gnu-free/FreeMono.ttf",
        "/usr/share/fonts/liberation-mono/LiberationMono-Regular.ttf",
        ):
        if os.path.exists(font_file):
            try:
                _PIL_font = ImageFont.load_path(font_file)
                return _PIL_font
            except OSError:
                pass
    _PIL_font = ImageFont.load_default()
    return _PIL_font


#ie:
#CSC_OPTIONS = { "YUV420P" : {"RGBX" : [swscale.spec], "BGRX" : ...} }
CSC_OPTIONS = None
def load_csc_options():
    global CSC_OPTIONS
    if CSC_OPTIONS is None:
        CSC_OPTIONS = {}
        vh = getVideoHelper()
        for csc_in in vh.get_csc_inputs():
            CSC_OPTIONS[csc_in] = vh.get_csc_specs(csc_in)
    return CSC_OPTIONS

#get the list of video encodings (and the module for each one):
VIDEO_DECODERS = None
def load_video_decoders():
    global VIDEO_DECODERS
    if VIDEO_DECODERS is None:
        VIDEO_DECODERS = {}
        vh = getVideoHelper()
        for encoding in vh.get_decodings():
            specs = vh.get_decoder_specs(encoding)
            for colorspace, decoders in specs.items():
                log("%-5s decoders for %7s: %s", encoding, colorspace, csv([d.get_type() for _,d in decoders]))
                assert decoders
                #use the first one:
                _, decoder_module = decoders[0]
                VIDEO_DECODERS[encoding] = decoder_module
        log("video decoders: %s", dict((e,d.get_type()) for e,d in VIDEO_DECODERS.items()))
    return VIDEO_DECODERS


def fire_paint_callbacks(callbacks, success=True, message=""):
    for x in callbacks:
        try:
            x(success, message)
        except Exception:
            log.error("error calling %s(%s)", x, success, exc_info=True)


def verify_checksum(img_data, options):
    l = options.intget("z.len")
    if l:
        assert l==len(img_data), "compressed pixel data failed length integrity check: expected %i bytes but got %i" % (
            l, len(img_data))
    chksum = options.get("z.sha256")
    if chksum:
        h = hashlib.sha256(img_data)
    if h:
        hd = h.hexdigest()
        assert chksum==hd, "pixel data failed compressed chksum integrity check: expected %s but got %s" % (chksum, hd)


class WindowBackingBase:
    """
    Generic superclass for all Backing code,
    see CairoBackingBase and GTK2WindowBacking subclasses for actual implementations
    """
    RGB_MODES = ()

    def __init__(self, wid : int, window_alpha : bool):
        load_csc_options()
        load_video_decoders()
        self.wid = wid
        self.size = 0, 0
        self.render_size = 0, 0
        #padding between the window contents and where we actually draw the backing
        #(ie: if the window is bigger than the backing,
        # we may be rendering the backing in the center of the window)
        self.offsets = 0, 0, 0, 0       #top,left,bottom,right
        self.gravity = 0
        self._alpha_enabled = window_alpha
        self._backing = None
        self._video_decoder = None
        self._csc_decoder = None
        self._decoder_lock = Lock()
        self._PIL_encodings = []
        self.default_paint_box_line_width = PAINT_BOX or 1
        self.paint_box_line_width = PAINT_BOX
        self.pointer_overlay = None
        self.cursor_data = None
        self.default_cursor_data = None
        self.jpeg_decoder = None
        self.webp_decoder = None
        self.pil_decoder = get_codec("dec_pillow")
        if self.pil_decoder:
            self._PIL_encodings = self.pil_decoder.get_encodings()
        self.jpeg_decoder = get_codec("dec_jpeg")
        self.webp_decoder = get_codec("dec_webp")
        self.spng_decoder = get_codec("dec_spng")
        self.avif_decoder = get_codec("dec_avif")
        self.nvjpeg_decoder = get_codec("dec_nvjpeg")
        self.cuda_context = None
        self.draw_needs_refresh = True
        self.repaint_all = REPAINT_ALL
        self.mmap = None
        self.mmap_enabled = False
        self.fps_events = deque(maxlen=120)
        self.fps_buffer_size = 0, 0
        self.fps_buffer_update_time = 0
        self.fps_value = 0
        self.fps_refresh_timer = 0

    def idle_add(self, *_args, **_kwargs):
        raise NotImplementedError()

    def get_rgb_formats(self):
        if self._alpha_enabled:
            return self.RGB_MODES
        #remove modes with alpha:
        return list(filter(lambda mode : mode.find("A")<0,
                            ["BGRA", "BGRX", "RGBA", "RGBX", "BGR", "RGB", "r210", "BGR565"]))


    def get_info(self):
        info = {
            "rgb-formats"   : self.get_rgb_formats(),
            "transparency"  : self._alpha_enabled,
            "mmap"          : bool(self.mmap_enabled),
            "size"          : self.size,
            "render-size"   : self.render_size,
            "offsets"       : self.offsets,
            "fps"           : self.fps_value,
            }
        vd = self._video_decoder
        if vd:
            info["video-decoder"] = vd.get_info()
        csc = self._csc_decoder
        if csc:
            info["csc"] = csc.get_info()
        return info

    def record_fps_event(self):
        self.fps_events.append(monotonic())
        now = monotonic()
        elapsed = now-self.fps_buffer_update_time
        if elapsed>0.2:
            self.update_fps()

    def update_fps(self):
        self.fps_buffer_update_time = monotonic()
        self.fps_value = self.calculate_fps()
        if self.is_show_fps():
            text = "%i fps" % self.fps_value
            width, height = 64, 32
            self.fps_buffer_size = (width, height)
            pixels = self.rgba_text(text, width, height)
            self.update_fps_buffer(width, height, pixels)

    def update_fps_buffer(self, width, height, pixels):
        raise NotImplementedError

    def calculate_fps(self):
        pe = list(self.fps_events)
        if not pe:
            return 0
        e0 = pe[0]
        now = monotonic()
        elapsed = now-e0
        if elapsed<=1 and len(pe)>=5:
            return len(pe)//elapsed
        cutoff = now-1
        count = 0
        while pe and pe.pop()>=cutoff:
            count += 1
        return count

    def is_show_fps(self):
        if not SHOW_FPS and self.paint_box_line_width<=0:
            return False
        #show fps if the value is non-zero:
        if self.fps_value>0:
            return True
        pe = list(self.fps_events)
        if not pe:
            return False
        last_fps_event = pe[-1]
        #or if there was an event less than N seconds ago:
        N = 4
        return monotonic()-last_fps_event<N

    def rgba_text(self, text, width=64, height=32, x=20, y=10, bg=(128, 128, 128, 32)):
        rgb_format = "RGBA"
        img = Image.new(rgb_format, (width, height), color=bg)
        draw = ImageDraw.Draw(img)
        font = load_PIL_font()
        draw.text((x, y), text, "blue", font=font)
        return img.tobytes("raw", rgb_format)

    def cancel_fps_refresh(self):
        frt = self.fps_refresh_timer
        if frt:
            self.fps_refresh_timer = 0
            GLib.source_remove(frt)


    def enable_mmap(self, mmap_area):
        self.mmap = mmap_area
        self.mmap_enabled = True

    def gravity_copy_coords(self, oldw, oldh, bw, bh):
        sx = sy = dx = dy = 0
        def center_y():
            if bh>=oldh:
                #take the whole source, paste it in the middle
                return 0, (bh-oldh)//2
            #skip the edges of the source, paste all of it
            return (oldh-bh)//2, 0
        def center_x():
            if bw>=oldw:
                return 0, (bw-oldw)//2
            return (oldw-bw)//2, 0
        def east_x():
            if bw>=oldw:
                return 0, bw-oldw
            return oldw-bw, 0
        def west_x():
            return 0, 0
        def north_y():
            return 0, 0
        def south_y():
            if bh>=oldh:
                return 0, bh-oldh
            return oldh-bh, 0
        g = self.gravity
        if not g or g==NorthWestGravity:
            #undefined (or 0), use NW
            sx, dx = west_x()
            sy, dy = north_y()
        elif g==NorthGravity:
            sx, dx = center_x()
            sy, dy = north_y()
        elif g==NorthEastGravity:
            sx, dx = east_x()
            sy, dy = north_y()
        elif g==WestGravity:
            sx, dx = west_x()
            sy, dy = center_y()
        elif g==CenterGravity:
            sx, dx = center_x()
            sy, dy = center_y()
        elif g==EastGravity:
            sx, dx = east_x()
            sy, dy = center_y()
        elif g==SouthWestGravity:
            sx, dx = west_x()
            sy, dy = south_y()
        elif g==SouthGravity:
            sx, dx = center_x()
            sy, dy = south_y()
        elif g==SouthEastGravity:
            sx, dx = east_x()
            sy, dy = south_y()
        elif g==StaticGravity:
            if first_time("StaticGravity-%i" % self.wid):
                log.warn("Warning: window %i requested static gravity", self.wid)
                log.warn(" this is not implemented yet")
        w = min(bw, oldw)
        h = min(bh, oldh)
        return sx, sy, dx, dy, w, h

    def gravity_adjust(self, x, y, options):
        #if the window size has changed,
        #adjust the coordinates honouring the window gravity:
        window_size = options.inttupleget("window-size", None)
        g = self.gravity
        log("gravity_adjust%s window_size=%s, size=%s, gravity=%s",
            (x, y, options), window_size, self.size, GRAVITY_STR.get(g, "unknown"))
        if not window_size:
            return x, y
        window_size = tuple(window_size)
        if window_size==self.size:
            return x, y
        if g==0 or self.gravity==NorthWestGravity:
            return x, y
        oldw, oldh = window_size
        bw, bh = self.size
        def center_y():
            if bh>=oldh:
                return y + (bh-oldh)//2
            return y - (oldh-bh)//2
        def center_x():
            if bw>=oldw:
                return x + (bw-oldw)//2
            return x - (oldw-bw)//2
        def east_x():
            if bw>=oldw:
                return x + (bw-oldw)
            return x - (oldw-bw)
        def west_x():
            return x
        def north_y():
            return y
        def south_y():
            if bh>=oldh:
                return y + (bh-oldh)
            return y - (oldh-bh)
        if g==NorthGravity:
            return center_x(), north_y()
        if g==NorthEastGravity:
            return east_x(), north_y()
        if g==WestGravity:
            return west_x(), center_y()
        if g==CenterGravity:
            return center_x(), center_y()
        if g==EastGravity:
            return east_x(), center_y()
        if g==SouthWestGravity:
            return west_x(), south_y()
        if g==SouthGravity:
            return center_x(), south_y()
        if g==SouthEastGravity:
            return east_x(), south_y()
        #if self.gravity==StaticGravity:
        #    pass
        return x, y

    def assign_cuda_context(self, opengl=False):
        if self.cuda_context is None:
            from xpra.codecs.nvidia.nvjpeg.decoder import get_default_device  # @NoMove pylint: disable=no-name-in-module, import-outside-toplevel
            dev = get_default_device()
            assert dev
            #make this an opengl compatible context:
            from xpra.codecs.cuda_common.cuda_context import cuda_device_context
            self.cuda_context = cuda_device_context(dev.device_id, dev.device, opengl)
            #create the context now as this is the part that takes time:
            self.cuda_context.make_context()
        return self.cuda_context


    def free_cuda_context(self):
        cc = self.cuda_context
        if cc:
            self.cuda_context = None
            cc.free()

    def close(self):
        self.free_cuda_context()
        self.cancel_fps_refresh()
        self._backing = None
        log("%s.close() video_decoder=%s", self, self._video_decoder)
        #try without blocking, if that fails then
        #the lock is held by the decoding thread,
        #and it will run the cleanup after releasing the lock
        #(it checks for self._backing None)
        self.close_decoder(False)

    def close_decoder(self, blocking=False):
        videolog("close_decoder(%s)", blocking)
        dl = self._decoder_lock
        if dl is None or not dl.acquire(blocking):
            videolog("close_decoder(%s) lock %s not acquired", blocking, dl)
            return False
        try:
            self.do_clean_video_decoder()
            self.do_clean_csc_decoder()
            return True
        finally:
            dl.release()

    def do_clean_video_decoder(self):
        if self._video_decoder:
            self._video_decoder.clean()
            self._video_decoder = None

    def do_clean_csc_decoder(self):
        if self._csc_decoder:
            self._csc_decoder.clean()
            self._csc_decoder = None


    def get_encoding_properties(self):
        return {
                 "encodings.rgb_formats"    : self.get_rgb_formats(),
                 "encoding.transparency"    : self._alpha_enabled,
                 "encoding.full_csc_modes"  : self._get_full_csc_modes(self.get_rgb_formats()),
                 "encoding.send-window-size" : True,
                 "encoding.render-size"     : self.render_size,
                 }

    def _get_full_csc_modes(self, rgb_modes):
        #calculate the server CSC modes the server is allowed to use
        #based on the client CSC modes we can convert to in the backing class we use
        #and trim the transparency if we cannot handle it
        target_rgb_modes = tuple(rgb_modes)
        if not self._alpha_enabled:
            target_rgb_modes = tuple(x for x in target_rgb_modes if x.find("A")<0)
        full_csc_modes = getVideoHelper().get_server_full_csc_modes_for_rgb(*target_rgb_modes)
        full_csc_modes["webp"] = tuple(x for x in rgb_modes if x in ("BGRX", "BGRA", "RGBX", "RGBA"))
        full_csc_modes["jpeg"] = tuple(x for x in rgb_modes if x in ("BGRX", "BGRA", "RGBX", "RGBA", "YUV420P"))
        full_csc_modes["jpega"] = tuple(x for x in rgb_modes if x in ("BGRA", "RGBA"))
        videolog("_get_full_csc_modes(%s) with target_rgb_modes=%s", rgb_modes, target_rgb_modes)
        for e in sorted(full_csc_modes.keys()):
            modes = full_csc_modes.get(e)
            videolog(" * %s : %s", e, modes)
        return full_csc_modes


    def set_cursor_data(self, cursor_data):
        self.cursor_data = cursor_data


    def paint_jpeg(self, img_data, x, y, width, height, options, callbacks):
        self.do_paint_jpeg("jpeg", img_data, x, y, width, height, options, callbacks)

    def paint_jpega(self, img_data, x, y, width, height, options, callbacks):
        self.do_paint_jpeg("jpega", img_data, x, y, width, height, options, callbacks)

    def do_paint_jpeg(self, encoding, img_data, x, y, width, height, options, callbacks):
        alpha_offset = options.intget("alpha-offset", 0)
        log("do_paint_jpeg: nvjpeg_decoder=%s", self.nvjpeg_decoder)
        img = None
        if self.nvjpeg_decoder and not alpha_offset:
            try:
                with self.assign_cuda_context(False):
                    img = self.nvjpeg_decoder.decompress_and_download("RGB", img_data)
            except Exception as e:
                if first_time(str(e)):
                    log.error("Error accessing cuda context", exc_info=True)
                else:
                    log("cuda context error, again")
        if img is None:
            if encoding=="jpeg":
                rgb_format = "RGBX"
            elif encoding=="jpega":
                rgb_format = "BGRA"
            else:
                raise Exception("invalid encoding %r" % encoding)
            img = self.jpeg_decoder.decompress_to_rgb(rgb_format, img_data, alpha_offset)
        rgb_format = img.get_pixel_format()
        img_data = img.get_pixels()
        rowstride = img.get_rowstride()
        w = img.get_width()
        h = img.get_height()
        self.idle_add(self.do_paint_rgb, rgb_format, img_data,
                  x, y, w, h, width, height, rowstride, options, callbacks)

    def paint_avif(self, img_data, x, y, width, height, options, callbacks):
        img = self.avif_decoder.decompress(img_data, options)
        rgb_format = img.get_pixel_format()
        img_data = img.get_pixels()
        rowstride = img.get_rowstride()
        w = img.get_width()
        h = img.get_height()
        self.idle_add(self.do_paint_rgb, rgb_format, img_data,
                      x, y, w, h, width, height, rowstride, options, callbacks)

    def paint_image(self, coding, img_data, x, y, width, height, options, callbacks):
        # can be called from any thread
        rgb_format, img_data, iwidth, iheight, rowstride = self.pil_decoder.decompress(coding, img_data, options)
        self.idle_add(self.do_paint_rgb, rgb_format, img_data,
                      x, y, iwidth, iheight, width, height, rowstride, options, callbacks)

    def paint_spng(self, img_data, x, y, width, height, options, callbacks):
        rgba, rgb_format, iwidth, iheight = self.spng_decoder.decompress(img_data)
        rowstride = iwidth*len(rgb_format)
        self.idle_add(self.do_paint_rgb, rgb_format, rgba,
                      x, y, iwidth, iheight, width, height, rowstride, options, callbacks)


    def paint_webp(self, img_data, x, y, width, height, options, callbacks):
        if not self.webp_decoder or WEBP_PILLOW:
            #if webp is enabled, then Pillow should be able to take care of it:
            self.paint_image("webp", img_data, x, y, width, height, options, callbacks)
            return
        rgb_format = options.strget("rgb_format")
        has_alpha = options.boolget("has_alpha", False)
        (
            buffer_wrapper,
            iwidth, iheight, stride, has_alpha,
            rgb_format,
            ) = self.webp_decoder.decompress(img_data, has_alpha, rgb_format, self.get_rgb_formats())
        def free_buffer(*_args):
            buffer_wrapper.free()
        callbacks.append(free_buffer)
        data = buffer_wrapper.get_pixels()
        #if the backing can't handle this format,
        #ie: tray only supports RGBA
        if rgb_format not in self.get_rgb_formats():
            # pylint: disable=import-outside-toplevel
            from xpra.codecs.rgb_transform import rgb_reformat
            from xpra.codecs.image_wrapper import ImageWrapper
            img = ImageWrapper(x, y, iwidth, iheight, data, rgb_format,
                               len(rgb_format)*8, stride, len(rgb_format), ImageWrapper.PACKED, True, None)
            rgb_reformat(img, self.get_rgb_formats(), has_alpha and self._alpha_enabled)
            rgb_format = img.get_pixel_format()
            data = img.get_pixels()
            stride = img.get_rowstride()
        #replace with the actual rgb format we get from the decoder:
        options["rgb_format"] = rgb_format
        self.idle_add(self.do_paint_rgb, rgb_format, data,
                                 x, y, iwidth, iheight, width, height, stride, options, callbacks)

    def paint_rgb(self, rgb_format, raw_data, x, y, width, height, rowstride, options, callbacks):
        """ can be called from a non-UI thread """
        iwidth, iheight = options.intpair("scaled-size", (width, height))
        #was a compressor used?
        comp = tuple(x for x in compression.ALL_COMPRESSORS if options.intget(x, 0))
        if comp:
            assert len(comp)==1, "more than one compressor specified: %s" % str(comp)
            rgb_data = compression.decompress_by_name(raw_data, algo=comp[0])
        else:
            rgb_data = raw_data
        self.idle_add(self.do_paint_rgb, rgb_format, rgb_data,
                      x, y, iwidth, iheight, width, height, rowstride, options, callbacks)

    def do_paint_rgb(self, rgb_format, img_data,
                     x, y, width, height, render_width, render_height, rowstride, options, callbacks):
        """ must be called from the UI thread
            this method is only here to ensure that we always fire the callbacks,
            the actual paint code is in _do_paint_rgb[24|32]
        """
        x, y = self.gravity_adjust(x, y, options)
        try:
            if not options.boolget("paint", True):
                fire_paint_callbacks(callbacks)
                return
            if self._backing is None:
                fire_paint_callbacks(callbacks, -1, "no backing")
                return
            if rgb_format=="r210":
                bpp = 30
            elif rgb_format=="BGR565":
                bpp = 16
            else:
                bpp = len(rgb_format)*8     #ie: "BGRA" -> 32
            if bpp==16:
                paint_fn = self._do_paint_rgb16
            elif bpp==24:
                paint_fn = self._do_paint_rgb24
            elif bpp==30:
                paint_fn = self._do_paint_rgb30
            elif bpp==32:
                paint_fn = self._do_paint_rgb32
            else:
                raise Exception("invalid rgb format '%s'" % rgb_format)
            options["rgb_format"] = rgb_format
            success = paint_fn(img_data, x, y, width, height, render_width, render_height, rowstride, options)
            fire_paint_callbacks(callbacks, success)
        except Exception as e:
            if not self._backing:
                fire_paint_callbacks(callbacks, -1, "paint error on closed backing ignored")
            else:
                log.error("Error painting rgb%s", bpp, exc_info=True)
                message = "paint rgb%s error: %s" % (bpp, e)
                fire_paint_callbacks(callbacks, False, message)

    def _do_paint_rgb16(self, img_data, x, y, width, height, render_width, render_height, rowstride, options):
        raise NotImplementedError

    def _do_paint_rgb24(self, img_data, x, y, width, height, render_width, render_height, rowstride, options):
        raise NotImplementedError

    def _do_paint_rgb30(self, img_data, x, y, width, height, render_width, render_height, rowstride, options):
        raise NotImplementedError

    def _do_paint_rgb32(self, img_data, x, y, width, height, render_width, render_height, rowstride, options):
        raise NotImplementedError


    def eos(self):
        dl = self._decoder_lock
        with dl:
            self.do_clean_csc_decoder()
            self.do_clean_video_decoder()


    def make_csc(self, src_width, src_height, src_format,
                       dst_width, dst_height, dst_format_options, speed):
        global CSC_OPTIONS
        in_options = CSC_OPTIONS.get(src_format, {})
        if not in_options:
            log.error("Error: no csc options for '%s' input, only found:", src_format)
            for k,v in CSC_OPTIONS.items():
                log.error(" * %-8s : %s", k, csv(v))
            raise Exception("no csc options for '%s' input in %s" % (src_format, csv(CSC_OPTIONS.keys())))
        videolog("make_csc%s",
            (src_width, src_height, src_format, dst_width, dst_height, dst_format_options, speed))
        for dst_format in dst_format_options:
            specs = in_options.get(dst_format)
            videolog("make_csc specs(%s)=%s", dst_format, specs)
            if not specs:
                continue
            for spec in specs:
                v = self.validate_csc_size(spec, src_width, src_height, dst_width, dst_height)
                if v:
                    continue
                options = {"speed" : speed}
                try:
                    csc = spec.make_instance()
                    csc.init_context(src_width, src_height, src_format,
                               dst_width, dst_height, dst_format, options)
                    return csc
                except Exception as e:
                    videolog("make_csc%s",
                        (src_width, src_height, src_format, dst_width, dst_height, dst_format_options, options),
                        exc_info=True)
                    videolog.error("Error: failed to create csc instance %s", spec.codec_class)
                    videolog.error(" for %s to %s: %s", src_format, dst_format, e)
        videolog.error("Error: no matching CSC module found")
        videolog.error(" for %ix%i %s source format,", src_width, src_height, src_format)
        videolog.error(" to %ix%i %s", dst_width, dst_height, " or ".join(dst_format_options))
        videolog.error(" with options=%s, speed=%i", dst_format_options, speed)
        videolog.error(" tested:")
        for dst_format in dst_format_options:
            specs = in_options.get(dst_format)
            if not specs:
                continue
            videolog.error(" * %s:", dst_format)
            for spec in specs:
                videolog.error("   - %s:", spec)
                v = self.validate_csc_size(spec, src_width, src_height, dst_width, dst_height)
                if v:
                    videolog.error("       "+v[0], *v[1:])
        raise Exception("no csc module found for wid %i %s(%sx%s) to %s(%sx%s) in %s" %
                        (self.wid, src_format, src_width, src_height, " or ".join(dst_format_options),
                         dst_width, dst_height, CSC_OPTIONS))

    def validate_csc_size(self, spec, src_width, src_height, dst_width, dst_height):
        if not spec.can_scale and (src_width!=dst_width or src_height!=dst_height):
            return "scaling not suported"
        if src_width<spec.min_w:
            return "source width %i is out of range: minimum is %i", src_width, spec.min_w
        if src_height<spec.min_h:
            return "source height %i is out of range: minimum is %i", src_height, spec.min_h
        if dst_width<spec.min_w:
            return "target width %i is out of range: minimum is %i", dst_width, spec.min_w
        if dst_height<spec.min_h:
            return "target height %i is out of range: minimum is %i", dst_height, spec.min_h
        if src_width>spec.max_w:
            return "source width %i is out of range: maximum is %i", src_width, spec.max_w
        if src_height>spec.max_h:
            return "source height %i is out of range: maximum is %i", src_height, spec.max_h
        if dst_width>spec.max_w:
            return "target width %i is out of range: maximum is %i", dst_width, spec.max_w
        if dst_height>spec.max_h:
            return "target height %i is out of range: maximum is %i", dst_height, spec.max_h
        return None

    def paint_with_video_decoder(self, decoder_module, coding, img_data, x, y, width, height, options, callbacks):
        assert decoder_module, "decoder module not found for %s" % coding
        dl = self._decoder_lock
        if dl is None:
            fire_paint_callbacks(callbacks, False, "no lock - retry")
            return
        with dl:
            if self._backing is None:
                message = "window %s is already gone!" % self.wid
                log(message)
                fire_paint_callbacks(callbacks, -1, message)
                return
            enc_width, enc_height = options.intpair("scaled_size", (width, height))
            input_colorspace = options.strget("csc", "YUV420P")
            #do we need a prep step for decoders that cannot handle the input_colorspace directly?
            decoder_colorspaces = decoder_module.get_input_colorspaces(coding)
            assert input_colorspace in decoder_colorspaces, "decoder %s does not support %s for %s" % (
                decoder_module.get_type(), input_colorspace, coding)

            vd = self._video_decoder
            if vd:
                if options.intget("frame", -1)==0:
                    videolog("paint_with_video_decoder: first frame of new stream")
                    self.do_clean_video_decoder()
                elif vd.get_encoding()!=coding:
                    videolog("paint_with_video_decoder: encoding changed from %s to %s", vd.get_encoding(), coding)
                    self.do_clean_video_decoder()
                elif vd.get_width()!=enc_width or vd.get_height()!=enc_height:
                    videolog("paint_with_video_decoder: video dimensions have changed from %s to %s",
                        (vd.get_width(), vd.get_height()), (enc_width, enc_height))
                    self.do_clean_video_decoder()
                elif vd.get_colorspace()!=input_colorspace:
                    #this should only happen on encoder restart, which means this should be the first frame:
                    videolog.warn("Warning: colorspace unexpectedly changed from %s to %s",
                             vd.get_colorspace(), input_colorspace)
                    self.do_clean_video_decoder()
            if self._video_decoder is None:
                videolog("paint_with_video_decoder: new %s(%s,%s,%s)",
                    decoder_module.Decoder, width, height, input_colorspace)
                vd = decoder_module.Decoder()
                vd.init_context(coding, enc_width, enc_height, input_colorspace)
                self._video_decoder = vd
                videolog("paint_with_video_decoder: info=%s", vd.get_info())

            img = vd.decompress_image(img_data, options)
            if not img:
                if options.intget("delayed", 0)>0:
                    #there are further frames queued up,
                    #and this frame references those, so assume all is well:
                    fire_paint_callbacks(callbacks)
                else:
                    fire_paint_callbacks(callbacks, False,
                                         "video decoder %s failed to decode %i bytes of %s data" % (
                                             vd.get_type(), len(img_data), coding))
                    videolog.error("Error: decode failed on %s bytes of %s data", len(img_data), coding)
                    videolog.error(" %sx%s pixels using %s", width, height, vd.get_type())
                    videolog.error(" frame options:")
                    for k,v in options.items():
                        if isinstance(v, bytes):
                            v = bytestostr(v)
                        videolog.error("   %s=%s", bytestostr(k), v)
                return

            x, y = self.gravity_adjust(x, y, options)
            self.do_video_paint(img, x, y, enc_width, enc_height, width, height, options, callbacks)
        if self._backing is None:
            self.close_decoder(True)

    def do_video_paint(self, img, x, y, enc_width, enc_height, width, height, options, callbacks):
        target_rgb_formats = self.get_rgb_formats()
        #as some video formats like vpx can forward transparency
        #also we could skip the csc step in some cases:
        pixel_format = img.get_pixel_format()
        cd = self._csc_decoder
        if cd is not None:
            if cd.get_src_format()!=pixel_format:
                videolog("do_video_paint csc: switching src format from %s to %s", cd.get_src_format(), pixel_format)
                self.do_clean_csc_decoder()
            elif cd.get_dst_format() not in target_rgb_formats:
                videolog("do_video_paint csc: switching dst format from %s to %s", cd.get_dst_format(), target_rgb_formats)
                self.do_clean_csc_decoder()
            elif cd.get_src_width()!=enc_width or cd.get_src_height()!=enc_height:
                videolog("do_video_paint csc: switching src size from %sx%s to %sx%s",
                         enc_width, enc_height, cd.get_src_width(), cd.get_src_height())
                self.do_clean_csc_decoder()
            elif cd.get_dst_width()!=width or cd.get_dst_height()!=height:
                videolog("do_video_paint csc: switching src size from %sx%s to %sx%s",
                         width, height, cd.get_dst_width(), cd.get_dst_height())
                self.do_clean_csc_decoder()
        if self._csc_decoder is None:
            #use higher quality csc to compensate for lower quality source
            #(which generally means that we downscaled via YUV422P or lower)
            #or when upscaling the video:
            q = options.intget("quality", 50)
            csc_speed = int(min(100, 100-q, 100.0 * (enc_width*enc_height) / (width*height)))
            cd = self.make_csc(enc_width, enc_height, pixel_format,
                                           width, height, target_rgb_formats, csc_speed)
            videolog("do_video_paint new csc decoder: %s", cd)
            self._csc_decoder = cd
        rgb_format = cd.get_dst_format()
        rgb = cd.convert_image(img)
        videolog("do_video_paint rgb using %s.convert_image(%s)=%s", cd, img, rgb)
        img.free()
        assert rgb.get_planes()==0, "invalid number of planes for %s: %s" % (rgb_format, rgb.get_planes())
        #make a new options dict and set the rgb format:
        paint_options = typedict(options)
        #this will also take care of firing callbacks (from the UI thread):
        def paint():
            data = rgb.get_pixels()
            rowstride = rgb.get_rowstride()
            try:
                self.do_paint_rgb(rgb_format, data,
                                  x, y, width, height, width, height, rowstride, paint_options, callbacks)
            finally:
                rgb.free()
        self.idle_add(paint)

    def paint_mmap(self, img_data, x, y, width, height, rowstride, options, callbacks):
        """ must be called from UI thread
            see _mmap_send() in server.py for details """
        assert self.mmap_enabled
        data = mmap_read(self.mmap, *img_data)
        rgb_format = options.strget("rgb_format", "RGB")
        #Note: BGR(A) is only handled by gl_window_backing
        x, y = self.gravity_adjust(x, y, options)
        self.do_paint_rgb(rgb_format, data, x, y, width, height, width, height, rowstride, options, callbacks)

    def paint_scroll(self, img_data, options, callbacks):
        log("paint_scroll%s", (img_data, options, callbacks))
        raise NotImplementedError("no paint scroll on %s" % type(self))


    def draw_region(self, x, y, width, height, coding, img_data, rowstride, options, callbacks):
        """ dispatches the paint to one of the paint_XXXX methods """
        try:
            assert self._backing is not None
            log("draw_region(%s, %s, %s, %s, %s, %s bytes, %s, %s, %s)",
                x, y, width, height, coding, len(img_data), rowstride, options, callbacks)
            coding = bytestostr(coding)
            options["encoding"] = coding            #used for choosing the color of the paint box
            if INTEGRITY_HASH:
                verify_checksum(img_data, options)
            if coding == "mmap":
                self.idle_add(self.paint_mmap, img_data, x, y, width, height, rowstride, options, callbacks)
            elif coding in ("rgb24", "rgb32"):
                #avoid confusion over how many bytes-per-pixel we may have:
                rgb_format = options.strget("rgb_format")
                if not rgb_format:
                    rgb_format = {
                        "rgb24" : "RGB",
                        "rgb32" : "RGBX",
                        }.get(coding)
                if rowstride==0:
                    rowstride = width * len(rgb_format)
                self.paint_rgb(rgb_format, img_data, x, y, width, height, rowstride, options, callbacks)
            elif coding in VIDEO_DECODERS:
                self.paint_with_video_decoder(VIDEO_DECODERS.get(coding),
                                              coding,
                                              img_data, x, y, width, height, options, callbacks)
            elif self.jpeg_decoder and coding=="jpeg":
                self.paint_jpeg(img_data, x, y, width, height, options, callbacks)
            elif self.jpeg_decoder and coding=="jpega":
                self.paint_jpega(img_data, x, y, width, height, options, callbacks)
            elif self.avif_decoder and coding=="avif":
                self.paint_avif(img_data, x, y, width, height, options, callbacks)
            elif coding == "webp":
                self.paint_webp(img_data, x, y, width, height, options, callbacks)
            elif self.spng_decoder and coding=="png":
                self.paint_spng(img_data, x, y, width, height, options, callbacks)
            elif coding in self._PIL_encodings:
                self.paint_image(coding, img_data, x, y, width, height, options, callbacks)
            elif coding == "scroll":
                self.paint_scroll(img_data, options, callbacks)
            else:
                self.do_draw_region(x, y, width, height, coding, img_data, rowstride, options, callbacks)
        except Exception:
            if self._backing is None:
                fire_paint_callbacks(callbacks, -1, "this backing is closed - retry?")
            else:
                raise

    def do_draw_region(self, _x, _y, _width, _height, coding, _img_data, _rowstride, _options, callbacks):
        msg = "invalid encoding: '%s'" % coding
        log.error("Error: %s", msg)
        fire_paint_callbacks(callbacks, False, msg)
