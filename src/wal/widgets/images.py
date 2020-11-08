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
from wx.adv import Animation, AnimationCtrl

from .. import base
from .. import const
from .. import mixins
from .. import utils


class Bitmap(wx.StaticBitmap, mixins.WidgetMixin):
    bmp = None
    rcallback = None
    lcallback = None

    def __init__(self, parent, bitmap, on_left_click=None, on_right_click=None):
        self.bmp = bitmap
        wx.StaticBitmap.__init__(self, parent, wx.ID_ANY, bitmap)
        if on_left_click:
            self.lcallback = on_left_click
            self.Bind(wx.EVT_LEFT_UP, self._on_left_click, self)
        if on_right_click:
            self.rcallback = on_right_click
            self.Bind(wx.EVT_RIGHT_UP, self._on_right_click, self)

    def _on_right_click(self, event):
        if self.rcallback:
            self.rcallback(base.MouseEvent(event))

    def _on_left_click(self, event):
        if self.lcallback:
            self.lcallback(base.MouseEvent(event))

    def _get_bitmap(self):
        if const.IS_MSW and not self.get_enabled():
            return utils.disabled_bmp(self.bmp)
        return self.bmp

    def set_bitmap(self, bmp):
        self.bmp = bmp
        self.SetBitmap(self._get_bitmap())

    def set_enable(self, value):
        mixins.WidgetMixin.set_enable(self, value)
        if const.IS_MSW:
            self.set_bitmap(self.bmp)


class AnimatedGif(AnimationCtrl):
    def __init__(self, parent, filepath):
        AnimationCtrl.__init__(self, parent, wx.ID_ANY, Animation(filepath))

    def stop(self):
        self.Stop()

    def play(self):
        self.Play()
