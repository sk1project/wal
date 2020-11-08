# -*- coding: utf-8 -*-
#
# 	Copyright (C) 2013-2018 by Ihor E. Novikov
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

import wx

from . import const
from . import utils


class DialogMixin(object):
    def fit(self):
        self.Fit()

    def set_title(self, title):
        self.SetTitle(title)

    def set_minsize(self, size):
        self.SetMinSize(size)

    def is_maximized(self):
        return self.IsMaximized()

    def maximize(self, val=True):
        self.Maximize(val)

    def center(self):
        self.Centre()

    def get_size(self):
        return tuple(self.GetSize())

    def set_size(self, size):
        self.SetSize(wx.Size(*size))

    def show_modal(self):
        return self.ShowModal()

    def end_modal(self, ret):
        self.EndModal(ret)

    def destroy(self):
        self.Destroy()

    def layout(self):
        self.Layout()

    def update(self):
        self.Update()


class WidgetMixin(object):
    shown = True
    enabled = True

    def set_position(self, point=(0, 0)):
        self.SetPosition(point)

    def show(self, update=True):
        self.Show()
        self.shown = True
        if update:
            parent = self.GetParent()
            parent.Layout()

    def hide(self, update=True):
        self.Hide()
        self.shown = False
        if update:
            parent = self.GetParent()
            parent.Layout()

    def get_size(self):
        return tuple(self.GetSize())

    def get_position(self):
        return self.GetPosition()

    def is_shown(self):
        return self.IsShown()

    def set_enable(self, value):
        self.enabled = value
        self.Enable(value)

    def set_visible(self, value):
        if value:
            self.show()
        else:
            self.hide()

    def get_enabled(self):
        return self.IsEnabled()

    def _set_width(self, size, width):
        if not width: return size
        width += 2
        return width * const.FONT_SIZE[0], size[1]

    def set_tooltip(self, tip=None):
        if tip:
            self.SetToolTip(tip)

    def destroy(self):
        self.Destroy()

    def set_focus(self):
        self.SetFocus()

    def set_double_buffered(self):
        if const.IS_MSW:
            self.SetDoubleBuffered(True)

    def refresh(self, x=0, y=0, w=0, h=0, clear=True):
        if not w:
            w, h = self.GetSize()
        self.Refresh(rect=wx.Rect(x, y, w, h), eraseBackground=clear)

    def get_cursor(self):
        return self.GetCursor()

    def set_cursor(self, cursor):
        self.SetCursor(cursor)

    def set_bg(self, color):
        if isinstance(color, tuple):
            self.SetBackgroundColour(wx.Colour(*color[:4]))
        else:
            self.SetBackgroundColour(color)

    def get_bg(self):
        return self.GetBackgroundColour().Get()[:3]

    def popup_menu(self, menu, position=None):
        position = position or wx.DefaultPosition
        self.PopupMenu(menu, position)

    def set_drop_target(self, target):
        self.SetDropTarget(target)


class DataWidgetMixin(WidgetMixin):
    def set_value(self, value):
        self.SetValue(value)

    def get_value(self):
        return self.GetValue()


class RangeDataWidgetMixin(DataWidgetMixin):
    range_val = ()

    def set_range(self, range_val):
        self.range_val = range_val
        self.SetRange(*range_val)

    def get_range(self):
        return self.range_val


