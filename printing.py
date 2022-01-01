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
        self.max_string = 10
        self.max_spaces = 10

    def _format_string(self, string, max_length, spacing):
        """
        Defines spaces to show as a table and limits
        characters to show.
        """
        if len(string) > max_length - 2:
            string = string[:max_length - 2] + "..."

        string = string.ljust(spacing)

        return string

    def color_print(self, text, foreground="white", background="grey", styles=None):
        text = colored(text, foreground, "on_" + background, attrs=styles)
        print(text)

    def special_print(self, struct):
        """
        Prints an object in a special way, for simplified view.

        for lists, prints each element in a line.
        """
        if type(struct) == list:
            for item in struct:
                print(item)
        elif type(struct) == dict:
            keys = list(struct.keys())
            len_chars_numbers = len(str(len(keys)))

            for key, value in struct.items():
                index = keys.index(key)
                print("{:<5} {} {}".format(
                    index,
                    self._format_string(key, self.max_string, self.max_spaces),
                    self._format_string(value, self.max_string, self.max_spaces)
                ))
        else:
            print(struct)

def main():
    Printer().color_print("hello", "red", "green", ["concealed"])
    Printer().special_print({
        "hello": "bye",
        "red": "blue",
        "black": "white"
    })

if __name__ == "__main__":
    main()
