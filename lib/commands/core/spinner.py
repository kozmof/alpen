# coding: utf-8
import os
import time
import threading
import sys, itertools
import subprocess

# Based on https://stackoverflow.com/questions/4995733/how-to-create-a-spinning-command-line-cursor

class Spinner:
    def __init__(self, statement=""):
        self.run = False
        # self.motions = "⣾⣽⣻⢿⡿⣟⣯⣷"
        # self.motions = "▖ ▘ ▝ ▗"
        self.motions = "|/_\\_"
        self.delay = 0.03
        self.statement = statement
        self.thread = None

    def spin(self):
        cycles1 = itertools.cycle(self.motions)
        while self.run:
            text = f"{next(cycles1)} {self.statement}"
            sys.stdout.write(text)
            time.sleep(self.delay)
            sys.stdout.flush()
            sys.stdout.write('\b' * len(text))

    def __enter__(self):
        subprocess.run(["clear"])
        self.run = True
        self.thread = threading.Thread(target=self.spin)
        self.thread.start()
        return self

    def __exit__(self, exception, value, tb):
        self.run = False
        sys.stdout.flush()
        subprocess.run(["clear"])

    def change(self, statement):
        self.statement = statement
        sys.stdout.flush()
        subprocess.run(["clear"])


if __name__ == "__main__":
    # demo
    with Spinner("testing...") as s:
        time.sleep(2)
        s.change("statement is changed...")
        time.sleep(5)