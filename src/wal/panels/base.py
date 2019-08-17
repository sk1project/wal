# -*- coding: utf-8 -*-
#
# 	Copyright (C) 2013-2018 by Igor E. Novikov
#
# 	This program is free software: you can redistribute it and/or modify
# 	it under the terms of the GNU General Public License as published by
# 	the Free Software Foundation, either version 3 of the License, or
# 	(at your option) any later version.
#
# 	This program is distributed in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# 	GNU General Public License for more details.
#
# 	You should have received a copy of the GNU General Public License
# 	along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#   MacOS X env: export VERSIONER_PYTHON_PREFER_32_BIT=yes

import wx
import wx.lib.scrolledpanel as scrolled

from .. import const
from .. import mixins
from .. import utils
from ..base import MouseEvent
from ..mixins import WidgetMixin


class Panel(wx.Panel, WidgetMixin):
    def __init__(self, parent, border=False, allow_input=False,
                 style=wx.TAB_TRAVERSAL):
        style = style | wx.WANTS_CHARS if allow_input else style
        style = style | wx.BORDER_MASK if border and not const.IS_WX3 else style
        wx.Panel.__init__(self, parent, wx.ID_ANY, style=style)

    def set_size(self, size):
        self.SetSize(size)

    def layout(self):
        self.Layout()

    def fit(self):
        self.Fit()


class SizedPanel(Panel):
    panel = None

    def __init__(self, parent, orientation=wx.HORIZONTAL, border=False):
        self.parent = parent
        self.orientation = orientation
        Panel.__init__(self, parent, border)
        self.box = wx.BoxSizer(orientation)
        self.SetSizer(self.box)
        self.panel = self

    def add(self, *args, **kw):
        """Arguments: object, expandable (0 or 1), flag, border"""
        obj = args[0]
        if not isinstance(obj, tuple):
            if not obj.GetParent() == self.panel:
                obj.Reparent(self.panel)
        self.box.Add(*args, **kw)
        if not isinstance(obj, tuple) and not isinstance(obj, int):
            obj.Show()

    def box_add(self, *args, **kw):
        """Arguments: object, expandable (0 or 1), flag, border"""
        self.box.Add(*args, **kw)

    def remove(self, obj):
        self.box.Detach(obj)
        if not isinstance(obj, tuple) and not isinstance(obj, int):
            obj.Hide()

    def remove_all(self):
        self.box.Clear()


class HPanel(SizedPanel):
    def __init__(self, parent, border=False):
        SizedPanel.__init__(self, parent, wx.HORIZONTAL, border)

    def pack(self, obj, expand=False, fill=False,
             padding=0, start_padding=0, end_padding=0, padding_all=0):
        expand = 1 if expand else 0
        flags = wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL
        flags = flags | wx.LEFT | wx.RIGHT if padding else flags
        flags = flags | wx.ALL if padding_all else flags
        padding = padding_all or padding
        flags = flags | wx.LEFT if start_padding else flags
        padding = start_padding or padding
        flags = flags | wx.RIGHT if end_padding else flags
        padding = end_padding or padding
        flags = flags | wx.EXPAND if fill else flags

        self.add(obj, expand, flags, padding)


class VPanel(SizedPanel):
    def __init__(self, parent, border=False):
        SizedPanel.__init__(self, parent, wx.VERTICAL, border)

    def pack(
            self, obj, expand=False, fill=False, align_center=True,
            padding=0, start_padding=0, end_padding=0, padding_all=0):
        expand = 1 if expand else 0
        flags = wx.ALIGN_TOP
        flags = flags | wx.ALIGN_CENTER_HORIZONTAL if align_center else flags
        flags = flags | wx.TOP | wx.BOTTOM if padding else flags
        flags = flags | wx.ALL if padding_all else flags
        padding = padding_all or padding
        flags = flags | wx.TOP if start_padding else flags
        padding = start_padding or padding
        flags = flags | wx.BOTTOM if end_padding else flags
        padding = end_padding or padding
        flags = flags | wx.EXPAND if fill else flags

        self.add(obj, expand, flags, padding)


class BorderedPanel(VPanel, mixins.DrawableWidget):
    widget_panel = None

    def __init__(self, parent):
        VPanel.__init__(self, parent)
        mixins.DrawableWidget.__init__(self)

    def paint(self):
        w, h = self.get_size()
        dx = 8
        dy = 0
        if self.widget_panel:
            dx += self.widget_panel.get_size()[0]
            dy += self.widget_panel.get_size()[1] // 2
        self.set_fill(None)
        color = const.UI_COLORS['border']
        self.set_stroke(color)
        self.draw_line(0, dy, 6, dy)
        self.draw_line(0, dy, 0, h - 2)
        self.draw_line(0, h - 2, w - 2, h - 2)
        self.draw_line(w - 2, h - 2, w - 2, dy)
        self.draw_line(w - 2, dy, dx - 1, dy)
        self.layout()
        if self.widget_panel:
            self.widget_panel.refresh()


