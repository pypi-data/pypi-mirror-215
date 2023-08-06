import errno
import os

class FileReader:

    def __init__(self, filepath):
        self.filepath = filepath
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                self.content = f.readlines()
                self.content = [line.replace("\n", "").replace("\r", "") for line in self.content]
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.filepath)

    def read_all_lines(self):
        return self.content

