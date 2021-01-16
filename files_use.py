#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Class to simplify use of files.
"""

import glob, os, re
from datetime import datetime

class FileUse(object):
    """Class to simplify use of files"""
    def __init__(self):
        super(FileUse, self).__init__()
        self.dirs = []
        self.files = []

    def list_all(self, path):
        """
        Return all the content recursively.
        """
        for root, dirs, files in os.walk(path):
            for directorio in dirs:
                    self.dirs.append(os.path.abspath(directorio))
            for file in files:
                    self.files.append(os.path.abspath(file))

        return self.dirs, self.files

    def list_dirs(self, filter_re=''):
        """
        Returns all the folder of the root directory.

         - If it receives filter_re as a regular expression, it can
           filter elements that satify the criterion.
        """
        regex = re.compile(filter_re)

        return list(filter(regex.search, self.dirs))

    def list_files(self, filtro=''):
        """
        Returns all the files of the root dir.

         - If it receives filter_re as a regular expression, it can
           filter elements that satify the criterion.
        """
        regex = re.compile(filtro)

        return list(filter(regex.search, self.files))

    def get_files_extensions(self):
        """
        Generates and dict object with each extension as keys,
        and the number of ocurrences of each one as values.
        """
        exts = {}

        for file in self.files:
                ext = re.search(r'\.(.+)$', file).group()
                ext = ext[1:len(ext)]
                if ext not in exts:
                        exts[ext] = 1
                else:
                        exts[ext] += 1

        return exts

    def get_file_info(self, file):
        """
        Receives the complete name of a file and returns:

            - Path.
            - Name itself.
            - Extension.
        """
        path = os.path.dirname(file)

        base = os.path.basename(file)
        name, ext = os.path.splitext(base)

        ext = ext[1:]

        return path, name, ext

    def create_file(self, path="", filename="", extension="", ow=False):
        """
        Creates a empty file:
            - If exists a file with its name:
                - If not ow: Search another name iteratively.
                - If ow: Overwrites it.
            - Return a FILE object.
            - If it not receives a name, generates it with current date.
        """
        if extension == "":
                extension = "txt"

        if filename == "":
                filename = datetime.now().date().__str__() + "." + extension
                filename = filename.replace(" ", "_")

        if path == "":
                path = os.getcwd()

        name = path + '\\' + filename

        if not(ow):
                filename, ext = filename.split('.')[-2], filename.split('.')[-1]
                if ext == "":
                        ext = extension
                name = path + '\\' + filename + '.' + ext
                i = 1
                while os.path.isfile(name):
                        name = path + '\\' + filename + ' (' + str(i) + ').' + ext
                        i += 1

        return open(name, 'w')

def main():
    file_object = FileUse()

    print(file_object.get_file_info("/home/joel/apps/log.txt"))

if __name__ == "__main__":
    main()
