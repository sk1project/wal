# -*- coding: utf-8 -*-
#
# 	Copyright (C) 2013 by Ihor E. Novikov
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


def _dialog(parent, title, text, icon, yesno=False, cancel=False):
    if any([yesno, cancel]):
        buttons = wx.YES_NO if yesno else 0
        if cancel:
            buttons = buttons | wx.CANCEL if buttons else wx.OK | wx.CANCEL
    else:
        buttons = wx.OK
    dlg = wx.MessageDialog(parent, text, title, icon | buttons)
    ret = dlg.ShowModal()
    dlg.Destroy()
    return ret


def msg_dialog(parent, title, text):
    _dialog(parent, title, text, wx.ICON_INFORMATION)


def error_dialog(parent, title, text):
    _dialog(parent, title, text, wx.ICON_ERROR)


def stop_dialog(parent, title, text):
    _dialog(parent, title, text, wx.ICON_STOP)


def yesno_dialog(parent, title, text):
    return _dialog(
        parent, title, text, wx.ICON_WARNING, True, False) == wx.ID_YES


def ync_dialog(parent, title, text):
    return {wx.ID_YES: True,
            wx.ID_NO: False,
            }.get(_dialog(parent, title, text, wx.ICON_WARNING, True, True))
