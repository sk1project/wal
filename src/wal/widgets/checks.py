# -*- coding: utf-8 -*-
#
#  Copyright (C) 2019 by Igor E. Novikov
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
from .. import utils


class Checkbox(wx.CheckBox, mixins.DataWidgetMixin):
    callback = None

    def __init__(self, parent, text='', value=False, onclick=None, right=False):
        style = wx.ALIGN_RIGHT if right else 0
        wx.CheckBox.__init__(
            self, parent, wx.ID_ANY, utils.tr(text), style=style)
        self.SetValue(True if value else False)
        if onclick:
            self.callback = onclick
            self.Bind(wx.EVT_CHECKBOX, self.on_click, self)

    def set_value(self, val, action=True):
        self.SetValue(val)
        if action:
            self.on_click()

    def on_click(self, _event=None):
        if self.callback:
            self.callback()


SWITCH_SIZE = (76, 26)


class Switch(panels.VPanel, panels.SensitiveCanvas):
    state = False
    callback = None

    def __init__(self, parent, value=False, onclick=None):
        self.state = bool(value)
        self.callback = onclick
        panels.VPanel.__init__(self, parent)
        panels.SensitiveCanvas.__init__(self)
        self.pack(SWITCH_SIZE)

    def mouse_left_up(self, _point):
        self.state = not self.state
        self.refresh()
        if self.callback:
            self.callback()

    def get_value(self):
        return self.state

    def set_value(self, value, action=True):
        self.state = bool(value)
        if action:
            self.on_click()

    def on_click(self, _event=None):
        if self.callback:
            self.callback()

    def paint(self):
        on_color = const.UI_COLORS['selected_text_bg']
        off_color = const.UI_COLORS['dark_shadow']
        border_color = const.UI_COLORS['workspace']
        bg_color = const.UI_COLORS['bg']
        on_text_color = const.UI_COLORS['selected_text']
        off_text_color = const.UI_COLORS['text']

        w, h = self.get_size()

        # Light shadow
        self.set_gc_stroke()
        self.set_gc_fill(color=const.WHITE)
        self.gc_draw_rounded_rect(w=w, h=h, radius=2)
        # Background
        self.set_gc_fill(color=on_color if self.state else off_color)
        self.gc_draw_rounded_rect(w=w, h=h - 1, radius=2)
        # Background shadow
        rect = (1, 1, w - 2, h - 3)
        start_color = const.WHITE.Get() + (0,)
        stop_color = const.WHITE.Get() + (55,)
        self.gc_draw_linear_gradient(rect, start_color, stop_color, True)
        # Border
        self.set_gc_fill()
        self.set_gc_stroke(color=border_color, width=1)
        self.gc_draw_rounded_rect(w=w, h=h - 1, radius=2)
        # Button
        self.set_gc_stroke(color=border_color, width=1)
        self.set_gc_fill(color=bg_color)
        self.gc_draw_rounded_rect(x=w / 2 if self.state else 2, y=2,
                                  w=w / 2 - 2, h=h - 5, radius=3)
        # Button relief
        rect = (w / 2 + 1 if self.state else 3, 3, w / 2 - 4, h - 7)
        start_color = const.WHITE.Get() + (40,)
        stop_color = const.BLACK.Get() + (40,)
        self.gc_draw_linear_gradient(rect, start_color, stop_color, True)

        # Text
        self.set_gc_font(bold=True, size_incr=-1)
        txt_color = on_text_color if self.state else off_text_color
        self.set_gc_text_color(color=txt_color)
        txt = 'ON' if self.state else 'OFF'
        tw, th = utils.get_text_size(txt, True, -1)
        x = (w if self.state else 3 * w) / 4 - tw / 2
        y = h / 2 - th / 2 - 1
        self.gc_draw_text(txt, x, y)


class NumCheckbox(Checkbox):
    def set_value(self, val, action=True):
        self.SetValue(bool(val))
        if action:
            self.on_click()

    def get_value(self):
        return 1 if self.GetValue() else 0


class Radiobutton(wx.RadioButton, mixins.DataWidgetMixin):
    callback = None

    def __init__(self, parent, text='', onclick=None, group=False):
        style = wx.RB_GROUP if group else 0
        wx.RadioButton.__init__(
            self, parent, wx.ID_ANY, utils.tr(text), style=style)
        if onclick:
            self.callback = onclick
            self.Bind(wx.wx.EVT_RADIOBUTTON, self.on_click, self)

    def on_click(self, _event):
        if self.callback:
            self.callback()
