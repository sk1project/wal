import os
import sys

parent = os.path.dirname
cur_path = os.path.abspath(os.getcwd())
wal_path = os.path.join(parent(parent(cur_path)), 'src')
sys.path.insert(0, wal_path)


import wal


class ColorPanel(wal.ScrolledPanel):
    def __init__(self, parent):
        wal.ScrolledPanel.__init__(self, parent)
        keys = wal.UI_COLORS.keys()
        grid = wal.GridPanel(self, len(keys), 2, 10, 10)
        for item in keys:
            grid.pack(wal.Label(grid, item))
            panel = wal.VPanel(grid)
            panel.set_bg(wal.BLACK)
            color_panel = wal.VPanel(panel)
            color_panel.pack((80, 30))
            color_panel.set_bg(wal.UI_COLORS[item])
            panel.pack(color_panel, padding_all=1)
            grid.pack(panel)
        self.pack(grid, padding=10)


app = wal.Application('wxWidgets')
mw = wal.MainWindow(app, 'WAL colors', (350, 550))
top_panel = wal.VPanel(mw)
mw.pack(top_panel, expand=True, fill=True)
panel = ColorPanel(top_panel)
top_panel.pack(panel, expand=True, fill=True)
app.mw = mw
app.run()
