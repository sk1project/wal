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
from .. import renderer
from .. import utils


class Button(wx.Button, mixins.WidgetMixin):
    callback = None

    def __init__(self, parent, text, size=const.DEF_SIZE, onclick=None,
                 tooltip='', default=False, pid=wx.ID_ANY):
        wx.Button.__init__(self, parent, pid, utils.tr(text), size=size)
        if default:
            self.SetDefault()
        if onclick:
            self.callback = onclick
            self.Bind(wx.EVT_BUTTON, self.on_click, self)
        if tooltip:
            self.SetToolTipString(tooltip)

    def set_default(self):
        self.SetDefault()

    def on_click(self, _event=None):
        if self.callback:
            self.callback()


class ColorButton(wx.ColourPickerCtrl, mixins.WidgetMixin):
    callback = None
    silent = True

    def __init__(self, parent, color=(), onchange=None, silent=True):
        self.silent = silent
        if not color:
            color = const.BLACK
        elif isinstance(color, str):
            color = wx.Colour(*self.hex_to_val255(color))
        else:
            color = wx.Colour(*self.val255(color))
        wx.ColourPickerCtrl.__init__(self, parent, wx.ID_ANY, color)
        if onchange:
            self.callback = onchange
            self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.on_change, self)

    def on_change(self, _event):
        if self.callback:
            self.callback()

    @staticmethod
    def hex_to_val255(hexcolor):
        return tuple(int(hexcolor[a:b], 0x10)
                     for a, b in ((1, 3), (3, 5), (5, -1)))

    @staticmethod
    def val255(vals):
        return tuple(int(item * 255) for item in vals)

    @staticmethod
    def val255_to_dec(vals):
        return tuple(item / 255.0 for item in vals)

    def set_value(self, color):
        self.SetColour(wx.Colour(*self.val255(color)))
        if not self.silent:
            self.on_change(None)

    def set_value255(self, color):
        self.SetColour(wx.Colour(*color))
        if not self.silent:
            self.on_change(None)

    def get_value(self):
        return self.val255_to_dec(self.GetColour().Get())

    def get_value255(self):
        return self.GetColour().Get()


class ImageButton(mixins.GenericGWidget):
    def __init__(
            self, parent, art_id=None, art_size=const.DEF_SIZE,
            text='', tooltip='', padding=0, decoration_padding=6,
            flat=True, native=True,
            fontbold=False, fontsize=0, textplace=const.RIGHT,
            onclick=None, repeat=False):

        self.flat = flat
        self.decoration_padding = decoration_padding

        mixins.GenericGWidget.__init__(self, parent, tooltip, onclick, repeat)

        if native:
            rndr = renderer.NativeButtonRenderer
        else:
            rndr = renderer.ButtonRenderer

        self.renderer = rndr(
            self, art_id, art_size, text,
            padding, fontbold, fontsize, textplace)

    def _on_paint(self, event):
        if self.enabled:
            if not self.mouse_over:
                self.renderer.draw_normal(self.flat)
            else:
                if self.mouse_pressed:
                    self.renderer.draw_pressed()
                else:
                    self.renderer.draw_hover()
        else:
            self.renderer.draw_disabled(self.flat)
