
__version__ , __license__ , __copyright__ = "0.1" , "GPLv3 license" , f"\nCopyright (C) 2023 \nMohammad Mehrabi and amir kamankesh <github.com/OnlyRad>\n"

def welcome(text, time:float=0.035):
    from time import sleep
    try:
        from rich import print as Print
        Print(text)
    except ModuleNotFoundError:
        for char in text:
            print(char, end='', flush=True)
            sleep(float(time))
    print()