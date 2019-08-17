# -*- coding: utf-8 -*-
#
#  Copyright (C) 2013-2018 by Igor E. Novikov
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import wx

from .. import const
from .. import mixins
from .. import panels

from . import entry


class NativeSpin(wx.SpinCtrl, mixins.RangeDataWidgetMixin):
    callback = None
    callback1 = None
    flag = True
    ctxmenu_flag = False

    def __init__(self, parent, value=0, range_val=(0, 1), size=const.DEF_SIZE,
                 width=6, onchange=None, onenter=None, check_focus=True):
        width = 0 if const.IS_GTK3 else width
        width = width + 2 if const.IS_MSW else width
        size = self._set_width(size, width)
        style = wx.SP_ARROW_KEYS | wx.ALIGN_LEFT | wx.TE_PROCESS_ENTER
        wx.SpinCtrl.__init__(self, parent, wx.ID_ANY, '',
                             size=size, style=style)
        self.set_range(range_val)
        self.set_value(value)
        if onchange:
            self.callback = onchange
            self.Bind(wx.EVT_SPINCTRL, self.on_change, self)
        if onenter:
            self.callback1 = onenter
            self.Bind(wx.EVT_TEXT_ENTER, self.on_enter, self)
        if check_focus:
            self.Bind(wx.EVT_KILL_FOCUS, self._entry_lost_focus, self)
            self.Bind(wx.EVT_CONTEXT_MENU, self._ctxmenu, self)

    def on_change(self, *_args):
        if self.callback:
            self.callback()

    def on_enter(self, event):
        if self.callback1:
            self.callback1()
        event.Skip()

    def _ctxmenu(self, event):
        self.ctxmenu_flag = True
        event.Skip()

    def _entry_lost_focus(self, event):
        if not self.flag and not self.ctxmenu_flag:
            self.on_change()
        elif not self.flag and self.ctxmenu_flag:
            self.ctxmenu_flag = False
        event.Skip()

    def get_value(self):
        return int(self.GetValue())

    def set_value(self, value):
        self.SetValue(int(value))


NativeSpinDouble = NativeSpin

if not const.IS_WX2:
    class NativeSpinDouble(wx.SpinCtrlDouble, mixins.RangeDataWidgetMixin):
        callback = None
        callback1 = None
        flag = True
        ctxmenu_flag = False
        digits = 2
        step = 0

        def __init__(
                self, parent, value=0.0, range_val=(0.0, 1.0), step=0.01,
                digits=2, size=const.DEF_SIZE, width=6,
                onchange=None, onenter=None, check_focus=True):

            self.range_val = range_val
            width = 0 if const.IS_GTK3 else width
            width = width + 2 if const.IS_MSW else width
            size = self._set_width(size, width)
            style = wx.SP_ARROW_KEYS | wx.ALIGN_LEFT | wx.TE_PROCESS_ENTER
            wx.SpinCtrlDouble.__init__(self, parent, wx.ID_ANY, '',
                                       size=size, style=style,
                                       min=0, max=100, initial=value, inc=step)
            self.set_range(range_val)
            self.set_value(value)
            self.set_step(step)
            self.set_digits(digits)
            if onchange:
                self.callback = onchange
                self.Bind(wx.EVT_SPINCTRLDOUBLE, self.on_change, self)
            if onenter:
                self.callback1 = onenter
                self.Bind(wx.EVT_TEXT_ENTER, self.on_enter, self)
            if check_focus:
                self.Bind(
                    wx.EVT_KILL_FOCUS, self._entry_lost_focus, self)
                self.Bind(wx.EVT_CONTEXT_MENU, self._ctxmenu, self)

        def set_step(self, step):
            self.step = step
            self.SetIncrement(step)

        def set_digits(self, digits):
            self.digits = digits
            self.SetDigits(digits)

        def _set_digits(self, digits):
            self.set_digits(digits)

        def on_change(self, *_args):
            if self.callback:
                self.callback()

        def on_enter(self, event):
            if self.callback1:
                self.callback1()
            event.Skip()

        def _ctxmenu(self, event):
            self.ctxmenu_flag = True
            event.Skip()

        def _entry_lost_focus(self, event):
            if not self.flag and not self.ctxmenu_flag:
                self.on_change()
            elif not self.flag and self.ctxmenu_flag:
                self.ctxmenu_flag = False
            event.Skip()

        def get_value(self):
            return float(self.GetValue()) if self.digits \
                else int(self.GetValue())

        def set_value(self, value):
            self.SetValue(float(value) if self.digits else int(value))


