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

from .. import const
from .. import mixins
from .. import panels


class VLine(wx.StaticLine, mixins.WidgetMixin):
    def __init__(self, parent):
        wx.StaticLine.__init__(self, parent, style=wx.VERTICAL)


class HLine(wx.StaticLine, mixins.WidgetMixin):
    def __init__(self, parent):
        wx.StaticLine.__init__(self, parent, style=wx.HORIZONTAL)


class PLine(panels.VPanel):
    def __init__(self, parent, color=None):
        panels.VPanel.__init__(self, parent)
        self.pack((1, 1))
        self.set_bg(color or const.UI_COLORS['hover_solid_border'])
