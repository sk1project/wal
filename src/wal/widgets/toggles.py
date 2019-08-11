# -*- coding: utf-8 -*-
#
# 	Copyright (C) 2015-2018 by Igor E. Novikov
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

from .. import const
from .. import mixins
from .. import panels
from .. import renderer


class ImageToggleButton(mixins.GenericGWidget):
    value = False
    onchange = None

    def __init__(
            self, parent, value=False, art_id=None, art_size=const.DEF_SIZE,
            text='', tooltip='', padding=0, decoration_padding=6,
            flat=True, native=not const.IS_MAC,
            fontbold=False, fontsize=0, textplace=const.RIGHT,
            onchange=None):

        self.flat = flat
        self.decoration_padding = decoration_padding

        self.value = value
        self.onchange = onchange
        mixins.GenericGWidget.__init__(self, parent, tooltip)

        renderer_class = renderer.NativeButtonRenderer \
            if native else renderer.ButtonRenderer
        self.renderer = renderer_class(
            self, art_id, art_size, text,
            padding, fontbold, fontsize, textplace)

    def set_value(self, value, silent=False):
        self.value = value
        if self.onchange and not silent:
            self.onchange()
        self.refresh()

    def set_active(self, value):
        self.value = value
        self.refresh()

    def get_value(self):
        return self.value

    def get_active(self):
        return self.value

    def _on_paint(self, event):
        if self.enabled:
            if not self.mouse_over and not self.value:
                self.renderer.draw_normal(self.flat)
            elif not self.mouse_over and self.value:
                self.renderer.draw_pressed()
            elif self.mouse_over and not self.value and not self.mouse_pressed:
                self.renderer.draw_hover()
            elif self.mouse_over and self.value and not self.mouse_pressed:
                self.renderer.draw_pressed()
            elif self.mouse_over and self.mouse_pressed:
                self.renderer.draw_pressed()
        else:
            if self.value:
                self.renderer.draw_pressed_disabled()
            else:
                self.renderer.draw_disabled(self.flat)

    def _mouse_up(self, event):
        self.mouse_pressed = False
        if self.mouse_over:
            if self.enabled:
                self.value = not self.value
                if self.onchange:
                    self.onchange()
        self.refresh()


class ModeToggleButton(ImageToggleButton):
    keeper = None
    mode = 0
    callback = None
    allow_off = False

    def __init__(self, parent, keeper, mode, icons, names, on_change=None,
                 allow_off=False):
        self.keeper = keeper
        self.mode = mode
        self.callback = on_change
        self.allow_off = allow_off
        ImageToggleButton.__init__(
            self, parent, False, icons[mode],
            tooltip=names[mode], onchange=self.change)

    def change(self):
        if not self.get_active():
            if self.keeper.mode == self.mode and not self.allow_off:
                self.set_active(True)
            elif self.allow_off:
                if self.callback:
                    self.callback(None)
        else:
            if not self.keeper.mode == self.mode:
                if self.callback:
                    self.callback(self.mode)

    def set_mode(self, mode):
        if not self.mode == mode:
            if self.get_active():
                self.set_active(False)
        else:
            if not self.get_active():
                self.set_active(True)


class HToggleKeeper(panels.HPanel):
    mode = 0
    mode_buts = None
    modes = None
    callback = None
    allow_none = False

    def __init__(self, parent, modes, icons, names, on_change=None,
                 allow_none=False):
        self.modes = modes
        self.mode_buts = []
        self.callback = on_change
        self.allow_none = allow_none
        panels.HPanel.__init__(self, parent)
        for item in self.modes:
            but = ModeToggleButton(
                self, self, item, icons, names,
                self.changed, self.allow_none)
            self.mode_buts.append(but)
            self.pack(but)

    def set_enable(self, val):
        for item in self.mode_buts:
            item.set_enable(val)

    def changed(self, mode):
        self.mode = mode
        for item in self.mode_buts:
            item.set_mode(mode)
        if self.callback:
            self.callback(mode)

    def set_mode(self, mode):
        self.mode = mode
        for item in self.mode_buts:
            item.set_mode(mode)

    def get_mode(self):
        return self.mode


class VToggleKeeper(panels.VPanel):
    mode = 0
    mode_buts = None
    modes = None
    callback = None
    allow_none = False

    def __init__(self, parent, modes, icons, names, on_change=None,
                 allow_none=False):
        self.modes = modes
        self.mode_buts = []
        self.callback = on_change
        self.allow_none = allow_none
        panels.VPanel.__init__(self, parent)
        for item in self.modes:
            but = ModeToggleButton(
                self, self, item, icons, names,
                self.changed, self.allow_none)
            self.mode_buts.append(but)
            self.pack(but)

    def set_enable(self, val):
        for item in self.mode_buts:
            item.set_enable(val)

    def changed(self, mode):
        self.mode = mode
        for item in self.mode_buts:
            item.set_mode(mode)
        if self.callback:
            self.callback(mode)

    def set_mode(self, mode):
        self.mode = mode
        for item in self.mode_buts:
            item.set_mode(mode)

    def get_mode(self):
        return self.mode
