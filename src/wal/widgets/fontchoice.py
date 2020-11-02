# -*- coding: utf-8 -*-
#
#  Copyright (C) 2016-2018 by Ihor E. Novikov
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
from .. import utils


if const.IS_WX4:
    import wx.adv as adv
else:
    import wx.combo as adv


class FontBitmapChoice(adv.OwnerDrawnComboBox, mixins.WidgetMixin):
    fontnames = None
    bitmaps = None
    sample_bitmaps = None
    font_icon = None
    control_height = 0

    def __init__(self, parent, value=0, size=(10, 30),
                 fontnames=None, fontname_bitmaps=None,
                 fontsample_bitmaps=None, font_icon=None, onchange=None):

        self.fontnames = fontnames or []
        self.bitmaps = fontname_bitmaps or []
        self.sample_bitmaps = fontsample_bitmaps or []
        self.font_icon = font_icon

        self.font = utils.get_default_gui_font()
        self.fontcolor = wx.Colour(*const.UI_COLORS['text'])

        choices = self._create_items()
        x, y = size
        self.control_height = y
        x += 4
        if self.font_icon:
            x += self.font_icon.GetSize()[0]
        y += 7 + 3
        style = wx.CB_READONLY | wx.NO_BORDER if const.IS_GTK3 else wx.CB_READONLY
        adv.OwnerDrawnComboBox.__init__(
            self, parent, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
            (x, y), choices, style, wx.DefaultValidator)
        self._set_active(value)
        self.callback = onchange
        self.Bind(wx.EVT_COMBOBOX, self.on_change, self)

    def on_change(self, _event):
        if self.callback:
            self.callback()

    def OnDrawItem(self, dc, rect, item, flags):
        if item == wx.NOT_FOUND:
            return
        r = wx.Rect(*rect)
        icon_size = (0, 0)
        if self.font_icon:
            icon_size = self.font_icon.GetSize()
        icon_x = r.x + 2
        label_y = r.y + 4
        label_x = icon_x + 4 + icon_size[0]
        icon_y = self.control_height / 2 - icon_size[1] / 2 + label_y
        sample_y = label_y + self.control_height + 2
        if flags & adv.ODCB_PAINTING_SELECTED and not \
                flags & adv.ODCB_PAINTING_CONTROL:
            if const.IS_MSW:
                pdc = wx.PaintDC(self)
                pdc.SetPen(wx.TRANSPARENT_PEN)
                pdc.SetBrush(wx.Brush(
                    wx.Colour(*const.UI_COLORS['selected_text_bg'])))
                pdc.DrawRectangle(*r.Get())
            else:
                render = wx.RendererNative.Get()
                render.DrawItemSelectionRect(self, dc, r, wx.CONTROL_SELECTED)
            if self.font_icon:
                icon = utils.bmp_to_white(self.font_icon)
                dc.DrawBitmap(icon, icon_x, icon_y, True)
            dc.SetTextForeground(wx.WHITE)
            dc.DrawText(self.fontnames[item], label_x, label_y)
            bmp = utils.bmp_to_white(self.sample_bitmaps[item])
            dc.DrawBitmap(bmp, label_x, sample_y, True)
        elif flags & adv.ODCB_PAINTING_CONTROL:
            if const.IS_GTK:
                icon_x += 4
                icon_y += 1
                label_x += 4
                label_y += 1
                pdc = wx.PaintDC(self)
                pdc.SetPen(wx.TRANSPARENT_PEN)
                pdc.SetBrush(wx.Brush(wx.Colour(*const.UI_COLORS['bg'])))
                h = self.get_size()[1]
                w = r.width - 1
                pdc.DrawRectangle(0, 0, r.width, h)
                nr = wx.RendererNative.Get()
                if const.IS_WX4:
                    nr.DrawTextCtrl(self, dc, (0, 0, w, h), wx.CONTROL_FLAT)
                else:
                    nr.DrawTextCtrl(self, dc, (0, 0, w, h), wx.CONTROL_DIRTY)
            if self.font_icon:
                dc.DrawBitmap(self.font_icon, icon_x, icon_y, True)
            dc.SetTextForeground(self.fontcolor)
            dc.DrawText(self.fontnames[item], label_x, label_y)
        else:
            if self.font_icon:
                dc.DrawBitmap(self.font_icon, icon_x, icon_y, True)
            dc.SetTextForeground(self.fontcolor)
            dc.DrawText(self.fontnames[item], label_x, label_y)
            dc.DrawBitmap(self.sample_bitmaps[item], label_x, sample_y, True)
            dc.SetPen(wx.Pen(wx.Colour(240, 240, 240), 1))
            val = sample_y + self.sample_bitmaps[item].GetSize()[1]
            dc.DrawLine(0, val, r.width, val)

    def OnMeasureItem(self, item):
        if item == wx.NOT_FOUND:
            return 1
        val = self.bitmaps[item].GetSize()[1]
        val += self.sample_bitmaps[item].GetSize()[1] + 7
        return val

    def OnMeasureItemWidth(self, item):
        if item == wx.NOT_FOUND:
            return 1
        val = max(self.bitmaps[item].GetSize()[0],
                  self.sample_bitmaps[item].GetSize()[0])
        if self.font_icon:
            val += self.font_icon.GetSize()[0] + 2
        return val - 4

    def _create_items(self):
        return [str(item) for item in range(len(self.fontnames))]

    def _set_bitmaps(self, bitmaps, sample_bitmaps):
        self.bitmaps = bitmaps
        self.sample_bitmaps = sample_bitmaps
        self.SetItems(self._create_items())

    def _set_selection(self, index):
        if index < self.GetCount():
            if const.IS_WX4:
                self.SetSelection(index, index)
            else:
                self.SetSelection(index)

    def _get_selection(self):
        return self.GetSelection()

    def _set_active(self, index):
        self._set_selection(index)

    def _get_active(self):
        return self._get_selection()
