#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Clase para facilitar el parseo del contenido de una pagina WEB.
"""

import requests
from bs4 import BeautifulSoup
from bs4 import Comment

class WebParsing(object):
    """Clase para facilitar el parseo del contenido de una pagina WEB"""
    def __init__(self, url):
        super(WebParsing, self).__init__()
        self.url = url
        self.page = None
        self.soup = None
        self.init()

    def init(self):
        """
        Inicializa la pagina y el objeto de BeautifulSoup
        """
        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')

    def get_title(self):
        """
        Devuelve el titulo de la pagina en formato texto
        """		
        return self.soup.title.text

    def get_elements(self, selector):
        """
        Obtiene los elementos que corresponden al selector.

         - Emplea selectores CSS.
         - Devuelve una lista, NO un objeto ResultSet
        """
        return [element for element in self.soup.select(selector)]

    def get_family(self, elements):
        """
        Devuelve una lista con:
         - El padre del elemento
         - El elemento
         - El hermano anterior
         - El hermano siguiente

         - Si recibe una lista, realiza el proceso para cada
           elemento de la lista
        """
        if type(elements) is not list:
                elements = [elements]

        new_elements = []
        for element in elements:
                padre = element.parent
                menor = element.find_previous()
                if menor["class"] != padre["class"]:
                        menor = None
                mayor = element.find_next()
                if mayor["class"] != mayor["class"]:
                        mayor = None
                new_elements.append([
                        padre,
                        element,
                        menor,
                        mayor
                ])

        return new_elements

    def get_comments(self, elements):
        """
        Obtiene todos los comentarios del bloque
        de codigo que se le pasa.

         - Si se le pasa una lista realiza el proceso para
           todos los elementos de la lista
        """
        if type(elements) is not list:
                elements = [elements]

        new_elements = []
        for element in elements:
                new_elements.append(self.soup.find_all(string=lambda text: isinstance(text, Comment)))

        return new_elements

    def get_properties(self, elements, properties):
        """
        Devuelve la propiedad o atributo pedido.

         - Le es indistinto si le piden uno u otro
         - Si le pasan una lista realiza el proceso con cada
           elemento de la lista
        """
        if type(elements) is not list:
                elements = [elements]

        if type(properties) is not list:
                properties = [properties]

        new_elements = []
        for element in elements:
                for proper in properties:
                        try:
                                new_elements.append(element[proper])
                                # Para cuando es una propiedad
                        except KeyError as e:
                                new_elements.append(getattr(element, proper))
                                # Para cuando es un atributo

        return new_elements

    def prettify(self, elements):
        """
        Devuelve el mismo contenido pero identado y adaptado
        para ser presentado de forma mas prolija.

         - Si le pasan una lista realiza el proceso con cada
           elemento de la lista
        """
        if type(elements) is not list:
                elements = [elements]

        new_elements = []
        for element in elements:
                new_elements.append(element.prettify())

        return new_elements

def main():
    parser = WebParsing("https://sodocumentation.net/beautifulsoup/topic/1940/locating-elements")

    element = parser.get_elements("li.nav-item a.nav-link")

    print(parser.prettify(element))

if __name__ == "__main__":
    main()
