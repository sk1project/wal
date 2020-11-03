# -*- coding: utf-8 -*-
#
#  Copyright (C) 2018 by Ihor E. Novikov
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
from .. import utils


def get_accelerator_entry(*args):
    return wx.AcceleratorEntry(*args)


class Menu(wx.Menu):
    def __init__(self):
        wx.Menu.__init__(self)

    def append_menu(self, item_id, text, menu):
        if const.IS_WX4:
            self.Append(item_id, utils.tr(text), menu)
        else:
            self.AppendMenu(item_id, utils.tr(text), menu)

    def remove_item(self, item):
        if const.IS_WX4:
            self.Remove(item)
        else:
            self.RemoveItem(item)

    def append_item(self, item):
        if const.IS_WX4:
            self.Append(item)
        else:
            self.AppendItem(item)

    def append_separator(self):
        return self.AppendSeparator()


class MenuItem(wx.MenuItem):
    def __init__(self, parent, action_id, text, checkable=False):
        if not const.IS_WX4:
            wx.MenuItem.__init__(self, parent, action_id, text=utils.tr(text))
        else:
            kind = wx.ITEM_CHECK if checkable else wx.ITEM_NORMAL
            wx.MenuItem.__init__(self, parent, action_id, text=utils.tr(text), kind=kind)

    @staticmethod
    def bind_to(mw, callback, action_id):
        mw.Bind(wx.EVT_MENU, callback, id=action_id)

    def get_enable(self):
        return self.IsEnabled()

    def set_enable(self, enabled):
        self.Enable(enabled)

    def set_checkable(self, val):
        if not const.IS_WX4:
            self.SetCheckable(val)

    def is_checked(self):
        return self.IsChecked()

    def is_checkable(self):
        return self.IsCheckable()

    def set_bitmap(self, bmp):
        if bmp and not const.IS_MAC:
            self.SetBitmap(bmp)

    def toggle(self):
        if not const.IS_WX4:
            self.Toggle()
        else:
            self.Check(not self.is_checked())

    def set_active(self, val):
        if self.is_checkable() and self.is_checked() != val:
            self.toggle()

    def is_separator(self):
        return self.IsSeparator()


class MenuBar(wx.MenuBar):
    def __init__(self):
        wx.MenuBar.__init__(self)

    def append_menu(self, _menu_id, txt, menu):
        self.Append(menu, utils.tr(txt))
