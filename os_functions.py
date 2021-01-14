# -*- coding: utf-8 -*-

"""

This class simplifies the use of some os functions
like run a command, and get the output, etc.

Useful submodules will be os, subprocess, psutil,
screeninfo.

"""

import os
import subprocess
import psutil
import screeninfo

class OSrun(object):
    """Simplfies the use of some os functions"""
    
    def __init__(self):
        super(OSrun, self).__init__()
        self.init()

    def init(self):
        """
        Runs some init functions.
        """
        pass
