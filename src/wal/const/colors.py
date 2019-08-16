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


def _init_gtk_colors(kw):
    border = get_sys_color(wx.SYS_COLOUR_BTNSHADOW)
    bg = get_sys_color(wx.SYS_COLOUR_3DFACE)
    fg = get_sys_color(wx.SYS_COLOUR_BTNTEXT)
    infobk = get_sys_color(wx.SYS_COLOUR_INFOBK)
    sel_bg = get_sys_color(wx.SYS_COLOUR_ACTIVECAPTION) \
        if sysconst.IS_GTK2 else get_sys_color(wx.SYS_COLOUR_HIGHLIGHT)
    sel_text = get_sys_color(wx.SYS_COLOUR_HIGHLIGHTTEXT)
    disabled_text = get_sys_color(wx.SYS_COLOUR_GRAYTEXT)
    entry_bg = get_sys_color(wx.SYS_COLOUR_WINDOW)
    kw['fg'] = fg + (255,)
    kw['bg'] = bg + (255,)
    kw['text'] = fg + (255,)
    kw['entry_bg'] = () + entry_bg
    kw['selected_text_bg'] = () + sel_bg
    kw['selected_text'] = () + sel_text
    kw['disabled_text'] = mix_colors(fg, bg, 125)
    kw['disabled_text_shadow'] = mix_colors((255, 255, 255), bg, 200)
    kw['hover_border'] = border + (90,)
    kw['hover_solid_border'] = disabled_text
    kw['pressed_border'] = border + (0,)
    kw['light_shadow'] = mix_colors((255, 255, 255), bg, 40)
    kw['dark_shadow'] = disabled_text
    kw['dark_face'] = border + (40,)
    kw['light_face'] = (255, 255, 255, 60)
    kw['workspace'] = (89, 89, 89)
    kw['tooltip_bg'] = () + infobk


def _init_mac_colors(kw):
    border = get_sys_color(wx.SYS_COLOUR_APPWORKSPACE)
    bg = get_sys_color(wx.SYS_COLOUR_3DFACE)
    fg = get_sys_color(wx.SYS_COLOUR_BTNTEXT)
    ws = get_sys_color(wx.SYS_COLOUR_APPWORKSPACE)
    infobk = get_sys_color(wx.SYS_COLOUR_INFOBK)
    sel_bg = get_sys_color(wx.SYS_COLOUR_HIGHLIGHT)
    sel_text = get_sys_color(wx.SYS_COLOUR_HIGHLIGHTTEXT)
    entry_bg = get_sys_color(wx.SYS_COLOUR_WINDOW)
    kw['fg'] = () + fg
    kw['bg'] = () + bg
    kw['text'] = () + fg
    kw['entry_bg'] = () + entry_bg
    kw['selected_text_bg'] = () + sel_bg
    kw['selected_text'] = () + sel_text
    kw['disabled_text'] = mix_colors(fg, bg, 125)
    kw['disabled_text_shadow'] = (255, 255, 255)
    kw['hover_border'] = border + (90,)
    kw['hover_solid_border'] = border + ()
    kw['pressed_border'] = border + ()
    kw['light_shadow'] = (255, 255, 255, 90)
    kw['dark_shadow'] = border + (40,)
    kw['dark_face'] = border + (40,)
    kw['light_face'] = (255, 255, 255, 60)
    kw['workspace'] = () + ws
    kw['tooltip_bg'] = () + infobk


def _init_msw_colors(kw):
    border = get_sys_color(wx.SYS_COLOUR_BTNSHADOW)
    bg = get_sys_color(wx.SYS_COLOUR_3DFACE)
    fg = get_sys_color(wx.SYS_COLOUR_BTNTEXT)
    ws = get_sys_color(wx.SYS_COLOUR_APPWORKSPACE)
    infobk = get_sys_color(wx.SYS_COLOUR_INFOBK)
    sel_bg = get_sys_color(wx.SYS_COLOUR_HIGHLIGHT)
    sel_text = get_sys_color(wx.SYS_COLOUR_HIGHLIGHTTEXT)
    entry_bg = get_sys_color(wx.SYS_COLOUR_WINDOW)
    kw['fg'] = () + fg
    kw['bg'] = () + bg
    kw['text'] = () + fg
    kw['entry_bg'] = () + entry_bg
    kw['selected_text_bg'] = () + sel_bg
    kw['selected_text'] = () + sel_text
    kw['disabled_text'] = mix_colors(fg, bg, 125)
    kw['disabled_text_shadow'] = mix_colors((255, 255, 255), bg, 200)
    kw['hover_border'] = border + (90,)
    kw['hover_solid_border'] = mix_colors(border, bg, 200)
    kw['pressed_border'] = border + (0,)
    kw['light_shadow'] = (255, 255, 255, 90)
    kw['dark_shadow'] = border + (40,)
    kw['dark_face'] = border + (40,)
    kw['light_face'] = (255, 255, 255, 60)
    kw['workspace'] = () + ws
    kw['tooltip_bg'] = () + infobk


UI_COLORS = {}

EVEN_COLOR = wx.Colour(240, 240, 240)
ODD_COLOR = wx.Colour(255, 255, 255)
YELLOW_EVEN_COLOR = wx.Colour(255, 255, 191)
YELLOW_ODD_COLOR = wx.Colour(255, 255, 222)
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
    if sysconst.IS_MAC:
        _init_mac_colors(kw)
    elif sysconst.IS_MSW:
        _init_msw_colors(kw)
    else:
        _init_gtk_colors(kw)

    global EVEN_COLOR, ODD_COLOR
    lb_bg = get_sys_color(wx.SYS_COLOUR_LISTBOX)
    EVEN_COLOR = wx.Colour(*mix_colors((0, 0, 0), lb_bg, 15))
    ODD_COLOR = wx.Colour(*mix_colors((255, 255, 255), lb_bg, 15))


def get_sel_bg():
    return get_sys_color(wx.SYS_COLOUR_ACTIVECAPTION) \
        if sysconst.IS_GTK2 else get_sys_color(wx.SYS_COLOUR_HIGHLIGHT)
