import os
import time
from collections import deque


class Tail:
    def __init__(self, filename, n=5, s = 3):
        self.filename = filename
        self.lines_limit = n
        self.secs = s
        self.last_modified_time = None
        self.last_n_lines = deque()
        self.eof_pos = 0


    def get_last_modified_time(self):
        return os.path.getmtime(self.filename)


    def check_file_modified(self):
        if self.last_modified_time == self.get_last_modified_time():
            print(f'No modifications in {self.filename}...')
            return False

        if not self.last_modified_time:
            print(f'Started monitoring {self.filename}...')
            self.last_modified_time = self.get_last_modified_time()
            return True

        # This means self.last_modified_time != get_last_modified_time
        print(f'File {self.filename} was modified in the last {self.secs} seconds!')
        self.last_modified_time = self.get_last_modified_time()
        return True

    def yield_last_n_lines(self):
        if self.check_file_modified():
            with open(self.filename, 'rb') as file:
                file.seek(0, os.SEEK_END)

                last_eof_pos = self.eof_pos
                curr_pos, self.eof_pos = file.tell(), file.tell()
                line = b''
                while curr_pos >= last_eof_pos:
                    file.seek(curr_pos)
                    char = file.read(1) # read 1 byte
                    if char == b'\n':
                        if line and line != b'\r':
                            yield line[::-1].decode()
                            line = b''
                    else:
                        line += char
                    curr_pos -= 1
                if line and line != b'\r':
                    yield line[::-1].decode()


    def print_last_n_lines(self):
        ct = 0
        curr_last_lines = deque()

        for line in self.yield_last_n_lines():
            print(f'line fetched - {line}')
            curr_last_lines.appendleft(line)
            if len(self.last_n_lines) + len(curr_last_lines) > self.lines_limit:
                self.last_n_lines.popleft()
            ct += 1
            if ct == self.lines_limit:
                break

        self.last_n_lines.extend(curr_last_lines)

        # for line in self.last_n_lines:
        #     print(line)

        print(f'all lines - {self.last_n_lines}')


    def start_tailing(self):
        while True:
            self.print_last_n_lines()
            time.sleep(self.secs)


if __name__ == '__main__':
    t = Tail('../hello.txt')
    t.start_tailing()