# -*- coding: utf-8 -*-

"""
Class to simplify use of regular expressions
functions. It is not to simplify use of
regular expressions itself. It is needed
to know how to use them. But it simplifies
the use of functions findall, search and
match.
"""

import re

def analyse(string, pattern, use_all=False):
    """
    Analyses the regex and returns the
    result as a list.

    If time matters, then use "search".
    If not, run findall, with use_all param.

    This is because usually findall is slower.
    """
    if use_all:
        # Find all ocurrences
        result = re.findall(pattern, string)
    else:
        result = re.search(pattern, string)

        if result == None:
            result = []
        else:
            result = result.groups()

    return result

def main():
    print(analyse("hi everyone", r'\s', use_all=True))

if __name__ == "__main__":
    main()
