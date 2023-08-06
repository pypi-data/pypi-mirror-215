from datetime import datetime
from colorama import Fore as f

__version__ , __license__ , __copyright__ = "0.1" , "GPLv3 license" , f" Copyright (C) {datetime.now().year} \namir kamankesh and Mohammad Mehrabi Rad <github.com/onlyrad>"


def welcome(text, time:float=0.5):
    from time import sleep
    try:
        from rich import print as Print
        Print(text)
    except ModuleNotFoundError:
        for char in text:
            print(char, end='', flush=True)
            sleep(float(time))
    print()
