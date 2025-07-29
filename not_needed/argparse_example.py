import argparse
import os
import sys
import time


class Tail:
    def __init__(self, filename):
        self.tailed_file = filename
        self.callback = sys.stdout.write


    def follow(self, secs=1):
        with open(self.tailed_file) as file:
            file.seek(0, 2)
            while True:
                curr_pos = file.tell()
                print(curr_pos)
                line = file.readline()
                if not line:
                    file.seek(curr_pos)
                    time.sleep(secs)
                else:
                    self.callback(line)

    def register_callback(self, func):
        self.callback = func


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Print the last lines from a file')
    parser.add_argument('file', type=str, help='File to read from')
    parser.add_argument('-s', type=int, default=5, help='Polling time in secs')
    args = parser.parse_args()

    tail_obj = Tail(args.file)
    tail_obj.follow(args.s)