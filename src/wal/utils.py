# -*- coding: utf-8 -*-
#
# 	Copyright (C) 2019 by Igor E. Novikov
#
# 	This program is free software: you can redistribute it and/or modify
# 	it under the terms of the GNU General Public License as published by
# 	the Free Software Foundation, either version 3 of the License, or
# 	(at your option) any later version.
#
# 	This program is distributed in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# 	GNU General Public License for more details.
#
# 	You should have received a copy of the GNU General Public License
# 	along with this program.  If not, see <https://www.gnu.org/licenses/>.


import cairo
from PIL import Image, ImageOps

import wx


def tr(msg):
    return msg.decode('utf-8') if isinstance(msg, str) else msg


def untr(msg):
    return msg.encode('utf-8') if isinstance(msg, unicode) else msg


def new_id():
    return wx.NewId()


def cursor(path, bitmap_type, x=0, y=0):
    return wx.Cursor(tr(path), bitmap_type, x, y)


def stock_cursor(cursor_id):
    return wx.StockCursor(cursor_id)


def get_bitmap_size(bitmap):
    return bitmap.GetSize()


def stream_to_image(image_stream):
    image_stream.seek(0)
    return wx.ImageFromStream(image_stream)


def stream_to_bitmap(image_stream):
    return stream_to_image(image_stream).ConvertToBitmap()


# ----- PIL interfaces

def image_to_pil_image(image):
    """
    Converts wx.Image to PIL Image object.
    """
    pil_image = Image.new('RGB', (image.GetWidth(), image.GetHeight()))
    pil_image.frombytes(image.GetData())
    if image.HasAlpha():
        alpha = Image.new('L', (image.GetWidth(), image.GetHeight()))
        alpha.frombytes(image.GetAlphaData())
        pil_image.putalpha(alpha)
    return pil_image


def pil_image_to_image(pil_image):
    """
    Converts PIL Image object to wx.Image.
    """
    image = wx.EmptyImage(*pil_image.size)
    if pil_image.mode[-1] == 'A':
        image.SetData(pil_image.convert('RGB').tobytes())
        image.SetAlphaData(pil_image.tobytes()[3::4])
    else:
        image.SetData(pil_image.tobytes())
    return image


def bitmap_to_pil_image(bitmap):
    """
    Converts wx.Bitmap to PIL Image object.
    """
    return image_to_pil_image(bitmap.ConvertToImage())


def pil_image_to_bitmap(pil_image):
    """
    Converts PIL Image object to wx.Bitmap.
    """
    return pil_image_to_image(pil_image).ConvertToBitmap()


# ----- Cairo interfaces

def copy_surface_to_bitmap(surface):
    """
    Create a wx.Bitmap from a Cairo ImageSurface.
    """
    cairo_format = surface.get_format()
    if cairo_format not in [cairo.FORMAT_ARGB32, cairo.FORMAT_RGB24]:
        raise TypeError("Unsupported format")

    width = surface.get_width()
    height = surface.get_height()
    stride = surface.get_stride()
    data = surface.get_data()
    if cairo_format == cairo.FORMAT_ARGB32:
        fmt = wx.BitmapBufferFormat_ARGB32
        bmp = wx.EmptyBitmapRGBA(width, height)
    else:
        fmt = wx.BitmapBufferFormat_RGB32
        bmp = wx.EmptyBitmap(width, height, 32)
    bmp.CopyFromBuffer(data, fmt, stride)
    return bmp


def copy_bitmap_to_surface(bitmap):
    """
    Create an ImageSurface from a wx.Bitmap
    """
    width, height = bitmap.GetSize()
    if bitmap.HasAlpha():
        cairo_format = cairo.FORMAT_ARGB32
        fmt = wx.BitmapBufferFormat_ARGB32
    else:
        cairo_format = cairo.FORMAT_RGB24
        fmt = wx.BitmapBufferFormat_RGB32

    try:
        stride = cairo.ImageSurface.format_stride_for_width(cairo_format, width)
    except AttributeError:
        stride = width * 4

    surface = cairo.ImageSurface(cairo_format, width, height)
    bitmap.CopyToBuffer(surface.get_data(), fmt, stride)
    return surface


# ----- Text routines

def get_text_size(text, bold=False, size_incr=0):
    font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
    if bold:
        font.SetWeight(wx.FONTWEIGHT_BOLD)
    if size_incr:
        if font.IsUsingSizeInPixels():
            sz = font.GetPixelSize()[1] + size_incr
            font.SetPixelSize((0, sz))
        else:
            sz = font.GetPointSize() + size_incr
            font.SetPointSize(sz)
    pdc = wx.MemoryDC()
    bmp = wx.EmptyBitmap(1, 1)
    pdc.SelectObject(bmp)
    pdc.SetFont(font)
    height = pdc.GetCharHeight()
    width = pdc.GetTextExtent(text)[0]
    result = (width, height)
    pdc.SelectObject(wx.NullBitmap)
    return result


def invert_text_bitmap(bmp, color=(0, 0, 0)):
    w, h = bmp.GetSize()
    img = bmp.ConvertToImage()
    img.ConvertColourToAlpha(0, 0, 0)
    img.SetRGBRect(wx.Rect(0, 0, w, h), *color)
    return img.ConvertToBitmap()


def text_to_bitmap(text, color=(0, 0, 0), bold=False):
    w, h = get_text_size(text, bold)
    dc = wx.MemoryDC()
    bmp = wx.EmptyBitmap(w, h)
    dc.SelectObject(bmp)
    dc.SetBackground(wx.Brush("white"))
    dc.Clear()
    font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
    if bold:
        font.SetWeight(wx.FONTWEIGHT_BOLD)
    dc.SetFont(font)
    dc.SetTextForeground(wx.Colour(*color))
    dc.DrawText(text, 0, 0)
    image = bitmap_to_pil_image(bmp)
    image.putalpha(ImageOps.invert(image).convert('L'))
    ret = pil_image_to_bitmap(image)
    dc.EndDrawing()
    dc.SelectObject(wx.NullBitmap)
    return ret, (w, h)


def recolor_bmp(bmp, color):
    image = bmp.ConvertToImage()
    if isinstance(color, wx.Colour):
        color = color.Get()
    image.SetRGBRect(wx.Rect(0, 0, *bmp.GetSize()), *color)
    return image.ConvertToBitmap()


def bmp_to_white(bmp):
    return recolor_bmp(bmp, (255, 255, 255))


def disabled_bmp(bmp):
    image = bmp.ConvertToImage()
    image = image.ConvertToGreyscale()
    image = image.AdjustChannels(1.0, 1.0, 1.0, 0.5)
    return image.ConvertToBitmap()


def get_dc(widget):
    pdc = wx.PaintDC(widget)
    # noinspection PyBroadException
    try:
        dc = wx.GCDC(pdc)
    except Exception:
        dc = pdc
    pdc.BeginDrawing()
    dc.BeginDrawing()
    return dc


def get_buffered_dc(widget):
    pdc = wx.BufferedPaintDC(widget)
    pdc.BeginDrawing()
    return pdc


def wxcolor_to_dec(wxcolor):
    return tuple(map(lambda x: x / 255.0, wxcolor.Get()[:3]))


def get_screen_dpi():
    return wx.GetDisplayPPI()


def get_screen_resolution():
    return wx.GetDisplaySize()


def get_system_fontsize():
    font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
    if font.IsUsingSizeInPixels():
        fontsize = font.GetPixelSize()
    else:
        fontsize = font.GetPointSize()
    return fontsize
