#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Class that simpifies the reading of PDFs.
"""

import PyPDF2
import re

class PDFUse(object):
    """Class that simpifies the reading of PDFs."""
    def __init__(self, filename):
        super(PDFUse, self).__init__()
        self.filename = filename
        self.init()

    def init(self):
        """
        Generates the object and decrypts.
        """
        self.pdf = PyPDF2.PdfFileReader(self.filename)

        if self.pdf.isEncrypted:
            self.pdf.decrypt('')

    def is_valid(self):
        """
        Does an operation to know if the PDF file can be use with
        this module.
        """
        try:
            self.pdf.getDocumentInfo()

            result = True
        except:
            result = False

        return result

    def get_number_of_pages(self):
        """
        Returns the total amount of pages.
        """
        return self.pdf.getNumPages()

    def get_info(self):
        """
        Returns the base info of the document, if it has.
        """
        return self.pdf.getDocumentInfo()

    def get_fields(self):
        """
        Returns interactive content.
        """
        return self.pdf.getFields()

    def get_content(self, page_num, regex=None):
        """
        Returns the content of the page.

         - If regex != None, returns compatible content with
           the regular expression.
        """
        page_content = self.pdf.getPage(page_num).extractText()

        if regex:
            page_content = re.findall(regex, page_content)
        
        return page_content

def main():
    filename = "book.pdf"

    pdf_class = PDFUse(filename)

    print(pdf_class.get_content(100, r".*"))

if __name__ == "__main__":
    main()