class NativeSpinButton(wx.SpinButton, mixins.RangeDataWidgetMixin):
    def __init__(
            self, parent, value=0, range_val=(0, 10), size=const.DEF_SIZE,
            onchange=None, vertical=True):
        self.range_val = range_val
        style = wx.SL_VERTICAL
        if not vertical:
            style = wx.SL_HORIZONTAL
        wx.SpinButton.__init__(self, parent, wx.ID_ANY, size=size, style=style)
        self.SetValue(value)
        self.SetRange(*range_val)
        if onchange:
            self.Bind(wx.EVT_SPIN, onchange, self)


class DummyEvent(object):
    def Skip(self): pass


_dummy_event = DummyEvent()


class _MBtn(panels.Panel, mixins.SensitiveDrawableWidget):
    _pressed = False
    _enabled = True
    _active = True
    _top = True
    parent = None
    callback = None
    callback_wheel = None
    points = None

    def __init__(self, parent, size, top=True, onclick=None, onwheel=None):
        self._top = top
        self.callback = onclick
        self.callback_wheel = onwheel
        self.parent = parent
        panels.Panel.__init__(self, parent, wx.ID_ANY)
        mixins.SensitiveDrawableWidget.__init__(self)
        self.set_size(size)
        self.points = self._get_points()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self._repeat_on_timer)

    def _get_points(self):
        w, h = self.GetSizeTuple()
        mx = 6
        my = h // 2 + 4
        s = 3
        points = [(mx - s, my), (mx + s, my), (mx, my - s), (mx - s, my)]
        if not self._top:
            my = h // 2 - 4
            points = [(mx - s, my), (mx + s, my), (mx, my + s), (mx - s, my)]
        return points

    def _repeat_on_timer(self, _event):
        if self._pressed and self._enabled:
            self.btn_down()
            self.refresh()
        else:
            if self.timer.IsRunning():
                self.timer.Stop()

    def set_enable(self, value):
        self._enabled = value
        self._pressed = False if not value else self._pressed
        self.refresh()

    def get_enabled(self):
        return self._enabled

    def set_active(self, value):
        self._active = value
        self._pressed = False if not value else self._pressed
        self.refresh()

    def get_active(self):
        return self._active

    def mouse_left_down(self, point):
        if self._enabled:
            self._pressed = True
            self.btn_down()
        self.timer.Start(200)
        self.refresh()

    def mouse_left_up(self, point):
        self._pressed = False
        self.refresh()

    def mouse_wheel(self, val):
        if self.callback_wheel and self._enabled:
            self.callback_wheel(val)

    def btn_down(self):
        if self.callback:
            self.callback()

    def paint(self):
        w, h = self.GetSizeTuple()
        x = -20
        y = 0 if self._top else -h
        flag = wx.CONTROL_DIRTY
        if self._pressed and self._enabled:
            flag = wx.CONTROL_PRESSED | wx.CONTROL_SELECTED
        elif not self._enabled:
            flag = wx.CONTROL_DIRTY | wx.CONTROL_DISABLED

        # Draw button bg
        self.set_stroke()
        self.set_fill(const.UI_COLORS['bg'])
        self.draw_rounded_rect(x, y, w - x, 2 * h, 3)

        # Draw button
        nr = wx.RendererNative.Get()
        nr.DrawPushButton(self, self.pdc, (x, y, w - x, 2 * h), flag)

        # Drawing signs
        self.set_gc_stroke()
        self.set_gc_fill(const.UI_COLORS['text']
                         if self._enabled and self._active
                         else const.UI_COLORS['disabled_text'])
        self.gc_draw_polygon(self.points)


