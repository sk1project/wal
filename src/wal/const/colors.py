# -*- coding: utf-8 -*-
#
#  Copyright (C) 2013-2020 by Ihor E. Novikov
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
import typing as tp

from . import sysconst


def mix_colors(fg: tp.Union[tp.List[float], tp.Tuple[float, ...]],
               bg: tp.Union[tp.List[float], tp.Tuple[float, ...]],
               alpha: float) -> tp.Tuple[float, float, float]:
    """Mixes two RGB color values applying transparency value

    :param fg: (tuple|list) foreground RGB color value
    :param bg: (tuple|list) foreground RGB color value
    :param alpha: (float) transparency value
    :return: tuple of mixed RGB color values
    """
    r1, g1, b1 = fg[:3]
    r2, g2, b2 = bg[:3]
    a1 = alpha / 255.0
    a2 = 1.0 - a1
    r = int(r1 * a1 + r2 * a2)
    b = int(b1 * a1 + b2 * a2)
    g = int(g1 * a1 + g2 * a2)
    return r, g, b


def lighter_color(color: tp.Union[tp.List[float], tp.Tuple[float, ...]],
                  coef: float) -> tp.Tuple[float, float, float]:
    """Lighters color by provided coefficient between 0.0 - 1.0

    :param color: (tuple|list) RGB color value
    :param coef: (float) lightening coefficient between 0.0 - 1.0
    :return: tuple of lightened RGB color values
    """
    white = (255, 255, 255)
    return mix_colors(color, white, coef * 255.0)


def get_sys_color(color_const: int) -> tp.Tuple[float, float, float]:
    """Returns wx predefined system color as RGB tuple

    :param color_const: (int) wx predefined color constant
    :return: tuple of RGB color values
    """
    return wx.SystemSettings.GetColour(color_const).Get()[:3]


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


def get_system_colors() -> tp.Dict[str, tp.Tuple[float, float, float]]:
    """Returns wx predefined system colors as RGB tuples in dict

    :return: dict of RGB tuples
    """
    return {
        'fg': get_sys_color(wx.SYS_COLOUR_BTNTEXT),
        'bg': get_sys_color(wx.SYS_COLOUR_3DFACE),
        'text': get_sys_color(wx.SYS_COLOUR_BTNTEXT),
        'disabled_text': get_sys_color(wx.SYS_COLOUR_GRAYTEXT),
        'selected_text': get_sys_color(wx.SYS_COLOUR_HIGHLIGHTTEXT),
        'selected_text_bg': get_sys_color(wx.SYS_COLOUR_ACTIVECAPTION)
        if sysconst.IS_GTK2 else get_sys_color(wx.SYS_COLOUR_HIGHLIGHT),
        'border': mix_colors(get_sys_color(wx.SYS_COLOUR_GRAYTEXT),
                             get_sys_color(wx.SYS_COLOUR_3DFACE), 150)
        if sysconst.IS_AMBIANCE else get_sys_color(wx.SYS_COLOUR_BTNSHADOW),
        'entry_bg': get_sys_color(wx.SYS_COLOUR_WINDOW),
        'workspace': get_sys_color(wx.SYS_COLOUR_APPWORKSPACE),
        'tooltip': get_sys_color(wx.SYS_COLOUR_INFOBK),
        'list_bg': get_sys_color(wx.SYS_COLOUR_LISTBOX),
        '3dlight': get_sys_color(wx.SYS_COLOUR_3DLIGHT),
    }


def set_ui_colors(prefs: tp.Optional[tp.Dict[str, tp.Tuple[float, float, float]]] = None) -> None:
    """Sets UI_COLOR members and updates them from optional prefs.

    :param prefs: (dict|None) optional prefs dict
    """
    kw = UI_COLORS
    kw.update(get_system_colors())
    kw.update(prefs or {})
    kw['even'] = mix_colors((0, 0, 0), kw['list_bg'], 15)
    kw['odd'] = mix_colors((255, 255, 255), kw['list_bg'], 15)


def get_sel_bg() -> tp.Tuple[float, float, float]:
    """Returns selection background color

    :return: RGB color values tuple
    """
    return get_sys_color(wx.SYS_COLOUR_HIGHLIGHT)
