# -*- coding: utf-8 -*-
#
#  Copyright (C) 2013-2018 by Ihor E. Novikov
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

import os
import platform
import wx

MSW = '__WXMSW__'
GTK = '__WXGTK__'
MAC = '__WXMAC__'

VERSION = wx.version()
IS_MAC = wx.Platform == MAC
IS_MSW = wx.Platform == MSW
IS_WINXP = IS_MSW and platform.release() == 'XP'
IS_WIN7 = IS_MSW and platform.release() == '7'
IS_WIN10 = IS_MSW and platform.release() == '10'
IS_GTK = wx.Platform == GTK
IS_GTK2 = IS_GTK and 'gtk2' in VERSION
IS_GTK3 = IS_GTK and 'gtk3' in VERSION
IS_WX2 = wx.VERSION[0] == 2
IS_WX3 = wx.VERSION[0] == 3
IS_WX4 = wx.VERSION[0] == 4


def _get_desktop_name():
    if IS_GTK and 'XDG_CURRENT_DESKTOP' in os.environ:
        return os.environ['XDG_CURRENT_DESKTOP']
    return None


DESKTOP_NAME = _get_desktop_name()
IS_UNITY = DESKTOP_NAME == 'Unity'


def is_unity_16_04():
    if IS_GTK:
        if platform.dist()[0] == 'Ubuntu' and platform.dist()[1]:
            return IS_UNITY and int(platform.dist()[1].split('.')[0]) >= 16
    return False


def get_theme_name():
    if IS_GTK:
        cmd = "gsettings get org.gnome.desktop.interface gtk-theme"
        return os.environ.get('GTK_THEME') or \
            os.popen(cmd).readline().strip().strip('\'') or None


IS_UNITY_16 = is_unity_16_04()
IS_AMBIANCE = get_theme_name() == 'Ambiance'
