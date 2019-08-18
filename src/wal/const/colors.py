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

from . import sysconst


def mix_colors(fg, bg, alpha):
    r1, g1, b1 = fg[:3]
    r2, g2, b2 = bg[:3]
    a1 = alpha / 255.0
    a2 = 1.0 - a1
    r = int(r1 * a1 + r2 * a2)
    b = int(b1 * a1 + b2 * a2)
    g = int(g1 * a1 + g2 * a2)
    return r, g, b


def lighter_color(color, coef):
    white = (255, 255, 255)
    return mix_colors(color, white, coef * 255.0)


def get_sys_color(color_const):
    return wx.SystemSettings_GetColour(color_const).Get()


UI_COLORS = {}

WHITE = wx.Colour(255, 255, 255)
BLACK = wx.Colour(0, 0, 0)
DARK_GRAY = wx.Colour(89, 89, 89)
GRAY = wx.Colour(129, 134, 134)
LIGHT_GRAY = wx.Colour(240, 240, 240)
RED = wx.Colour(255, 0, 0)
DARK_RED = wx.Colour(230, 50, 50)
BROWN = wx.Colour(145, 45, 45)
GREEN = wx.Colour(0, 255, 0)
BLUE = wx.Colour(0, 0, 255)
AMBIANCE_GRAY = wx.Colour(60, 59, 55)


def set_ui_colors(kw):
    kw['fg'] = get_sys_color(wx.SYS_COLOUR_BTNTEXT)
    kw['bg'] = get_sys_color(wx.SYS_COLOUR_3DFACE)
    kw['border'] = get_sys_color(wx.SYS_COLOUR_BTNSHADOW)
    kw['text'] = get_sys_color(wx.SYS_COLOUR_BTNTEXT)
    kw['entry_bg'] = get_sys_color(wx.SYS_COLOUR_WINDOW)
    kw['selected_text'] = get_sys_color(wx.SYS_COLOUR_HIGHLIGHTTEXT)
    kw['selected_text_bg'] = get_sys_color(wx.SYS_COLOUR_ACTIVECAPTION) \
        if sysconst.IS_GTK2 else get_sys_color(wx.SYS_COLOUR_HIGHLIGHT)
    kw['disabled_text'] = get_sys_color(wx.SYS_COLOUR_GRAYTEXT)
    kw['workspace'] = get_sys_color(wx.SYS_COLOUR_APPWORKSPACE)
    kw['tooltip'] = get_sys_color(wx.SYS_COLOUR_INFOBK)
    list_bg = get_sys_color(wx.SYS_COLOUR_LISTBOX)
    kw['list_bg'] = list_bg
    kw['even'] = mix_colors((0, 0, 0), list_bg, 15)
    kw['odd'] = mix_colors((255, 255, 255), list_bg, 15)
    kw['3dlight'] = get_sys_color(wx.SYS_COLOUR_3DLIGHT)


def get_sel_bg():
    return get_sys_color(wx.SYS_COLOUR_ACTIVECAPTION) \
        if sysconst.IS_GTK2 else get_sys_color(wx.SYS_COLOUR_HIGHLIGHT)