class LabeledPanel(BorderedPanel):
    panel = None
    widget_panel = None
    widget = None

    def __init__(self, parent, text='', widget=None):
        BorderedPanel.__init__(self, parent)
        self.inner_panel = VPanel(self)

        if widget or text:
            self.widget_panel = HPanel(self)
            self.widget = widget
            if text:
                self.widget = wx.StaticText(self.widget_panel,
                                            wx.ID_ANY, utils.tr(text))
            self.widget_panel.pack(self.widget, padding=5)
            self.widget_panel.Fit()
            self.add(self.widget_panel, 0, wx.ALIGN_LEFT | wx.LEFT, 7)

        self.add(self.inner_panel, 1,
                 wx.ALIGN_LEFT | wx.LEFT | wx.BOTTOM | wx.RIGHT | wx.EXPAND, 5)
        self.parent.refresh()

    def pack(self, *args, **kw):
        obj = args[0]
        self.inner_panel.pack(*args, **kw)
        if not isinstance(obj, tuple) and not isinstance(obj, int):
            obj.show()


class GridPanel(Panel, WidgetMixin):
    def __init__(self, parent, rows=2, cols=2, vgap=0, hgap=0, border=False):
        Panel.__init__(self, parent, border)
        self.grid = wx.FlexGridSizer(rows, cols, vgap, hgap)
        self.SetSizer(self.grid)

    def set_vgap(self, val):
        self.grid.SetVGap(val)

    def set_hgap(self, val):
        self.grid.SetHGap(val)

    def sel_cols(self, val):
        self.grid.SetCols(val)

    def sel_rows(self, val):
        self.grid.SetRows(val)

    def add_growable_col(self, index):
        self.grid.AddGrowableCol(index)

    def add_growable_row(self, index):
        self.grid.AddGrowableRow(index)

    def pack(self, obj, expand=False, fill=False, align_right=False,
             align_left=True):
        expand = 1 if expand else 0
        flags = wx.ALIGN_CENTER_HORIZONTAL
        flags = wx.ALIGN_RIGHT if align_right else flags
        flags = wx.ALIGN_LEFT if align_left else flags
        flags |= wx.ALIGN_CENTER_VERTICAL
        flags = flags | wx.EXPAND if fill else flags
        self.add(obj, expand, flags)

    def add(self, *args, **kw):
        """Arguments: object, expandable (0 or 1), flag"""
        obj = args[0]
        if not isinstance(obj, tuple):
            if not obj.GetParent() == self:
                obj.Reparent(self)
        self.grid.Add(*args, **kw)
        if not isinstance(obj, tuple) and not isinstance(obj, int):
            obj.show()


class ScrolledPanel(scrolled.ScrolledPanel, WidgetMixin):
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent, -1)
        self.box = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.box)
        self.SetAutoLayout(1)
        self.SetupScrolling()
        self.panel = self

    def set_size(self, size):
        self.SetSize(size)

    def layout(self):
        self.Layout()

    def fit(self):
        self.Fit()

    def pack(self, obj, expand=False, fill=False, align_center=True,
             padding=0, start_padding=0, end_padding=0, padding_all=0):
        expand = 1 if expand else 0

        flags = wx.ALIGN_TOP
        flags = flags | wx.ALIGN_CENTER_HORIZONTAL if align_center else flags
        flags = flags | wx.TOP | wx.BOTTOM if padding else flags
        flags = flags | wx.ALL if padding_all else flags
        padding = padding_all or padding
        flags = flags | wx.TOP if start_padding else flags
        padding = start_padding or padding
        flags = flags | wx.BOTTOM if end_padding else flags
        padding = end_padding or padding
        flags = flags | wx.EXPAND if fill else flags

        self.add(obj, expand, flags, padding)

    def add(self, *args, **kw):
        """Arguments: object, expandable (0 or 1), flag, border"""
        obj = args[0]
        if not isinstance(obj, tuple):
            if not obj.GetParent() == self.panel:
                obj.Reparent(self.panel)
        self.box.Add(*args, **kw)
        if not isinstance(obj, tuple) and not isinstance(obj, int):
            obj.Show()

    def box_add(self, *args, **kw):
        """Arguments: object, expandable (0 or 1), flag, border"""
        self.box.Add(*args, **kw)

    def remove(self, obj):
        self.box.Detach(obj)
        if not isinstance(obj, tuple) and not isinstance(obj, int):
            obj.Hide()

    def remove_all(self):
        self.box.Clear()


