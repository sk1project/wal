# The test should generate six colored
# rectangles on the main window

import os
import wx

import wal

SIZE = (300, 400)

parent = os.path.dirname
IMG_FOLDER = os.path.join(parent(parent(os.path.abspath(__file__))), 'images')


class ListItem(object):
    name = ''
    title = ''
    icon = ''


class MW(wal.MainWindow):

    def __init__(self):
        wal.MainWindow.__init__(self)
        self.set_size(SIZE)

        item = ListItem()

        item.icon = wx.Image(
            os.path.join(IMG_FOLDER, 'general_32.png')).ConvertToBitmap()
        item.name = 'Main text'
        item.title = 'Secondary text description'
        data = [item] * 5

        self.prefs = wal.PrefsList(self, data=data, on_select=self.click)
        self.pack(self.prefs, fill=True, expand=True, padding=10)

    def click(self, *args):
        print('CLICKED', self.prefs.get_selected_index())


MW().run()
