# The test should show buttons to launch
# different system dialogs

import wal

SIZE = (300, 300)


class MW(wal.MainWindow):

    def __init__(self):
        wal.MainWindow.__init__(self)
        self.set_size(SIZE)
        self.pack(wal.Button(self, 'get_open_file_name', onclick=self.get_open_file_name), padding=10)
        self.pack(wal.Button(self, 'get_save_file_name', onclick=self.get_save_file_name), padding=10)
        self.pack(wal.Button(self, 'get_dir_path', onclick=self.get_dir_path), padding=10)

    def get_open_file_name(self):
        print(wal.get_open_file_name(self))

    def get_save_file_name(self):
        print(wal.get_save_file_name(self, '~/test.txt'))

    def get_dir_path(self):
        print(wal.get_dir_path(self))


MW().run()
