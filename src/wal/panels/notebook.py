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

from .. import mixins
from .. import utils


class Notebook(wx.Notebook, mixins.WidgetMixin):
    childs = None
    callback = None

    def __init__(self, parent, on_change=None):
        self.childs = []
        wx.Notebook.__init__(self, parent, wx.ID_ANY)
        if on_change:
            self.callback = on_change
            self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self._on_change, self)

    def _on_change(self, _event):
        self.refresh()
        if self.callback:
            self.callback(self.get_active_index())

    def add_page(self, page, title):
        page.layout()
        self.childs.append(page)
        self.AddPage(page, utils.tr(title))

    def remove_page(self, page):
        index = self.childs.index(page)
        self.childs.remove(page)
        self.RemovePage(index)

    def remove_page_by_index(self, index):
        self.childs.remove(self.childs[index])
        self.RemovePage(index)

    def get_active_index(self):
        return self.GetSelection()

    def get_active_page(self):
        return self.childs[self.get_active_index()]

    def set_active_index(self, index):
        self.SetSelection(index)

    def set_active_page(self, page):
        if page in self.childs:
            self.SetSelection(self.childs.index(page))
