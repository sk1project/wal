# The test should generate six colored
# rectangles on the main window

import wal

SIZE = (300, 200)


class MW(wal.MainWindow):

    def __init__(self):
        wal.MainWindow.__init__(self)
        self.set_size(SIZE)

        btn = wal.ImageButton(self, text='Test image button', flat=False,
                              onclick=self.click)
        self.pack(btn, padding=10)

    def click(self, *args):
        print 'CLICK'


MW().run()
