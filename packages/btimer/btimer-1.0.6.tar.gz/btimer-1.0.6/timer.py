#!/usr/bin/env python

import subprocess
import sys
import random
import time

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress

verses = {
    0: {
        'quote': 'Self love brings happiness.',
        'author': 'Thich Nhat Hanh'
    },
    1: {
        'quote': 'There is no way to happiness, happiness is the way.',
        'author': 'Thich Nhat Hanh'
    },
    2: {
        'quote': 'Happiness is in the here and now.',
        'author': 'Thich Nhat Hanh'
    }
}

def count_down(t: any) -> None:
    console = Console()
    with Progress() as progress:
        task1 = progress.add_task("", total=t, transient=True)

        while not progress.finished:
            progress.update(task1, advance=1)
            time.sleep(1)

    console.print("\n")


def print_quotes() -> None:
    console = Console()

    randint = random.randint(0, 2)
    quote = verses[randint]
    console.print(Panel(""" "{}" - {} """.format(quote['quote'], quote['author']), title="Verses"))


def active_window() -> None:
    applescript = """
    tell application "Terminal"
        activate
    end tell
    """
    subprocess.call("osascript -e '{}'".format(applescript), shell=True)


def main() -> None:
    try:
        val = input("Enter the number of minutes: ")
        count_down(int(val) * 60)
    except KeyboardInterrupt:
        # Signal can not handler sleep
        sys.exit(0)

    active_window()
    print_quotes()


if __name__ == '__main__':
    main()
