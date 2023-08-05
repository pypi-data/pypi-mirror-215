from zennin.quotebook import QuoteBook
import random
import argparse
import os
import subprocess

CONFIG_FOLDER = os.path.expanduser("~/.config/zennin")
CONFIG_FILE_PATH = os.path.join(CONFIG_FOLDER, "quotebook.txt")
EXAMPLE_FILE_PATH = "/usr/share/doc/zennin/quotebook.txt"

QUOTEBOOK_HELP_URL = "https://github.com/Erymer/zennin#quote-book"

DEFAULT_JUSTIFICATION_POSITION = "center"

VERSION_COMMAND = "git describe --tags --abbrev=0 | sed 's/^v//'"

__version__ = subprocess.run(VERSION_COMMAND, shell=True, \
                             capture_output=True, text=True).stdout.strip()
HELP_TEXT = f"""
Print quotes on your terminal.\n
Quotes are grabed from 'Quote Book' file in {CONFIG_FILE_PATH}.\n
To know more about this file please visit {QUOTEBOOK_HELP_URL}.
"""

def main():
    '''
    Main function
    '''
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description=HELP_TEXT)
    parser.add_argument("-j", "--justify",
                        help="Justification position. Accepted values are 'left', 'center', 'right'.",
                        choices=["left", "right", "center"])
    parser.add_argument("-f", "--file", help="Specify 'Quote Book' path")
    parser.add_argument("-p", "--print", help="Print a designated quote from the 'Quote Book' based on its position number.", type=int)
    parser.add_argument("-n", "--number",
                        help="Prints quote quantity in your 'Quote Book'",
                        action="store_true")

    args = parser.parse_args()

    if args.justify == "center":
        justification_position = "center"
    elif args.justify == "right":
        justification_position = "right"
    elif args.justify == "left":
        justification_position = "left"
    else:
        justification_position = DEFAULT_JUSTIFICATION_POSITION

    if args.file:
        file_path = args.file
    else:
        file_path = CONFIG_FILE_PATH

    try:
        zennin = QuoteBook(file_path)
    except FileNotFoundError:
        try:
            zennin = QuoteBook(EXAMPLE_FILE_PATH)
            print(f"{file_path} Doesn't exist. Using example file")
        except FileNotFoundError:
            print("No 'Quote Book' file found")
            print(f"For more information about this file please visit {QUOTEBOOK_HELP_URL}")
            exit(1)

    if args.number:
        print(f"You have {zennin.quotes_quantity} quotes in your Quote Book")
        exit(0)

    if args.print:
        quote_num = args.print
    else:
        quote_num=random.randint(1, zennin.quotes_quantity)

    try:
        zennin.print_quote(quote_num, justification_position)
    except IndexError:
        print("Quote number outside of scope")
        print(f"You have {zennin.quotes_quantity} quotes")
        exit(1)


if __name__ == "__main__":
    main()
