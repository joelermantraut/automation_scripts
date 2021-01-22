# -*- coding:utf-8 -*-

"""
Class to simplify printing with colors on terminal.
"""

class Printer(object):
    """Class to simplify printing with colors on terminal."""
    def __init__(self):
        self.text_colors = {
            "black": "30",
            "red": "31",
            "green": "32",
            "yellow": "33",
            "blue": "34",
            "purple": "35",
            "cyan": "36",
            "white": "37"
        }
        self.back_colors = {
            "black": "40",
            "red": "41",
            "green": "42",
            "yellow": "43",
            "blue": "44",
            "purple": "45",
            "cyan": "46",
            "white": "47"
        }

    def pre_string(self, text_color="black", back_color="black"):
        """
        Receives a color or indication and returns the
        formatted "pre string" to put before the
        string to format.
        """
        return "\033[{};{}m".format(
                self.text_colors[text_color],
                self.back_colors[back_color]
            )

    def print_c(self, text, text_color="black", back_color="black"):
        """
        Prints with the given format.
        """
        print(self.pre_string(text_color, back_color) + text)

def main():
    Printer().print_c("hello", text_color="red", back_color="blue")

if __name__ == "__main__":
    main()
