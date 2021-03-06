# -*- coding: utf-8 -*-
#
# 	Copyright (C) 2016 by Ihor E. Novikov
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
from wx.lib.agw.ultimatelistctrl import ULC_VRULES, ULC_HRULES
from wx.lib.agw.ultimatelistctrl import UltimateListCtrl
from wx.lib.agw.ultimatelistctrl import UltimateListItemAttr

from .. import const
from .. import utils

WIDTH = 22


class LayerList(UltimateListCtrl):
    current_item = None
    pos_x = None
    sel_callback = None
    change_callback = None
    double_click_callback = None
    selection_flag = True
    data = None

    def __init__(
            self, parent, data=None, images=None, alt_color=True,
            even_color=None, odd_color=None,
            on_select=None, on_change=None, on_double_click=None):
        data = data or []
        images = images or []
        self.alt_color = alt_color
        self.attr1 = UltimateListItemAttr()
        self.attr1.SetBackgroundColour(
            odd_color or wx.Colour(*const.UI_COLORS['odd']))
        self.attr2 = UltimateListItemAttr()
        self.attr2.SetBackgroundColour(
            even_color or wx.Colour(*const.UI_COLORS['even']))

        self.sel_callback = on_select
        self.change_callback = on_change
        self.double_click_callback = on_double_click

        self.il = wx.ImageList(16, 16)
        index = 0
        for icon_id in images:
            bmp = wx.ArtProvider.GetBitmap(icon_id, wx.ART_OTHER, const.SIZE_16)
            if index > 1:
                if icon_id.endswith('-no.png'):
                    bmp = utils.recolor_bmp(
                        bmp, const.UI_COLORS['disabled_text'])
                else:
                    bmp = utils.recolor_bmp(bmp, const.UI_COLORS['fg'])
            self.il.Add(bmp)
            index += 1

        style = wx.LC_REPORT | wx.LC_VRULES | wx.LC_NO_HEADER
        style |= wx.LC_SINGLE_SEL
        style |= wx.LC_VIRTUAL
        style |= ULC_VRULES | ULC_HRULES | wx.NO_BORDER
        UltimateListCtrl.__init__(self, parent, agwStyle=style)
        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

        for i in range(5):
            self.InsertColumn(i, '')
            self.SetColumnWidth(i, WIDTH)
        self.InsertColumn(5, '')
        self.SetColumnWidth(5, -3)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_mouse_down)
        self.Bind(wx.EVT_LEFT_DCLICK, self.on_double_click)
        self.update(data)
        if data:
            self.set_selected(0)

    def get_selected(self):
        return self.current_item

    def update(self, data=None):
        self.selection_flag = False
        self.data = data or []
        self.SetItemCount(len(self.data))
        self.selection_flag = True

    def set_selected(self, index):
        self.selection_flag = False
        self.Select(index, True)
        self.current_item = index
        self.selection_flag = True

    def on_mouse_down(self, event):
        self.pos_x = event.GetX()
        event.Skip()

    def on_double_click(self, _event):
        if self.double_click_callback:
            self.double_click_callback()

    def OnItemSelected(self, event):
        if not self.selection_flag:
            return
        self.current_item = event.m_itemIndex
        if self.sel_callback:
            self.sel_callback(self.current_item)
        if self.pos_x is not None and self.change_callback:
            column = self.pos_x / WIDTH
            column = 5 if column > 5 else column
            self.change_callback(self.current_item, column)
            self.pos_x = None

    def OnGetItemToolTip(self, item, col):
        return self.data[item][5] if col == 5 else None

    def OnGetItemTextColour(self, item, col):
        return const.UI_COLORS['fg']

    def OnGetItemText(self, item, col):
        return self.data[item][5] if col == 5 else ''

    def OnGetItemImage(self, item):
        return -1

    def OnGetItemAttr(self, item):
        if self.alt_color:
            return self.attr2 if item % 2 else self.attr1
        return None

    def OnGetItemColumnImage(self, item, column=0):
        return [] if column == 5 else [column * 2 + self.data[item][column]]

    def OnGetItemColumnCheck(self, item, column=0):
        return []

    def OnGetItemColumnKind(self, item, column=0):
        return 0

    def OnGetItemKind(self, item):
        return 0
