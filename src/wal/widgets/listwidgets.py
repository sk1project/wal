# -*- coding: utf-8 -*-
#
#  Copyright (C) 2015-2018 by Igor E. Novikov
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
import wx.lib.mixins.listctrl as listmix

from .. import const
from .. import mixins
from .. import panels
from .. import utils


class SimpleList(wx.ListCtrl,
                 listmix.ListCtrlAutoWidthMixin, mixins.WidgetMixin):
    data = []
    select_cmd = None
    activate_cmd = None
    alt_color = False

    def __init__(self, parent, data=None, border=True, header=False,
                 single_sel=True, virtual=False, alt_color=False,
                 even_color=None, odd_color=None,
                 on_select=None, on_activate=None):
        self.data = data or []
        self.alt_color = alt_color
        self.odd_color = odd_color or wx.Colour(*const.UI_COLORS['odd'])
        self.even_color = even_color or wx.Colour(*const.UI_COLORS['even'])
        style = wx.LC_REPORT | wx.LC_VRULES | wx.NO_BORDER
        style = style | wx.LC_NO_HEADER if not header else style
        style = style | wx.LC_SINGLE_SEL if single_sel else style
        style = style | wx.LC_VIRTUAL if virtual else style
        wx.ListCtrl.__init__(self, parent, wx.ID_ANY, style=style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        if self.data:
            self.update(self.data)
        if on_select:
            self.select_cmd = on_select
            self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_select, self)
        if on_activate:
            self.activate_cmd = on_activate
            self.Bind(wx.wx.EVT_LIST_ITEM_ACTIVATED, self.on_activate, self)
        self.set_bg(const.UI_COLORS['list_bg'])

    def set_active(self, index):
        if len(self.data) - 1 >= index:
            self.Select(index, True)

    def clear_all(self):
        self.ClearAll()

    def set_column_width(self, index, width):
        self.SetColumnWidth(index, width)

    def update(self, data):
        self.DeleteAllItems()
        self.data = data
        if not self.GetColumnCount():
            self.set_columns()
        self.set_data(self.data, self.alt_color)
        self.SetColumnWidth(0, wx.LIST_AUTOSIZE)

    def set_columns(self):
        self.InsertColumn(0, '')

    def set_data(self, data, alt_color=True):
        even = False
        i = 0
        for item in data:
            item = utils.tr(item)
            self.Append([item])
            if alt_color:
                list_item = self.GetItem(i)
                if even:
                    list_item.SetBackgroundColour(self.even_color)
                else:
                    list_item.SetBackgroundColour(self.odd_color)
                self.SetItem(list_item)
                even = not even
                i += 1

    def on_select(self, *args):
        index = self.GetFocusedItem()
        ret = self.data[index] if index >= 0 else None
        self.select_cmd(ret)

    def on_activate(self, *args):
        index = self.GetFocusedItem()
        if not index < 0:
            self.activate_cmd(self.data[index])

    def get_selected(self):
        index = self.GetFocusedItem()
        return self.data[index] if not index < 0 else None

    def get_active(self):
        return self.GetFocusedItem()


class ReportList(SimpleList):
    def __init__(self, parent, data=None, border=True, header=True,
                 single_sel=True, virtual=False, alt_color=True,
                 even_color=None, odd_color=None,
                 on_select=None, on_activate=None):
        data = data or []
        SimpleList.__init__(self, parent, data, border, header, single_sel,
                            virtual, alt_color, even_color, odd_color,
                            on_select, on_activate)

    def set_columns(self):
        for item in self.data[0]:
            index = self.data[0].index(item)
            self.InsertColumn(index, utils.tr(item))

    def set_data(self, data, alt_color=True):
        even = False
        i = 0
        cols = len(data[0])
        subheader = any(isinstance(i, str) for i in data)
        for item in data[1:]:
            if isinstance(item, list):
                list_item = [utils.tr(label) for label in item]
            elif isinstance(item, str):
                list_item = [utils.tr(item), ] + ['', ] * (cols - 1)
            else:
                continue
            self.Append(list_item)
            list_item = self.GetItem(i)
            if subheader:
                if isinstance(item, str):
                    list_item.SetBackgroundColour(self.even_color)
                    self.SetItem(list_item)
            elif alt_color:
                color = self.even_color if even else self.odd_color
                list_item.SetBackgroundColour(color)
                self.SetItem(list_item)
                even = not even
            i += 1

    def on_select(self, *args):
        index = self.GetFocusedItem()
        ret = self.data[index + 1] if index >= 0 else None
        self.select_cmd(ret)

    def on_activate(self, *args):
        index = self.GetFocusedItem()
        if not index < 0:
            self.activate_cmd(self.data[index + 1])

    def get_selected(self):
        index = self.GetFocusedItem()
        return self.data[index + 1] if not index < 0 else None