class ScrolledCanvas(wx.ScrolledWindow, WidgetMixin):
    def __init__(self, parent, border=False):
        style = wx.NO_BORDER
        if border and not const.IS_WX3:
            style = wx.BORDER_MASK
        wx.ScrolledWindow.__init__(self, parent, wx.ID_ANY, style=style)
        self.set_scroll_rate()
        self.set_double_buffered()

    def set_virtual_size(self, size):
        self.SetVirtualSize(size)

    def get_virtual_size(self):
        return self.GetVirtualSize()

    def set_scroll_rate(self, h=20, v=20):
        self.SetScrollRate(h, v)

    def refresh(self, x=0, y=0, w=0, h=0, clear=True):
        if not w:
            w, h = self.GetVirtualSize()
        self.Refresh(rect=wx.Rect(x, y, w, h))

    def set_size(self, size):
        self.SetSize(size)

    def prepare_dc(self, dc):
        self.PrepareDC(dc)

    def win_to_doc(self, x, y):
        return tuple(self.CalcUnscrolledPosition(wx.Point(x, y)))

    def doc_to_win(self, x, y):
        return tuple(self.CalcScrolledPosition(wx.Point(x, y)))


class Expander(VPanel, mixins.DrawableWidget):
    state = False
    callback = None

    def __init__(self, parent, on_click=None):
        VPanel.__init__(self, parent)
        mixins.DrawableWidget.__init__(self)
        self.pack((13, 13))
        if on_click:
            self.callback = on_click
            self.Bind(wx.EVT_LEFT_UP, self._click, self)
            self.Bind(wx.EVT_RIGHT_UP, self._click, self)
        self.refresh()

    def _click(self, _event):
        self.callback()

    def change(self, val=False):
        self.state = val
        self.refresh()

    def paint(self):
        w, h = self.get_size()
        self.set_stroke(const.BLACK, 1)
        self.set_fill(None)
        self.draw_rect(3, 3, w - 4, h - 4)
        half = int(w / 2.0) + 1
        self.draw_line(5, half, w - 3, half)
        if not self.state:
            self.draw_line(half, 5, half, h - 3)


class ExpandedPanel(VPanel):
    def __init__(self, parent, txt=''):
        VPanel.__init__(self, parent)
        header = HPanel(self)
        self.expander = Expander(header, on_click=self.expand)
        header.pack(self.expander, padding=2)
        if txt:
            header.pack(wx.StaticText(header, wx.ID_ANY, utils.tr(txt)))
        VPanel.pack(self, header, fill=True)
        self.container = VPanel(self)
        VPanel.pack(self, self.container, fill=True)
        self.container.set_visible(False)
        self.layout()

    def expand(self):
        self.container.set_visible(not self.container.is_shown())
        self.parent.layout()
        self.expander.change(self.container.is_shown())

    def pack(self, *args, **kw):
        self.container.pack(*args, **kw)


class HSizer(HPanel):
    def __init__(self, parent, grip_width=5, visible=True):
        HPanel.__init__(self, parent)
        self.client = None
        self.client_parent = None
        self.client_min = 0
        self.left_side = True
        self.move = False
        self.mouse_captured = False
        self.processing = False
        self.start = 0
        self.end = 0
        self.grip_width = grip_width
        self.visible = visible
        if self.visible:
            self.pack((self.grip_width, self.grip_width))
        self.Bind(wx.EVT_LEFT_DOWN, self.mouse_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.mouse_left_up)
        self.Bind(wx.EVT_MOTION, self.mouse_move)
        self.Bind(wx.EVT_MOUSE_CAPTURE_LOST, self.capture_lost)
        self.SetCursor(wx.StockCursor(wx.CURSOR_SIZEWE))

    def set_client(self, client_parent, client, client_min=0, left_side=True):
        self.client = client
        self.client_parent = client_parent
        self.client_min = client_min
        self.left_side = left_side

    def resize(self):
        change = self.end - self.start
        if not change:
            return
        w = self.client.get_size()[0]
        w = w + change if self.left_side else w - change
        w = self.client_min if w < self.client_min else w
        self.client.remove_all()
        self.client.pack((w, 0))
        self.client_parent.Layout()

    def capture_mouse(self):
        if const.IS_MSW:
            self.CaptureMouse()
            self.mouse_captured = True

    def release_mouse(self):
        if self.mouse_captured:
            # noinspection PyBroadException
            try:
                self.ReleaseMouse()
            except Exception:
                pass
            self.mouse_captured = False

    def capture_lost(self, _event):
        self.release_mouse()

    def mouse_left_down(self, event):
        self.move = True
        self.capture_mouse()
        event = MouseEvent(event)
        self.start = self.end = event.get_point()[0]

    def mouse_left_up(self, event):
        self.release_mouse()
        self.move = False
        event = MouseEvent(event)
        self.end = event.get_point()[0]
        self.resize()

    def mouse_move(self, event):
        if self.move:
            if self.processing:
                return
            self.processing = True
            event = MouseEvent(event)
            self.end = event.get_point()[0]
            self.resize()
            self.processing = False
