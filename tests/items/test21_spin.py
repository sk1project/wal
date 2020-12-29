# The test should show Spin widget
# on the main window

import wal

SIZE = (300, 200)


class MW(wal.MainWindow):
    def __init__(self):
        wal.MainWindow.__init__(self)
        self.set_size(SIZE)

        self.spin = wal.IntSpin(self, 5, (0, 20), width=3,
                                onchange=self.onchange,
                                onenter=self.onenter)
        self.pack(self.spin, padding=5)

        self.spin1 = wal.IntSpin(self, 5, (0, 20), onchange=self.onchange1)
        self.pack(self.spin1, padding=5)

        self.spin2 = wal.FloatSpin(self, 5, (-20.0, 20.0), onchange=self.onchange2)
        self.pack(self.spin2, padding=5)

    def onchange(self):
        print(self.spin.get_value())

    def onenter(self):
        print('onenter', self.spin.get_value())

    def onchange1(self):
        print(self.spin1.get_value())

    def onchange2(self):
        print(self.spin2.get_value())


MW().run()