class VirtualList(SimpleList):
    def __init__(self, parent, data=None, border=True, header=True,
                 single_sel=True, virtual=True, alt_color=True,
                 even_color=None, odd_color=None,
                 on_select=None, on_activate=None):
        data = data or []
        SimpleList.__init__(self, parent, data, border, header, single_sel,
                            virtual, alt_color, even_color, odd_color,
                            on_select, on_activate)

    def OnGetItemText(self, item, col):
        return self.get_item_text(item, col)

    def get_item_text(self, _item, _col):
        """
        Callback method. Should return item text for specified column.
        """
        return ''

    def OnGetItemImage(self, item):
        return self.get_item_image(item)

    def get_item_image(self, _item):
        """
        Callback method. Should return item icon index or -1.
        """
        return -1


class PrefsList(panels.ScrolledCanvas, mixins.SensitiveDrawableWidget):
    callback = None
    data = None
    selected = 2
    metrics = None

    def __init__(self, parent, data=None, on_select=None):
        self.data = [
            (utils.recolor_bmp(obj.icon, const.UI_COLORS['selected_text_bg']),
             utils.recolor_bmp(obj.icon, const.UI_COLORS['selected_text']),
             utils.tr(obj.name), utils.tr(obj.title), obj)
            for obj in data]
        self.set_metrics()
        self.callback = on_select
        panels.ScrolledCanvas.__init__(self, parent, border=False)
        mixins.SensitiveDrawableWidget.__init__(self, True)
        self.set_bg(const.UI_COLORS['entry_bg'])
        self.set_virtual_size()
        self.set_double_buffered()

    def get_selected(self):
        return self.data[self.selected][-1]

    def get_selected_index(self):
        return self.selected

    def set_selected(self, index):
        if len(self.data) > index != self.selected:
            self.selected = index
            self.refresh()
            if self.callback:
                self.callback(self.data[self.selected][-1])

    def set_metrics(self):
        self.metrics = {
            'padding': 5,
            'bmp': 32,
            'bmp_padding': (0, 0),
            'width': 100,
            'height': 43,
            'text_xpadding': 47,
            'txt_ypadding': 5,
            'txt2_ypadding': 23,
        }
        if not self.data:
            return

        bw, bh = utils.get_bitmap_size(self.data[0][0])
        w0, h0 = utils.get_max_text_size([item[2] for item in self.data], True)
        w1, h1 = utils.get_max_text_size(
            [item[3] for item in self.data], False, -2)
        self.metrics['bmp'] = bw
        height = max(bh, h0 + h1 + 3)
        self.metrics['bmp_padding'] = (0, (height - bh) / 2)
        self.metrics['text_xpadding'] = 3 * self.metrics['padding'] + \
                                        self.metrics['bmp']
        self.metrics['txt_ypadding'] = self.metrics['padding']
        self.metrics['txt2_ypadding'] = self.metrics['txt_ypadding'] + h0 + 3
        self.metrics['height'] = height + 2 * self.metrics['padding'] + 1
        self.metrics['width'] = self.metrics['text_xpadding'] + max(w0, w1)

    def set_scroll_rate(self, h=20, v=20):
        self.SetScrollRate(h, v)

    def _mouse_wheel(self, event):
        event.Skip()

    def mouse_left_up(self, point):
        h = self.win_to_doc(*point)[1]
        index = h / self.metrics['height']
        self.set_selected(index)

    def set_virtual_size(self):
        w, h = self.metrics['width'], self.metrics['height']
        panels.ScrolledCanvas.set_virtual_size(self, (w, len(self.data) * h))

    def paint(self):
        self.set_virtual_size()
        w, h = self.get_size()
        index = 0
        mt = self.metrics
        item_h = mt['height']

        self.prepare_dc(self.pdc)

        for item in self.data:
            shift = item_h * index
            # Bottom line drawing
            self.set_stroke(const.UI_COLORS['border'])
            self.draw_line(0, item_h * (index + 1),
                           max(w, mt['width']) + 20, item_h * (index + 1))
            # Selection
            if self.selected == index:
                rect = (0, shift, max(w, mt['width']) + 20, mt['height'])
                if const.IS_MSW:
                    self.set_stroke()
                    self.set_fill(const.UI_COLORS['selected_text_bg'])
                    self.draw_rect(*rect)
                else:
                    render = wx.RendererNative.Get()
                    render.DrawItemSelectionRect(
                        self, self.dc, wx.Rect(*rect), wx.CONTROL_SELECTED)
            # Bitmap drawing
            bmp_pos = (mt['padding'] + mt['bmp_padding'][0],
                       mt['padding'] + mt['bmp_padding'][1])
            self.draw_bitmap(item[0] if self.selected != index else item[1],
                             bmp_pos[0], bmp_pos[1] + shift)
            # Main text
            self.set_font(True, 0)
            self.set_text_color(const.UI_COLORS['fg']
                                if self.selected != index else
                                const.UI_COLORS['selected_text'])
            self.draw_text(item[2], mt['text_xpadding'],
                           mt['txt_ypadding'] + shift)
            # Secondary text
            self.set_font(False, -1 if const.IS_MSW else -2)
            self.set_text_color(const.UI_COLORS['disabled_text']
                                if self.selected != index else
                                const.UI_COLORS['selected_text'])
            self.draw_text(item[3], mt['text_xpadding'],
                           mt['txt2_ypadding'] + shift)

            index += 1
