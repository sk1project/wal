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

from .. import const
from .. import mixins
from .. import renderer

from wx.adv import HyperlinkCtrl


class Label(wx.StaticText, mixins.WidgetMixin):
    def __init__(self, parent, text='', fontbold=False, fontsize=0, fg=()):
        self.parent = parent
        wx.StaticText.__init__(self, parent, wx.ID_ANY, text, style=wx.ALIGN_CENTER)
        font = self.GetFont()
        if fontbold:
            font.SetWeight(wx.FONTWEIGHT_BOLD)
        if fontsize:
            if isinstance(fontsize, str):
                sz = int(fontsize)
                font.SetPixelSize((0, sz))
            else:
                fontsize = int(fontsize)
                if fontsize > 0:
                    [font.MakeLarger() for _i in range(fontsize)]
                else:
                    [font.MakeSmaller() for _i in range(abs(fontsize))]
        self.SetFont(font)
        if fg:
            self.SetForegroundColour(wx.Colour(*fg))
        self.Wrap(-1)
        if const.IS_GTK3:
            self.Bind(wx.EVT_UPDATE_UI, self._on_show)

    def _on_show(self, *_args):
        self.InvalidateBestSize()
        self.SetSize(self.BestSize)

    def set_min_width(self, width):
        self.SetMinSize((width, -1))

    def set_text(self, text):
        self.SetLabel(text)

    def wrap(self, width):
        self.Wrap(width)


class SensitiveLabel(Label):
    def __init__(self, parent, text='', fontbold=False, fontsize=0, fg=(),
                 on_left_click=None, on_right_click=None):
        Label.__init__(self, parent, text, fontbold, fontsize, fg)
        if on_left_click:
            self.Bind(wx.EVT_LEFT_UP, on_left_click)
        if on_right_click:
            self.Bind(wx.EVT_RIGHT_UP, on_right_click)


class HyperlinkLabel(HyperlinkCtrl, mixins.WidgetMixin):
    def __init__(self, parent, text, url=''):
        url = text if not url else url
        HyperlinkCtrl.__init__(self, parent, wx.ID_ANY, text, url)


class ImageLabel(mixins.GenericGWidget):
    rightclick_cmd = None

    def __init__(
            self, parent, art_id=None, art_size=const.DEF_SIZE, text='',
            tooltip='', padding=0,
            fontbold=False, fontsize=0, textplace=const.RIGHT,
            onclick=None, onrightclick=None, repeat=False):

        self.flat = True

        mixins.GenericGWidget.__init__(self, parent, tooltip, onclick, repeat)
        self.renderer = renderer.LabelRenderer(
            self, art_id, art_size, text,
            padding, fontbold, fontsize, textplace)

        if onrightclick:
            self.rightclick_cmd = onrightclick
            self.Bind(wx.EVT_RIGHT_UP, self._on_rightclick, self)

    def _on_rightclick(self, _event):
        if self.rightclick_cmd:
            self.rightclick_cmd()

    def _on_paint(self, event):
        if self.enabled:
            self.renderer.draw_normal()
        else:
            self.renderer.draw_disabled()
