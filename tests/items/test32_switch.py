# The test should show two Switch widget
# on the main window

import wal

SIZE = (300, 200)


class MW(wal.MainWindow):

    def __init__(self):
        wal.MainWindow.__init__(self)
        self.set_size(SIZE)
        self.pack((10, 10))

        self.switch = wal.Switch(self, onclick=self.on_change)
        self.pack(self.switch)
        self.pack((10, 10))

        self.switch1 = wal.Switch(self, onclick=self.on_change1)
        self.pack(self.switch1)
        self.pack((10, 10))

        self.switch2 = wal.Switch(self, onclick=self.on_change2)
        self.pack(self.switch2)
        self.switch2.set_enable(False)
        self.pack((10, 10))

        self.switch3 = wal.Switch(self, onclick=self.on_change2)
        self.pack(self.switch3)
        self.switch3.set_enable(False)
        self.switch3.set_value(True)

    def on_change(self):
        print self.switch.get_value()

    def on_change1(self):
        print self.switch1.get_value()

    def on_change2(self):
        print self.switch1.get_value()


MW().run()