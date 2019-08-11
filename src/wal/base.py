# -*- coding: utf-8 -*-
#
# 	Copyright (C) 2019 by Igor E. Novikov
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

from . import const
from . import mixins
from . import utils


class Application(wx.App):
    app_name = None

    mw = None
    mdi = None
    actions = {}

    def __init__(self, name='', redirect=False):
        wx.App.__init__(self, redirect=redirect)
        if name:
            self.set_app_name(name)
        const.set_ui_colors(const.UI_COLORS)
        self._set_font_size()

    @staticmethod
    def _set_font_size():
        dc = wx.MemoryDC()
        bmp = wx.EmptyBitmap(1, 1)
        dc.SelectObject(bmp)
        dc.SetFont(wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT))
        const.FONT_SIZE[0] = dc.GetTextExtent('D')[0]
        const.FONT_SIZE[1] = dc.GetCharHeight()
        dc.SelectObject(wx.NullBitmap)

    def set_app_name(self, name):
        self.app_name = name
        self.SetAppName(name)
        self.SetClassName(name)

    def update_actions(self):
        for item in self.actions.keys():
            self.actions[item].update()

    def call_after(self, *args):
        pass

    def run(self):
        if self.mw:
            self.SetTopWindow(self.mw)
            if self.mw.maximized:
                self.mw.Maximize()
            self.mw.build()
            if self.actions:
                self.update_actions()
            self.mw.Show(True)
            self.mdi = self.mw.mdi
            wx.CallAfter(self.call_after)
            self.MainLoop()
        else:
            raise RuntimeError('Main window is not defined!')

    def exit(self, *_args):
        self.Exit()


class MainWindow(wx.Frame, mixins.DialogMixin):
    app = None
    mdi = None
    maximized = False

    def __init__(self, app=None, title='Frame', size=(100, 100),
                 vertical=True, maximized=False, on_close=None):
        self.app = app
        if app is None:
            self.app = Application()
            self.app.mw = self
            on_close = self.app.exit
        self.maximized = maximized

        wx.Frame.__init__(self, None, wx.ID_ANY, title,
                          pos=const.DEF_SIZE, size=size, name=title)
        self.orientation = wx.VERTICAL if vertical else wx.HORIZONTAL
        self.Centre()
        self.box = wx.BoxSizer(self.orientation)
        self.SetSizer(self.box)
        self.set_title(title)
        if on_close:
            self.Bind(wx.EVT_CLOSE, on_close, self)

    def build(self):
        pass

    def run(self):
        self.app.run()

    def set_global_shortcuts(self, actions):
        global_entries = []
        for item in actions.keys():
            if actions[item].global_accs:
                for acc in actions[item].global_accs:
                    global_entries.append(acc)
                    self.Bind(wx.EVT_KEY_DOWN, actions[item], self,
                              id=acc.GetCommand())
        if global_entries:
            self.SetAcceleratorTable(wx.AcceleratorTable(global_entries))

    def hide(self):
        self.Hide()

    def show(self):
        self.Show()

    def add(self, *args, **kw):
        """Arguments: object, expandable (0 or 1), flag, border"""
        self.box.Add(*args, **kw)

    def pack(self, obj, expand=False, fill=False,
             padding=0, start_padding=0, end_padding=0):
        expand = 1 if expand else 0
        if self.orientation == wx.VERTICAL:
            flags = wx.ALIGN_TOP | wx.ALIGN_CENTER_HORIZONTAL
            flags = flags | wx.TOP | wx.BOTTOM if padding else flags
            flags = flags | wx.TOP if start_padding else flags
            flags = flags | wx.BOTTOM if end_padding else flags
            flags = flags | wx.EXPAND if fill else flags
            self.box.Add(obj, expand, flags, padding)
        else:
            flags = wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL
            flags = flags | wx.LEFT | wx.RIGHT if padding else flags
            flags = flags | wx.LEFT if start_padding else flags
            flags = flags | wx.RIGHT if end_padding else flags
            flags = flags | wx.EXPAND if fill else flags
            self.box.Add(obj, expand, flags, padding)

    def set_icons(self, filepath):
        icons = wx.IconBundle()
        icons.AddIconFromFile(utils.tr(filepath), wx.BITMAP_TYPE_ANY)
        self.SetIcons(icons)

    def set_menubar(self, menubar):
        self.SetMenuBar(menubar)

    def bind_timer(self, callback):
        self.Bind(wx.EVT_TIMER, callback)

    def raise_window(self):
        self.Raise()


class MouseEvent(object):
    event = None

    def __init__(self, event):
        self.event = event

    def get_point(self):
        return list(self.event.GetPositionTuple())

    def get_rotation(self):
        return self.event.GetWheelRotation()

    def is_ctrl(self):
        return self.event.ControlDown()

    def is_alt(self):
        return self.event.AltDown()

    def is_shift(self):
        return self.event.ShiftDown()

    def is_cmd(self):
        return self.event.CmdDown()
