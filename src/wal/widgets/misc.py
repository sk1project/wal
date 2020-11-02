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

import wx

from .. import mixins
from .. import panels


class Slider(wx.Slider, mixins.RangeDataWidgetMixin):
    callback = None
    final_callback = None

    def __init__(
            self, parent, value=0, range_val=(1, 100),
            size=(100, -1), vertical=False, onchange=None,
            on_final_change=None):
        self.range_val = range_val
        style = 0
        if vertical:
            style |= wx.SL_VERTICAL
            if size == (100, -1):
                size = (-1, 100)
        else:
            style |= wx.SL_HORIZONTAL
        start, end = range_val
        wx.Slider.__init__(
            self, parent, wx.ID_ANY, value, start,
            end, size=size, style=style)
        if onchange:
            self.callback = onchange
            self.Bind(wx.EVT_SCROLL, self._onchange, self)
        if on_final_change:
            self.final_callback = on_final_change
            self.Bind(wx.EVT_LEFT_UP, self._on_final_change, self)
            self.Bind(wx.EVT_RIGHT_UP, self._on_final_change, self)

    def _onchange(self, _event):
        if self.callback:
            self.callback()

    def _on_final_change(self, event):
        event.Skip()
        if self.final_callback:
            self.final_callback()


class Splitter(wx.SplitterWindow, mixins.WidgetMixin):
    def __init__(self, parent, live_update=True, hidden=False):
        style = wx.SP_NOBORDER
        style = style | wx.SP_LIVE_UPDATE if live_update else style
        wx.SplitterWindow.__init__(self, parent, wx.ID_ANY, style=style)
        self.SetSashInvisible(hidden)

    def split_vertically(self, win1, win2, sash_pos=0):
        self.SplitVertically(win1, win2, sash_pos)

    def split_horizontally(self, win1, win2, sash_pos=0):
        self.SplitHorizontally(win1, win2, sash_pos)

    def set_min_size(self, size):
        self.SetMinimumPaneSize(size)

    def get_pane_size(self):
        return self.GetSashPosition()

    def unsplit(self, remove_win=None):
        self.Unsplit(remove_win)

    def set_sash_gravity(self, val):
        self.SetSashGravity(val)

    def set_sash_position(self, val):
        self.SetSashPosition(val)

    def get_sash_position(self):
        return self.GetSashPosition()


class SplitterSash(panels.VPanel, mixins.SensitiveWidget):
    move = False
    mouse_pos = 0
    sash_pos = 0

    def __init__(self, parent, splitter=None, size=3):
        self.splitter = splitter
        panels.VPanel.__init__(self, parent)
        mixins.SensitiveWidget.__init__(self, check_move=True)
        self.pack((size, size))
        self.SetCursor(wx.StockCursor(wx.CURSOR_SIZEWE))

    def mouse_left_down(self, point):
        self.capture_mouse()
        self.move = True
        self.mouse_pos = self.ClientToScreen(point)[0]
        self.sash_pos = self.splitter.get_sash_position()

    def mouse_move(self, point):
        if self.move:
            dx = self.ClientToScreen(point)[0] - self.mouse_pos
            self.splitter.set_sash_position(self.sash_pos + dx)

    def mouse_left_up(self, point):
        self.release_mouse()
        self.move = False


class ScrollBar(wx.ScrollBar, mixins.WidgetMixin):
    callback = None
    autohide = False

    def __init__(self, parent, vertical=True, onscroll=None, autohide=False):
        style = wx.SB_VERTICAL if vertical else wx.SB_HORIZONTAL
        wx.ScrollBar.__init__(self, parent, wx.ID_ANY, style=style)
        self.callback = onscroll
        self.autohide = autohide
        self.Bind(wx.EVT_SCROLL, self._scrolling, self)

    def set_scrollbar(self, pos, thumbsize, rng, pagesize, refresh=True):
        self.SetScrollbar(pos, thumbsize, rng, pagesize, refresh)

    def set_callback(self, callback):
        self.callback = callback

    def _scrolling(self, *_args):
        if self.callback:
            self.callback()

    def get_thumb_pos(self):
        return self.GetThumbPosition()


class ProgressBar(wx.Gauge, mixins.WidgetMixin):
    def __init__(self, parent):
        size = (400, 15)
        wx.Gauge.__init__(self, parent, range=100, size=size,
                          style=wx.GA_HORIZONTAL | wx.GA_SMOOTH)
        self.SetRange(100)

    def set_value(self, val):
        if val < 0:
            return self.pulse()
        self.SetValue(int(val))
        self.Update()

    def set_dec_value(self, val):
        self.set_value(val * 100)

    def get_value(self):
        return self.GetValue()

    def pulse(self):
        self.Pulse()
