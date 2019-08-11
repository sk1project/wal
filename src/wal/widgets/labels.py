# -*- coding: utf-8 -*-
#
#  Copyright (C) 2019 by Igor E. Novikov
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

from .. import mixins
from .. import utils


class Label(wx.StaticText, mixins.WidgetMixin):
    def __init__(self, parent, text='', fontbold=False, fontsize=0, fg=()):
        wx.StaticText.__init__(self, parent, wx.ID_ANY, utils.tr(text))
        font = self.GetFont()
        if fontbold:
            font.SetWeight(wx.FONTWEIGHT_BOLD)
        if fontsize:
            if isinstance(fontsize, str):
                sz = int(fontsize)
                if font.IsUsingSizeInPixels():
                    font.SetPixelSize((0, sz))
                else:
                    font.SetPointSize(sz)
            else:
                if font.IsUsingSizeInPixels():
                    sz = font.GetPixelSize()[1] + fontsize
                    font.SetPixelSize((0, sz))
                else:
                    sz = font.GetPointSize() + fontsize
                    font.SetPointSize(sz)
        self.SetFont(font)
        if fg:
            self.SetForegroundColour(wx.Colour(*fg))
        self.Wrap(-1)

    def set_min_width(self, width):
        self.SetMinSize((width, -1))

    def set_text(self, text):
        self.SetLabel(utils.tr(text))

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


class HtmlLabel(wx.HyperlinkCtrl, mixins.WidgetMixin):
    def __init__(self, parent, text, url=''):
        url = text if not url else url
        wx.HyperlinkCtrl.__init__(self, parent, wx.ID_ANY, utils.tr(text), url)