class MegaSpinButton(panels.Panel):
    enabled = True
    width = 14

    def __init__(self, parent, value=0, range_val=(0, 10), size=const.DEF_SIZE,
                 onchange=None, vertical=True):
        self.range_val = range_val
        self.value = value
        self.callback = onchange
        size = (self.width, 20) if size == const.DEF_SIZE \
            else (self.width, size[1])
        panels.Panel.__init__(self, parent, wx.ID_ANY)
        self.set_size(size)
        w, h = size
        my = h // 2
        self.top_btn = _MBtn(self, (w, my),
                             onclick=self._top_btn_down,
                             onwheel=self._mouse_wheel)
        self.top_btn.SetPosition((0, 0))
        self.bottom_btn = _MBtn(self, (w, h - my), False,
                                onclick=self._bottom_btn_down,
                                onwheel=self._mouse_wheel)
        self.bottom_btn.SetPosition((0, my))
        self._check_range()

    def Enable(self, val):
        self.enabled = val
        self.top_btn.set_enable(val)
        self.bottom_btn.set_enable(val)

    def get_value(self):
        return self.value

    def set_value(self, val):
        self.value = val
        self._check_range()

    def set_range(self, range_val):
        self.range_val = range_val
        self._check_range()

    def _check_range(self):
        if self.value == self.range_val[0]:
            self.bottom_btn.set_active(False)
        elif not self.bottom_btn.get_active():
            self.bottom_btn.set_active(True)
        if self.value == self.range_val[1]:
            self.top_btn.set_active(False)
        elif not self.top_btn.get_active():
            self.top_btn.set_active(True)

    def _mouse_wheel(self, val):
        if not self.enabled:
            return
        if val < 0:
            self._bottom_btn_down()
        else:
            self._top_btn_down()

    def _top_btn_down(self):
        if self.value < self.range_val[1]:
            self.value += 1
            if self.callback:
                self.callback(_dummy_event)
        self._check_range()

    def _bottom_btn_down(self):
        if self.value > self.range_val[0]:
            self.value -= 1
            if self.callback:
                self.callback(_dummy_event)
        self._check_range()


if const.IS_GTK3:
    SpinButton = MegaSpinButton
else:
    SpinButton = NativeSpinButton


