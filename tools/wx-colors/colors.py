import os
import sys

parent = os.path.dirname
cur_path = os.path.abspath(os.getcwd())
wal_path = os.path.join(parent(parent(cur_path)), 'src')
sys.path.insert(0, wal_path)

import wal
import wx

WX_COLORS = {
    "wx.SYS_COLOUR_SCROLLBAR": wx.SYS_COLOUR_SCROLLBAR,
    "wx.SYS_COLOUR_BACKGROUND": wx.SYS_COLOUR_BACKGROUND,
    "wx.SYS_COLOUR_ACTIVECAPTION": wx.SYS_COLOUR_ACTIVECAPTION,
    "wx.SYS_COLOUR_INACTIVECAPTION": wx.SYS_COLOUR_INACTIVECAPTION,
    "wx.SYS_COLOUR_MENU": wx.SYS_COLOUR_MENU,
    "wx.SYS_COLOUR_WINDOW": wx.SYS_COLOUR_WINDOW,
    "wx.SYS_COLOUR_WINDOWFRAME": wx.SYS_COLOUR_WINDOWFRAME,
    "wx.SYS_COLOUR_MENUTEXT": wx.SYS_COLOUR_MENUTEXT,
    "wx.SYS_COLOUR_WINDOWTEXT": wx.SYS_COLOUR_WINDOWTEXT,
    "wx.SYS_COLOUR_CAPTIONTEXT": wx.SYS_COLOUR_CAPTIONTEXT,
    "wx.SYS_COLOUR_ACTIVEBORDER": wx.SYS_COLOUR_ACTIVEBORDER,
    "wx.SYS_COLOUR_INACTIVEBORDER": wx.SYS_COLOUR_INACTIVEBORDER,
    "wx.SYS_COLOUR_APPWORKSPACE": wx.SYS_COLOUR_APPWORKSPACE,
    "wx.SYS_COLOUR_HIGHLIGHT": wx.SYS_COLOUR_HIGHLIGHT,
    "wx.SYS_COLOUR_HIGHLIGHTTEXT": wx.SYS_COLOUR_HIGHLIGHTTEXT,
    "wx.SYS_COLOUR_BTNFACE": wx.SYS_COLOUR_BTNFACE,
    "wx.SYS_COLOUR_BTNSHADOW": wx.SYS_COLOUR_BTNSHADOW,
    "wx.SYS_COLOUR_GRAYTEXT": wx.SYS_COLOUR_GRAYTEXT,
    "wx.SYS_COLOUR_BTNTEXT": wx.SYS_COLOUR_BTNTEXT,
    "wx.SYS_COLOUR_INACTIVECAPTIONTEXT": wx.SYS_COLOUR_INACTIVECAPTIONTEXT,
    "wx.SYS_COLOUR_BTNHIGHLIGHT": wx.SYS_COLOUR_BTNHIGHLIGHT,
    "wx.SYS_COLOUR_3DDKSHADOW": wx.SYS_COLOUR_3DDKSHADOW,
    "wx.SYS_COLOUR_3DLIGHT": wx.SYS_COLOUR_3DLIGHT,
    "wx.SYS_COLOUR_INFOTEXT": wx.SYS_COLOUR_INFOTEXT,
    "wx.SYS_COLOUR_INFOBK": wx.SYS_COLOUR_INFOBK,
    "wx.SYS_COLOUR_DESKTOP": wx.SYS_COLOUR_DESKTOP,
    "wx.SYS_COLOUR_3DFACE": wx.SYS_COLOUR_3DFACE,
    "wx.SYS_COLOUR_3DSHADOW": wx.SYS_COLOUR_3DSHADOW,
    "wx.SYS_COLOUR_3DHIGHLIGHT": wx.SYS_COLOUR_3DHIGHLIGHT,
    "wx.SYS_COLOUR_3DHILIGHT": wx.SYS_COLOUR_3DHILIGHT,
    "wx.SYS_COLOUR_BTNHILIGHT": wx.SYS_COLOUR_BTNHILIGHT,
    "wx.SYS_COLOUR_LISTBOX": wx.SYS_COLOUR_LISTBOX,
}


class ColorPanel(wal.ScrolledPanel):
    def __init__(self, parent):
        wal.ScrolledPanel.__init__(self, parent)
        keys = WX_COLORS.keys()
        keys.sort()
        grid = wal.GridPanel(self, len(keys), 2, 10, 10)
        for item in keys:
            grid.pack(wal.Label(grid, item))
            panel = wal.VPanel(grid)
            panel.set_bg(wal.BLACK)
            color_panel = wal.VPanel(panel)
            color_panel.pack((80, 30))
            color_panel.set_bg(wx.SystemSettings.GetColour(WX_COLORS[item]).Get() if wal.IS_WX4
                               else wx.SystemSettings_GetColour(WX_COLORS[item]).Get())
            panel.pack(color_panel, padding_all=1)
            grid.pack(panel)
        self.pack(grid, padding=10)


app = wal.Application('wxWidgets')
mw = wal.MainWindow(app, 'wxpython colors', (450, 550))
top_panel = wal.VPanel(mw)
mw.pack(top_panel, expand=True, fill=True)
panel = ColorPanel(top_panel)
top_panel.pack(panel, expand=True, fill=True)
app.mw = mw
app.run()
