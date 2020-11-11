# The test should show two
# color button on the main window

import wal

SIZE = (300, 300)


class MW(wal.MainWindow):

    def __init__(self):
        wal.MainWindow.__init__(self)
        self.set_size(SIZE)
        cb1 = wal.ColorButton(self, (0.1, 1.0, 0.0))
        self.pack(cb1, padding=10)
        cb2 = wal.ColorButton(self, (255, 0, 125), onchange=self.on_click)
        self.pack(cb2, padding=10)
        cb2.set_value((0.0, 0.1, 0.9))
        cb1.set_value255((255, 255, 0))

    def on_click(self):
        print('Works!')


MW().run()