class GenericGWidget(wx.Panel, WidgetMixin):
    decoration_padding = 0

    renderer = None
    mouse_over = False
    mouse_pressed = False
    timer = None
    onclick = None
    repeat = False
    flat = True
    buffer = None
    counter = 0

    def __init__(self, parent, tooltip='', onclick=None, repeat=False):
        self.parent = parent
        self.onclick = onclick
        self.repeat = repeat
        wx.Panel.__init__(self, parent, wx.ID_ANY)
        if const.IS_MSW:
            self.SetDoubleBuffered(True)
        self.box = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.box)
        self.box.Add((1, 1))
        if tooltip:
            self.set_tooltip(tooltip)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_PAINT, self._on_paint, self)
        self.Bind(wx.EVT_ENTER_WINDOW, self._mouse_over, self)
        self.Bind(wx.EVT_LEFT_DOWN, self._mouse_down, self)
        self.Bind(wx.EVT_LEFT_UP, self._mouse_up, self)
        self.Bind(wx.EVT_TIMER, self._on_timer)
        self.Bind(wx.EVT_LEAVE_WINDOW, self._on_win_leave, self)

    def set_enable(self, value):
        self.enabled = value
        self.refresh()

    def get_enabled(self):
        return self.enabled

    def set_size(self, w, h):
        self._set_size(w, h)
        if self.renderer:
            self.renderer._adjust_widget_size()

    def _set_size(self, w, h):
        self.box.Remove(0)
        self.box.Add((w, h))
        self.GetParent().Layout()
        self.refresh()

    def _on_paint(self, event):
        pass

    def _mouse_over(self, _event):
        self.mouse_over = True
        self.refresh()
        self.timer.Start(100)

    def _mouse_down(self, _event):
        self.mouse_pressed = True
        self.refresh()

    def _mouse_up(self, event):
        self.mouse_pressed = False
        if self.mouse_over:
            if self.onclick and self.enabled and not self.counter:
                self.counter = 5
                self.onclick()
        self.refresh()

    def _on_timer(self, _event):
        mouse_pos = wx.GetMousePosition()
        x, y = self.GetScreenPosition()
        w, h = self.GetSize()
        rect = wx.Rect(x, y, w, h)
        if not rect.Contains(mouse_pos):
            self.timer.Stop()
            if self.mouse_over:
                self.mouse_over = False
                self.mouse_pressed = False
                self.refresh()
        else:
            if self.enabled:
                self.counter = self.counter - 1 if self.counter else 0
                if self.repeat and self.onclick and self.mouse_pressed:
                    self.onclick()

    def _on_win_leave(self, _event):
        self.timer.Stop()
        if self.mouse_over:
            self.mouse_over = False
            self.mouse_pressed = False
            self.refresh()


