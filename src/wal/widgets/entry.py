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
from .. import utils


class Entry(wx.TextCtrl, mixins.DataWidgetMixin):
    my_changes = False
    value = ''
    _callback = None
    _callback1 = None
    editable = True

    def __init__(self, parent, value='', size=const.DEF_SIZE, width=0,
                 onchange=None, multiline=False, richtext=False, onenter=None,
                 editable=True, no_border=False, no_wrap=False):
        self.value = value
        self.editable = editable
        self._callback = onchange
        style = wx.TE_MULTILINE if multiline else 0
        style = style | wx.TE_RICH2 if richtext else style
        style = style | wx.NO_BORDER if no_border else style
        style = style | wx.TE_PROCESS_ENTER if onenter else style
        style = style | wx.TE_DONTWRAP if no_wrap else style

        size = self._set_width(size, width)
        wx.TextCtrl.__init__(self, parent, wx.ID_ANY, self.value, size=size, style=style)
        if onenter:
            self._callback1 = onenter
            self.Bind(wx.EVT_TEXT_ENTER, self._on_enter, self)
        if multiline:
            self.ScrollPages(0)
        self.SetEditable(editable)
        self.Bind(wx.EVT_TEXT, self._on_change, self)

    def get_cursor_pos(self):
        return self.GetInsertionPoint()

    def set_cursor_pos(self, pos):
        pos = 0 if pos < 0 else pos
        pos = len(self.value) if pos > len(self.value) else pos
        self.SetInsertionPoint(pos)

    def _on_change(self, event):
        if self.my_changes:
            self.my_changes = False
        else:
            self.value = self.GetValue()
            if self._callback:
                self._callback()
        event.Skip()

    def _on_enter(self, event):
        event.StopPropagation()
        self.value = self.GetValue()
        if self._callback1:
            self._callback1()

    def set_value(self, val):
        self.my_changes = True
        self.value = val
        cursor_pos = self.get_cursor_pos()
        self.SetValue(self.value)
        self.set_cursor_pos(cursor_pos)

    def set_editable(self, val):
        self.SetEditable(val)

    def set_text_colors(self, fg=(), bg=()):
        fg = wx.Colour(*fg) if fg else wx.NullColour
        bg = wx.Colour(*bg) if bg else wx.NullColour
        self.SetDefaultStyle(wx.TextAttr(fg, bg))

    def set_monospace(self, zoom=0):
        points = self.GetFont().GetPointSize()
        f = wx.Font(points + zoom, wx.MODERN, wx.NORMAL, wx.NORMAL)
        self.SetDefaultStyle(wx.TextAttr(wx.NullColour, wx.NullColour, f))

    def append(self, txt):
        self.AppendText(txt)
        self.value = self.GetValue()

    def clear(self):
        self.Clear()
        self.value = ''
