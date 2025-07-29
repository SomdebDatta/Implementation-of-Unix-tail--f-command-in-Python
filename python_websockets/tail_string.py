import os
import time

class Tail:
    def __init__(self, filename, n=5, s=0.5):
        self.filename = filename
        self.lines_limit = n
        self.secs = s
        self.last_modified_time = None
        self.last_n_lines = ''
        self.eof_pos = -1

    def get_last_modified_time(self):
        return os.path.getmtime(self.filename)

    def check_file_modified(self):
        if self.last_modified_time == self.get_last_modified_time():
            # print(f'No modifications in {self.filename}...')
            return False

        if not self.last_modified_time:
            # print(f'Started monitoring {self.filename}...')
            self.last_modified_time = self.get_last_modified_time()
            return True

        # This means self.last_modified_time != get_last_modified_time
        # print(f'File {self.filename} was modified in the last {self.secs} seconds!')
        self.last_modified_time = self.get_last_modified_time()
        return True


    def yield_last_n_lines(self):
        self.last_n_lines = ''
        lines = 0

        with open(self.filename, 'rb') as file:
            file.seek(0, os.SEEK_END)
            last_eof_pos = self.eof_pos
            curr_pos, self.eof_pos = file.tell(), file.tell()

            while curr_pos > last_eof_pos:
                file.seek(curr_pos)
                char = file.read(1) # read 1 byte'

                if char == b'\n':
                # if char == os.linesep.encode('utf-8'):
                    lines += 1
                    if lines == self.lines_limit:
                        break
                if char != b'\r':
                    self.last_n_lines = char.decode() + self.last_n_lines
                curr_pos -= 1
        yield self.last_n_lines

    def start_tailing(self):
        while True:
            if self.check_file_modified():
                for lines in self.yield_last_n_lines():
                    print(lines)
            time.sleep(self.secs)


if __name__ == '__main__':
    t = Tail('hello.txt', n=5)
    t.start_tailing()
    # t.yield_last_n_lines()
