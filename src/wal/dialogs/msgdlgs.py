# -*- coding: utf-8 -*-
#
# 	Copyright (C) 2013-2020 by Ihor E. Novikov
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

import typing as tp
import wx


def _dialog(parent: wx.Window, title: str, text: str, icon: int, yesno: bool = False, cancel: bool = False) -> int:
    """Shows predefined dialog

    :param parent: (wx.Window) parent window
    :param title: (str) dialog title
    :param text: (str) dialog text
    :param icon: (int) icon type
    :param yesno: (bool) yes|no buttons flag
    :param cancel: (bool) cancel button flag
    :return: (int) wx return value
    """
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


def msg_dialog(parent: wx.Window, title: str, text: str) -> None:
    """Shows message dialog with info icon

    :param parent: (wx.Window) parent window
    :param title: (str) dialog title
    :param text: (str) dialog text
    """
    _dialog(parent, title, text, wx.ICON_INFORMATION)


def error_dialog(parent: wx.Window, title: str, text: str) -> None:
    """Shows error dialog with error icon

    :param parent: (wx.Window) parent window
    :param title: (str) dialog title
    :param text: (str) dialog text
    """
    _dialog(parent, title, text, wx.ICON_ERROR)


def stop_dialog(parent: wx.Window, title: str, text: str) -> None:
    """Shows stop dialog with stop icon

    :param parent: (wx.Window) parent window
    :param title: (str) dialog title
    :param text: (str) dialog text
    """
    _dialog(parent, title, text, wx.ICON_STOP)


def yesno_dialog(parent: wx.Window, title: str, text: str) -> bool:
    """Shows Yes-No dialog

    :param parent: (wx.Window) parent window
    :param title: (str) dialog title
    :param text: (str) dialog text
    :return: (bool) yes|no result
    """
    return _dialog(parent, title, text, wx.ICON_WARNING, True, False) == wx.ID_YES


def ync_dialog(parent: wx.Window, title: str, text: str) -> tp.Optional[bool]:
    """Shows Yes-No dialog

    :param parent: (wx.Window) parent window
    :param title: (str) dialog title
    :param text: (str) dialog text
    :return: (bool) yes|no result
    """
    return {wx.ID_YES: True, wx.ID_NO: False}.get(_dialog(parent, title, text, wx.ICON_WARNING, True, True))