class DrawableWidget(object):
    dc = None
    pdc = None
    dashes = None

    def __init__(self, set_timer=True, buffered=False):
        self.Bind(wx.EVT_PAINT, self._on_paint, self)
        self.Bind(wx.EVT_SIZE, self._on_size_change, self)
        if buffered:
            self.set_double_buffered()
        if set_timer and const.IS_MAC:
            self.timer = wx.Timer(self)
            self.Bind(wx.EVT_TIMER, self._repaint_after)
            self.timer.Start(50)

    def _repaint_after(self, _event):
        self.repaint_after()
        self.timer.Stop()

    def set_double_buffered(self):
        if const.IS_MSW:
            self.SetDoubleBuffered(True)

    def get_size(self):
        return tuple(self.GetSize())

    def _on_size_change(self, event):
        self.refresh()
        event.Skip()

    def _on_paint(self, _event):
        w, h = self.GetSize()
        if not w or not h:
            return
        self.pdc = wx.PaintDC(self)
        try:
            self.dc = wx.GCDC(self.pdc)
        except Exception:
            self.dc = self.pdc

        self.paint()
        self.pdc = self.dc = None

    # Paint methods for inherited class
    def paint(self):
        pass

    def repaint_after(self):
        self.refresh()

    # ========PaintDC

    def set_origin(self, x=0, y=0):
        self.pdc.SetDeviceOrigin(x, y)

    def set_stroke(self, color=None, width=1, dashes=None):
        self.dashes = [] + dashes if dashes else []
        if color is None:
            self.pdc.SetPen(wx.TRANSPARENT_PEN)
        else:
            pen = wx.Pen(wx.Colour(*color[:4]), width)
            if dashes:
                pen = wx.Pen(wx.Colour(*color[:4]), width, wx.USER_DASH)
                pen.SetDashes(self.dashes)
            pen.SetCap(wx.CAP_BUTT)
            self.pdc.SetPen(pen)

    def set_fill(self, color=None):
        self.pdc.SetBrush(wx.TRANSPARENT_BRUSH if color is None
                          else wx.Brush(wx.Colour(*color[:4])))

    def set_font(self, bold=False, size_incr=0):
        font = self.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD if bold else wx.FONTWEIGHT_NORMAL)
        if size_incr:
            sz = font.GetPixelSize()[1] + size_incr
            font.SetPixelSize((0, sz))
        self.pdc.SetFont(font)
        return self.pdc.GetCharHeight()

    def set_text_color(self, color):
        self.pdc.SetTextForeground(wx.Colour(*color[:4]))

    def draw_line(self, x0, y0, x1, y1):
        self.pdc.DrawLine(x0, y0, x1, y1)

    def draw_rounded_rect(self, x=0, y=0, w=1, h=1, radius=1.0):
        self.pdc.DrawRoundedRectangle(x, y, w, h, radius)

    def draw_rect(self, x=0, y=0, w=1, h=1):
        self.pdc.DrawRectangle(x, y, w, h)

    def draw_text(self, text, x, y):
        self.pdc.DrawText(text, x, y)

    def draw_rotated_text(self, text, x, y, angle):
        self.pdc.DrawRotatedText(text, x, y, angle)

    def draw_polygon(self, points):
        self.pdc.DrawPolygon(points)

    def draw_surface(self, surface, x=0, y=0, use_mask=True):
        self.pdc.DrawBitmap(
            utils.copy_surface_to_bitmap(surface), x, y, use_mask)

    def put_surface(self, surface, x=0, y=0, use_mask=True):
        dc = wx.ClientDC(self)
        dc.DrawBitmap(
            utils.copy_surface_to_bitmap(surface), x, y, use_mask)

    def draw_linear_gradient(self, rect, start_clr, stop_clr, ndir=False):
        ndir = wx.SOUTH if ndir else wx.EAST
        self.pdc.GradientFillLinear(
            wx.Rect(*rect),
            wx.Colour(*start_clr),
            wx.Colour(*stop_clr),
            nDirection=ndir)

    def draw_bitmap(self, bmp, x=0, y=0, use_mask=True):
        self.pdc.DrawBitmap(bmp, x, y, use_mask)

    # =========GC device

    def set_gc_origin(self, x=0, y=0):
        self.dc.SetDeviceOrigin(x, y)

    def set_gc_stroke(self, color=None, width=1, dashes=None):
        self.dashes = [] + dashes if dashes else []
        if color is None:
            self.dc.SetPen(wx.TRANSPARENT_PEN)
        else:
            pen = wx.Pen(wx.Colour(*color[:4]), width)
            if self.dashes:
                pen = wx.Pen(wx.Colour(*color[:4]), width, wx.USER_DASH)
                pen.SetDashes(self.dashes)
            pen.SetCap(wx.CAP_BUTT)
            self.dc.SetPen(pen)

    def set_gc_fill(self, color=None):
        self.dc.SetBrush(wx.TRANSPARENT_BRUSH if color is None
                         else wx.Brush(wx.Colour(*color[:4])))

    def set_gc_font(self, bold=False, size_incr=0):
        font = self.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD if bold else wx.FONTWEIGHT_NORMAL)
        if size_incr:
            if font.IsUsingSizeInPixels():
                sz = font.GetPixelSize() + size_incr
                font.SetPixelSize(sz)
            else:
                sz = font.GetPointSize() + size_incr
                font.SetPointSize(sz)
        self.dc.SetFont(font)
        return self.dc.GetCharHeight()

    def set_gc_text_color(self, color):
        self.dc.SetTextForeground(wx.Colour(*color[:4]))

    def gc_draw_rounded_rect(self, x=0, y=0, w=1, h=1, radius=1.0):
        self.dc.DrawRoundedRectangle(x, y, w, h, radius)

    def gc_draw_line(self, x0, y0, x1, y1):
        self.dc.DrawLine(x0, y0, x1, y1)

    def gc_draw_rect(self, x=0, y=0, w=1, h=1):
        self.dc.DrawRectangle(x, y, w, h)

    def gc_draw_polygon(self, points):
        self.dc.DrawPolygon(points)

    def gc_draw_text(self, text, x, y):
        self.dc.DrawText(text, x, y)

    def gc_draw_rotated_text(self, text, x, y, angle):
        self.dc.DrawRotatedText(text, x, y, angle)

    def gc_draw_surface(self, surface, x=0, y=0, use_mask=True):
        self.dc.DrawBitmap(
            utils.copy_surface_to_bitmap(surface), x, y, use_mask)

    def gc_draw_linear_gradient(self, rect, start_clr, stop_clr, ndir=False):
        ndir = wx.SOUTH if ndir else wx.EAST
        self.dc.GradientFillLinear(
            wx.Rect(*rect),
            wx.Colour(*start_clr[:4]),
            wx.Colour(*stop_clr[:4]),
            nDirection=ndir)

    def gc_draw_bitmap(self, bmp, x=0, y=0, use_mask=True):
        self.dc.DrawBitmap(bmp, x, y, use_mask)