class MegaSpinDouble(wx.Panel, mixins.RangeDataWidgetMixin):
    entry = None
    sb = None
    line = None

    flag = True
    ctxmenu_flag = False
    value = 0.0
    range_val = (0.0, 1.0)
    step = 0.01
    digits = 2
    callback = None
    enter_callback = None

    def __init__(
            self, parent, value=0.0, range_val=(0.0, 1.0), step=0.01,
            digits=2, size=const.DEF_SIZE, width=5,
            onchange=None, onenter=None, check_focus=True):

        self.callback = onchange
        self.enter_callback = onenter
        spin_overlay = const.SPIN['overlay']
        spin_sep = const.SPIN['sep']
        if const.IS_MAC:
            spin_overlay = False
        if not width and const.IS_MSW:
            width = 5

        wx.Panel.__init__(self, parent)
        if spin_overlay:
            if const.IS_GTK:
                self.entry = entry.Entry(
                    self, '', size=size, width=width,
                    onchange=self._check_entry, onenter=self._entry_enter)
                size = (-1, self.entry.GetSize()[1])
                self.entry.SetPosition((0, 0))
                self.sb = SpinButton(self, size=size, onchange=self._check_spin)
                w_pos = self.entry.GetSize()[0] - 5
                if spin_sep:
                    self.line = panels.HPanel(self)
                    self.line.SetSize((1, self.sb.GetSize()[1] - 2))
                    self.line.set_bg(const.UI_COLORS['border'])
                    self.line.SetPosition((w_pos - 1, 1))
                self.sb.SetPosition((w_pos, 0))
                self.SetSize((-1, self.entry.GetSize()[1]))
            elif const.IS_MSW:
                width += 2
                self.entry = entry.Entry(
                    self, '', size=size, width=width,
                    onchange=self._check_entry, onenter=self._entry_enter)
                size = (-1, self.entry.GetSize()[1] - 3)
                self.sb = SpinButton(
                    self.entry, size=size, onchange=self._check_spin)
                w_pos = self.entry.GetSize()[0] - self.sb.GetSize()[0] - 3
                self.sb.SetPosition((w_pos, 0))
                w, h = self.entry.GetSize()
                self.entry.SetSize((w, h + 1))

        else:
            self.box = wx.BoxSizer(const.HORIZONTAL)
            self.SetSizer(self.box)
            self.entry = entry.Entry(
                self, '', size=size, width=width,
                onchange=self._check_entry, onenter=self._entry_enter)
            self.box.Add(self.entry, 0, wx.ALL)
            size = (-1, self.entry.GetSize()[1])
            self.sb = SpinButton(self, size=size, onchange=self._check_spin)
            self.box.Add(self.sb, 0, wx.ALL)

        if check_focus:
            self.entry.Bind(
                wx.EVT_KILL_FOCUS, self._entry_lost_focus, self.entry)
            self.entry.Bind(wx.EVT_CONTEXT_MENU, self._ctxmenu, self.entry)

        self.set_step(step)
        self.set_range(range_val)
        self._set_digits(digits)
        self._set_value(value)
        self.flag = False
        self.Fit()
        self.Bind(wx.EVT_MOUSEWHEEL, self._mouse_wheel)

    def set_enable(self, val):
        self.entry.Enable(val)
        self.sb.Enable(val)
        if self.line:
            color = const.UI_COLORS['border'] if val \
                else const.UI_COLORS['disabled_text']
            self.line.set_bg(color)

    def get_enabled(self):
        return self.entry.IsEnabled()

    def _check_spin(self, event):
        if self.flag:
            return
        coef = pow(10, self.digits)
        dval = float(self.sb.get_value() - int(self.value * coef))
        if not self.value == self._calc_entry():
            self._set_value(self._calc_entry())
        self.SetValue(dval * self.step + self.value)
        event.Skip()

    def _entry_enter(self):
        if self.flag:
            return
        self.SetValue(self._calc_entry())
        if self.enter_callback:
            self.enter_callback()

    def _mouse_wheel(self, event):
        if self.get_enabled():
            if event.GetWheelRotation() < 0:
                self.SetValue(self._calc_entry() - self.step)
            else:
                self.SetValue(self._calc_entry() + self.step)

    def _ctxmenu(self, event):
        self.ctxmenu_flag = True
        event.Skip()

    def _entry_lost_focus(self, event):
        if not self.flag and not self.ctxmenu_flag:
            self.SetValue(self._calc_entry())
        elif not self.flag and self.ctxmenu_flag:
            self.ctxmenu_flag = False
        event.Skip()

    def _check_entry(self):
        if not self.flag:
            value = self.entry.get_value()
            chars = '.0123456789+-*/' if self.digits else '0123456789+-*/'
            result = ''.join([item for item in value if item in chars])
            if not value == result:
                self.flag = True
                self.entry.set_value(result)
                self.flag = False

    def _calc_entry(self):
        txt = self.entry.get_value()
        val = 0
        # noinspection PyBroadException
        try:
            line = 'val=' + txt
            code = compile(line, '<string>', 'exec')
            exec code
        except Exception:
            return self.value
        return val

    def _check_in_range(self, val):
        minval, maxval = self.range_val
        if val < minval:
            val = minval
        if val > maxval:
            val = maxval
        coef = pow(10, self.digits)
        val = round(val * coef) / coef
        return val

    def _set_value(self, val):
        coef = pow(10, self.digits)
        self.value = self._check_in_range(val)
        if not self.digits:
            self.value = int(self.value)
        self.entry.set_value(str(self.value))
        self.sb.set_value(int(self.value * coef))

    def _set_digits(self, digits):
        self.digits = digits
        self.set_range(self.range_val)

    def set_value(self, val):
        self.flag = True
        self._set_value(val)
        self.flag = False

    # ----- Native API emulation
    def SetValue(self, val):
        self.flag = True
        old_value = self.value
        self._set_value(val)
        self.flag = False
        if self.callback is not None and not self.value == old_value:
            self.callback()

    def GetValue(self):
        if not self.value == self._calc_entry():
            self._set_value(self._calc_entry())
        return self.value

    def SetRange(self, minval, maxval):
        coef = pow(10, self.digits)
        self.range_val = (minval, maxval)
        self.sb.set_range((int(minval * coef), int(maxval * coef)))

    # ----- Control API
    def set_step(self, step):
        self.step = step

    def set_digits(self, digits):
        self._set_digits(digits)
        self.SetValue(self.value)


class MegaSpin(MegaSpinDouble):
    def __init__(self, parent, value=0, range_val=(0, 1), size=const.DEF_SIZE,
                 width=5, onchange=None, onenter=None, check_focus=True):
        MegaSpinDouble.__init__(self, parent, value, range_val, 1, 0, size,
                                width, onchange, onenter, check_focus)

    def set_digits(self, digits):
        pass


IntSpin = MegaSpin
FloatSpin = MegaSpinDouble
