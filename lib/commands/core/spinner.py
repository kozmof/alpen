"""Threading spinner
"""
import os
import time
import threading
import sys, itertools
import subprocess
from __future__ import annotations


class Spinner:
    # Based on https://stackoverflow.com/questions/4995733/how-to-create-a-spinning-command-line-cursor
    def __init__(self, statement: str="", delay=0.03) -> None:
        """Use `with` statement when initializing

        Args:
            statement (str, optional): A text of the right side of the spinner. Defaults to "".
            delay (str, optional): Adjust a motion speed
        """
        self.run = False
        self.motions = "|/_\\_"
        self.delay = delay
        self.statement = statement
        self.thread = None

    def spin(self) -> None:
        """Process spinning
        """
        cycles1 = itertools.cycle(self.motions)
        while self.run:
            text = f"{next(cycles1)} {self.statement}"
            sys.stdout.write(text)
            time.sleep(self.delay)
            sys.stdout.flush()
            sys.stdout.write('\b' * len(text))

    def __enter__(self) -> Spinner:
        """Start threading

        Returns:
            Spinner: Reference of this instance
        """
        subprocess.run(["clear"])
        self.run = True
        self.thread = threading.Thread(target=self.spin)
        self.thread.start()
        return self

    def __exit__(self, exception, value, tb) -> None:
        """Clear buffer and a terminal
        """
        self.run = False
        sys.stdout.flush()
        subprocess.run(["clear"])

    def change(self, statement: str) -> None:
        """Change a text to show

        Args:
            statement (str): text to show in the right side of the spinner
        """
        self.statement = statement
        sys.stdout.flush()
        subprocess.run(["clear"])


if __name__ == "__main__":
    # demo
    with Spinner("testing...") as s:
        time.sleep(2)
        s.change("statement is changed...")
        time.sleep(5)