class SensitiveWidget(object):
    kbdproc = None
    mouse_captured = False
    click_flag = False

    def __init__(self, check_move=False, kbdproc=None):
        self.kbdproc = kbdproc
        self.Bind(wx.EVT_LEFT_UP, self._mouse_left_up)
        self.Bind(wx.EVT_LEFT_DOWN, self._mouse_left_down)
        self.Bind(wx.EVT_MOUSEWHEEL, self._mouse_wheel)
        self.Bind(wx.EVT_RIGHT_DOWN, self._mouse_right_down)
        self.Bind(wx.EVT_RIGHT_UP, self._mouse_right_up)
        self.Bind(wx.EVT_LEFT_DCLICK, self._mouse_left_dclick)
        self.Bind(wx.EVT_LEAVE_WINDOW, self._mouse_leave)
        if check_move:
            self.Bind(wx.EVT_MOTION, self._mouse_move)
            self.Bind(wx.EVT_MOUSE_CAPTURE_LOST, self._capture_lost)
        if self.kbdproc is not None:
            self.Bind(wx.EVT_KEY_DOWN, self._on_key_down)

    def _get_point(self, event):
        return list(event.GetPosition())

    def _on_key_down(self, event):
        key_code = event.GetKeyCode()
        raw_code = event.GetRawKeyCode()
        modifiers = event.GetModifiers()
        if self.kbdproc.on_key_down(key_code, raw_code, modifiers):
            event.Skip()

    def capture_mouse(self):
        pass

    def release_mouse(self):
        pass

    def _mouse_leave(self, event):
        self.mouse_leave(self._get_point(event))

    def _mouse_left_down(self, event):
        self.mouse_left_down(self._get_point(event))

    def _mouse_left_up(self, event):
        if not self.click_flag:
            self.click_flag = True
            self.mouse_left_up(self._get_point(event))
            self.click_flag = False

    def _mouse_right_down(self, event):
        self.mouse_right_down(self._get_point(event))

    def _mouse_right_up(self, event):
        self.mouse_right_up(self._get_point(event))

    def _mouse_wheel(self, event):
        self.mouse_wheel(event.GetWheelRotation())

    def _mouse_move(self, event):
        self.mouse_move(self._get_point(event))

    def _capture_lost(self, _event):
        self.capture_lost()

    def _mouse_left_dclick(self, event):
        self.mouse_left_dclick(self._get_point(event))

    def mouse_leave(self, point):
        pass

    def mouse_left_down(self, point):
        pass

    def mouse_left_up(self, point):
        pass

    def mouse_right_down(self, point):
        pass

    def mouse_right_up(self, point):
        pass

    def mouse_wheel(self, val):
        pass

    def mouse_move(self, point):
        pass

    def capture_lost(self):
        pass

    def mouse_left_dclick(self, point):
        pass


class SensitiveDrawableWidget(DrawableWidget, SensitiveWidget):

    def __init__(self, check_move=False, kbdproc=None):
        DrawableWidget.__init__(self)
        SensitiveWidget.__init__(self, check_move, kbdproc)
