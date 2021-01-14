#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Clase que facilita la lectura de PDFs.
"""

import PyPDF2
import re

class PDFUse(object):
    """Clase que facilita la lectura de PDFs."""
    def __init__(self, filename):
        super(PDFUse, self).__init__()
        self.filename = filename
        self.init()

    def init(self):
        """
        Genera el objeto y lo desencripta.
        """
        self.pdf = PyPDF2.PdfFileReader(self.filename)

        if self.pdf.isEncrypted:
                self.pdf.decrypt('')

    def is_valid(self):
        """
        Realiza una operacion para saber si el PDF mantiene una
        estructura valida. De no ser asi, su uso se va a tornar
        imposible, generando excepciones para cualquier operacion.
        """
        try:
                self.pdf.getDocumentInfo()

                result = True
        except:
                result = False

        return result

    def get_number_of_pages(self):
        """
        Devuelve la cantidad total de paginas del PDF.
        """
        return self.pdf.getNumPages()

    def get_info(self):
        """
        Devuelve la informacion base del documento, si la tiene.
        """
        return self.pdf.getDocumentInfo()

    def get_fields(self):
        """
        Retorna contenido interactivo.
        """
        return self.pdf.getFields()

    def get_content(self, page_num, regex=None):
        """
        Devuelve el contenido de la pagina.

         - Si regex es distinto de None, devuelve el contenido
           compatible con la expresion regular.
        """
        page_content = self.pdf.getPage(page_num).extractText()

        if regex:
                page_content = re.findall(regex, page_content)
        
        return page_content

def main():
    filename = "libro.pdf"

    pdf_class = PDFUse(filename)

    print(pdf_class.get_content(100, r".*"))

if __name__ == "__main__":
    main()
