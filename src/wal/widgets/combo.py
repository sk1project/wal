# -*- coding: utf-8 -*-
#
#  Copyright (C) 2019 by Ihor E. Novikov
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
import wx.combo

from .. import const
from .. import mixins
from .. import utils


class Combolist(wx.Choice, mixins.WidgetMixin):
    items = []
    callback = None

    def __init__(self, parent, size=const.DEF_SIZE, width=0,
                 items=None, onchange=None):
        items = items or []
        self.items = [utils.tr(item) for item in items]
        size = self._set_width(size, width)
        wx.Choice.__init__(self, parent, wx.ID_ANY, size, choices=self.items)
        if onchange:
            self.callback = onchange
            self.Bind(wx.EVT_CHOICE, self.on_change, self)
        if const.IS_GTK3:
            self.Bind(wx.EVT_UPDATE_UI, self._on_show)

    def _on_show(self, *_args):
        self.InvalidateBestSize()
        self.SetSize(self.BestSize)

    def on_change(self, _event):
        if self.callback:
            self.callback()

    def set_items(self, items):
        self.items = [utils.tr(item) for item in items]
        self.SetItems(self.items)

    def set_selection(self, index):
        if index < self.GetCount():
            self.SetSelection(index)

    def get_selection(self):
        return self.GetSelection()

    def set_active(self, index):
        self.set_selection(index)

    def get_active(self):
        return self.get_selection()

    def get_active_value(self):
        return utils.untr(self.items[self.get_selection()])

    def set_active_value(self, val):
        val = utils.tr(val)
        if val not in self.items:
            self.items.append(val)
            self.SetItems(self.items)
        self.set_active(self.items.index[val])


class BitmapChoice(wx.combo.OwnerDrawnComboBox, mixins.WidgetMixin):
    def __init__(self, parent, value=0, bitmaps=None):
        self.bitmaps = bitmaps or []
        choices = self._create_items()
        x, y = self.bitmaps[0].GetSize()
        x += 4
        y += 7 + 3
        wx.combo.OwnerDrawnComboBox.__init__(
            self, parent, wx.ID_ANY,
            wx.EmptyString, wx.DefaultPosition,
            (x, y), choices, wx.CB_READONLY,
            wx.DefaultValidator)
        self.set_active(value)

    def OnDrawItem(self, dc, rect, item, flags):
        if item == wx.NOT_FOUND:
            return
        x, y, w, h = wx.Rect(*rect).Get()
        if flags & wx.combo.ODCB_PAINTING_SELECTED and \
                flags & wx.combo.ODCB_PAINTING_CONTROL:
            dc.SetBrush(wx.Brush(wx.WHITE))
            dc.DrawRectangle(x - 1, y - 1, w + 2, h + 2)
            bitmap = self.bitmaps[item]
        elif flags & wx.combo.ODCB_PAINTING_SELECTED:
            if const.IS_MSW:
                pdc = wx.PaintDC(self)
                pdc.SetPen(wx.TRANSPARENT_PEN)
                pdc.SetBrush(wx.Brush(
                    wx.Colour(*const.UI_COLORS['selected_text_bg'])))
                pdc.DrawRectangle(x, y, w, h)
            else:
                render = wx.RendererNative.Get()
                render.DrawItemSelectionRect(self, dc, rect,
                                             wx.CONTROL_SELECTED)
            bitmap = utils.bmp_to_white(self.bitmaps[item])
        else:
            bitmap = self.bitmaps[item]
        dc.DrawBitmap(bitmap, x + 2, y + 4, True)

    def OnMeasureItem(self, item):
        return 1 if item == wx.NOT_FOUND \
            else self.bitmaps[item].GetSize()[1] + 7

    def OnMeasureItemWidth(self, item):
        return 1 if item == wx.NOT_FOUND \
            else self.bitmaps[item].GetSize()[0] - 4

    def _create_items(self):
        return [str(item) for item in range(len(self.bitmaps))]

    def set_bitmaps(self, bitmaps):
        self.bitmaps = bitmaps
        self.SetItems(self._create_items())

    def set_items(self, items):
        self.SetItems(items)

    def set_selection(self, index):
        if index < self.GetCount():
            self.SetSelection(index)

    def get_selection(self):
        return self.GetSelection()

    def set_active(self, index):
        self.set_selection(index)

    def get_active(self):
        return self.get_selection()


class Combobox(wx.ComboBox, mixins.DataWidgetMixin):
    items = None
    callback = None
    flag = False

    def __init__(self, parent, value='', pos=(-1, 1), size=const.DEF_SIZE,
                 width=0, items=None, onchange=None):
        items = items or []
        self.items = [utils.tr(item) for item in items]
        flags = wx.CB_DROPDOWN | wx.TE_PROCESS_ENTER
        size = self._set_width(size, width)
        wx.ComboBox.__init__(self, parent, wx.ID_ANY, value,
                             pos, size, items, flags)
        if onchange:
            self.callback = onchange
            self.Bind(wx.EVT_COMBOBOX, self.on_change, self)
            self.Bind(wx.EVT_TEXT_ENTER, self.on_enter, self)
        self.Bind(wx.EVT_TEXT, self.on_typing, self)

    def on_typing(self, event):
        event.Skip()

    def on_change(self, event):
        if self.flag:
            return
        if self.callback:
            self.callback()
        event.Skip()

    def on_enter(self, event):
        if self.flag:
            return
        if self.callback:
            self.callback()
        event.Skip()

    def set_items(self, items):
        self.items = [utils.tr(item) for item in items]
        self.SetItems(self.items)


class FloatCombobox(Combobox):
    digits = 0

    def __init__(self, parent, value='', width=5, digits=1,
                 items=None, onchange=None):
        items = items or []
        vals = [str(item) for item in items]
        Combobox.__init__(self, parent, str(value), width=width,
                          items=vals, onchange=onchange)
        self.digits = digits

    def on_typing(self, event):
        if self.flag:
            return
        txt = Combobox.get_value(self)
        res = ''
        for item in txt:
            chars = '.0123456789'
            if not self.digits:
                chars = '0123456789'
            if item in chars:
                res += item
        if not txt == res:
            self.flag = True
            Combobox.set_value(self, res)
            self.flag = False
        event.Skip()

    def get_value(self):
        val = Combobox.get_value(self) or 1
        return float(val) if self.digits else int(val)

    def set_value(self, val):
        val = str(val)
        if not val == Combobox.get_value(self):
            Combobox.set_value(self, val)

    def set_items(self, items):
        self.SetItems([str(item) for item in items])
