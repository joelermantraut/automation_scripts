#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Class to simplify parsing of WEB content.
"""

import requests
from bs4 import BeautifulSoup
from bs4 import Comment

class WebParsing(object):
    """Class to simplify parsing of WEB content."""
    def __init__(self, url):
        super(WebParsing, self).__init__()
        self.url = url
        self.page = None
        self.soup = None
        self.init()

    def init(self):
        """
        Inits page and beautifulsoup object.
        """
        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')

    def get_title(self):
        """
        Return page title in text format.
        """
        return self.soup.title.text

    def get_elements(self, selector):
        """
        Get corresponding elements.

         - Use CSS selectors.
         - Returns a list, not ResultSet Object.
        """
        return [element for element in self.soup.select(selector)]

    def get_family(self, elements):
        """
        Return a list with:
            - Parent of element.
            - Element.
            - The next sibling.
            - The previous sibling.

        If it receives a list, does the same process
        with each element.
        """
        if type(elements) is not list:
            elements = [elements]

        new_elements = []
        for element in elements:
            father = element.parent
            lower = element.find_previous()
            if lower["class"] != father["class"]:
                    lower = None
            upper = element.find_next()
            if upper["class"] != upper["class"]:
                    upper = None
            new_elements.append([
                    father,
                    element,
                    lower,
                    upper
                ])

        return new_elements

    def get_comments(self, elements):
        """
        Get all comment of the block of code that is given.

         - if it is given a list, does the same with each
           element.
        """
        if type(elements) is not list:
                elements = [elements]

        new_elements = []
        for element in elements:
            new_elements.append(self.soup.find_all(string=lambda text: isinstance(text, Comment)))

        return new_elements

    def get_properties(self, elements, properties):
        """
        Return the property or attributes require.

         - It is the if is required an attribute or a property.
         - If it receives a list, does the same with each element.
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
                    # Properties
                except KeyError as e:
                    new_elements.append(getattr(element, proper))
                    # Attributes

        return new_elements

    def prettify(self, elements):
        """
        Returns the same content but indented and adapted to
        be presented.

         - If it receives a list, does the same with each element.
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
