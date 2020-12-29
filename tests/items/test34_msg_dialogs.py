# The test should show buttons to launch
# different system dialogs

import wal

SIZE = (300, 300)


class MW(wal.MainWindow):

    def __init__(self):
        wal.MainWindow.__init__(self)
        self.set_size(SIZE)
        self.pack(wal.Button(self, 'msg_dialog', onclick=self.msg_dialog), padding=10)
        self.pack(wal.Button(self, 'error_dialog', onclick=self.error_dialog), padding=10)
        self.pack(wal.Button(self, 'stop_dialog', onclick=self.stop_dialog), padding=10)
        self.pack(wal.Button(self, 'yesno_dialog', onclick=self.yesno_dialog), padding=10)
        self.pack(wal.Button(self, 'ync_dialog', onclick=self.ync_dialog), padding=10)

    def msg_dialog(self):
        wal.msg_dialog(self, 'Message dialog', 'Simple system message dialog')

    def error_dialog(self):
        wal.error_dialog(self, 'Error dialog', 'Simple system error dialog')

    def stop_dialog(self):
        wal.stop_dialog(self, 'Stop dialog', 'Simple system stop dialog')

    def yesno_dialog(self):
        print(wal.yesno_dialog(self, 'Yes|No dialog', 'Simple system yes-no dialog'))

    def ync_dialog(self):
        print(wal.ync_dialog(self, 'Yes|No|Cancel dialog', 'Simple system yes-no-cancel dialog'))


MW().run()