# -*- coding: utf-8 -*-

"""
This class simplifies the use of some os functions
like run a command, and get the output, etc.
"""

import os
import subprocess
import psutil
import screeninfo
import platform

def get_winfo(screen_num=None):
    """
    Get screen info.

    screen_num: Number of screen if it exists.
    """
    screens = screeninfo.get_monitors()

    if screen_num == None:
        return screens

    if len(screens) > screen_num:
        return screens[screen_num]
    else:
        return None

def get_osinfo():
    """
    Returns a tuple containing info
    about the system running.
    """
    return platform.uname()

def run_cmd(cmd, output=False):
    """
    Runs a command.

    If output, returns the output.
    """
    output_string = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE
    ).stdout.read().decode()

    if output:
        return output_string

def main():
    print(get_osinfo())
    print(get_winfo())

if __name__ == "__main__":
    main()
