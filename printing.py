# -*- coding:utf-8 -*-

"""
Class to simplify printing with colors on terminal.
"""

from termcolor import colored

class Printer(object):
    """Class to simplify printing with colors on terminal."""
    def __init__(self):
        self.text_colors = [
            "grey",
            "red",
            "green",
            "yellow",
            "blue",
            "magenta",
            "cyan",
            "white"
        ]
        self.back_colors = [
            "grey",
            "red",
            "green",
            "yellow",
            "blue",
            "magenta",
            "cyan",
            "white"
        ]
        self.attributes = [
            "bold",
            "dark",
            "underline",
            "blink",
            "reverse",
            "concealed" # hidden
        ]

    def color_print(self, text, foreground="white", background="grey", styles=None):
        text = colored(text, foreground, "on_" + background, attrs=styles)
        print(text)

    def special_print(self, struct):
        """
        Prints an object in a special way, for simplified view.
        """
        if type(struct) == list:
            for item in struct:
                print(item)

def main():
    Printer().color_print("hello", "red", "green", ["concealed"])
    Printer().special_print(["hola", "que", "tal"])

if __name__ == "__main__":
    main()
