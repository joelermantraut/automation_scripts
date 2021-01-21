#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Class to simplify WEB scrapping.

Uses Selenium with Chrome Driver.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
# Selenium imports
from time import sleep
# Standard Python

class WebScrapper(object):
    """Class to simplify WEB scrapping"""
    def __init__(self, PATH, url):
        super(WebScrapper, self).__init__()
        self.PATH = PATH
        # Direccion donde esta guardado ChromeDriver
        self.url = url
        self.find_methods = [
            By.ID,
            By.XPATH,
            By.LINK_TEXT,
            By.PARTIAL_LINK_TEXT,
            By.NAME,
            By.TAG_NAME,
            By.CLASS_NAME,
            By.CSS_SELECTOR
        ]
        self.modifier_strings = {
            "ctrl": Keys.CONTROL,
            "alt": Keys.ALT,
            "shift": Keys.SHIFT,
        }
        self.special_strings = {
            "enter": Keys.RETURN,
            "arrow_down": Keys.ARROW_DOWN,
            "arrow_up": Keys.ARROW_UP,
            "arrow_left": Keys.ARROW_LEFT,
            "arrow_right": Keys.ARROW_RIGHT,
            "backspace": Keys.BACKSPACE,
            'page_up': Keys.PAGE_UP,
            'page_down': Keys.PAGE_DOWN,
            "delete": Keys.DELETE,
            "escape": Keys.ESCAPE,
            "space": Keys.SPACE,
            "tab": Keys.TAB,
            "equal": Keys.EQUALS,
            "home": Keys.HOME,
            "insert": Keys.INSERT,
            "F1": Keys.F1,
            "F2": Keys.F2,
            "F3": Keys.F3,
            "F4": Keys.F4,
            "F5": Keys.F5,
            "F6": Keys.F6,
            "F7": Keys.F7,
            "F8": Keys.F8,
            "F9": Keys.F9,
            "F10": Keys.F10,
            "F11": Keys.F11,
            "F12": Keys.F12,
        }
        self.init()

    def init(self):
        """
        Inits WebDriver.
        """
        self.driver = webdriver.Chrome(self.PATH)
        self.driver.get(self.url)

    def quit(self):
        """
        Closes ChromeDriver.
        """
        self.driver.quit()

    def get_title(self):
        """
        Gets site title.
        """
        return self.driver.title

    def maximize(self):
        """
        Maximize window.
        """
        self.driver.maximize_window()

    def refresh(self):
        """
        Refresh page.
        """
        self.driver.refresh()

    def get_elements(self, selector, roots=None):
        """
        Gets object and return it.

        IMPORTANT:
            - If is given root, use it instead of root.
            - Else, use the driver.
            - Uses CSS selectors.
        SOURCE:
        https://selenium-python.readthedocs.io/locating-elements.html
        """
        if roots == None:
            roots = self.driver

        if type(roots) is not list:
            roots = [roots]

        new_roots = []
        for root in roots:
            new_roots += root.find_elements_by_css_selector(selector)

        return new_roots

    def process_keys(self, element, key):
        """
        Decides with keys press.

         - If it receives a combination, like key + key, get the
           modifiers, and presses it while tapping the other.
        """
        if '+' in key and len(key) > 1:
            keys = key.split('+')

            for key in keys: # Useful for any number of modifiers 
                if key in self.modifier_strings.keys():
                    key = self.modifier_strings[key]
                    ActionChains(self.driver).key_down(key).perform()
                # Gets Selenium Object 
                else:
                    if element is None:
                            ActionChains(self.driver).send_keys(key).perform()
                    else:
                            ActionChains(self.driver).send_keys_to_element(element, key).perform()

            for key in keys:
                if key in self.modifier_strings.keys():
                    key = self.modifier_strings[key]
                    ActionChains(self.driver).key_up(key).perform()
            # Releases all modifiers pressed

        else:
            if key in self.modifier_strings.keys():
                key = self.modifier_strings[key]
            elif key in self.special_strings.keys():
                key = self.special_strings[key]
            # Verifies if key is a special key

            if element is None:
                ActionChains(self.driver).send_keys(key).perform()
            else:
                ActionChains(self.driver).send_keys_to_element(element, key).perform()

    def send_keys(self, elements, keys_list):
        """
        Receives a list of keys and executes each one.

         - If it receives a number, it will be a delay up to next press.
         - To send a number, it must receives it as a string.
         - If element is a list, executes each one.
        """
        if type(elements) is not list:
            elements = [elements]
        if type(keys_list) is not list:
            keys_list = [keys_list]

        for element in elements:
            for key in keys_list:
                if type(key) is int:
                    sleep(key)
                else:
                    self.process_keys(element, key)

    def click_elements(self, elements=None, times=1):
        """
        Clicks the element given:

            - If receives a list, clicks each one.
            - Times: Number of times of clicking.
            - Times == 0: Presses and retains.
            - If doesn't receive element, click in the current position.
        """
        if type(elements) is not list:
            elements = [elements]

        for element in elements:
            if times == 0:
                ActionChains(self.driver).click_and_hold(element).perform()
            else:
                try:
                    for i in range(times):
                        ActionChains(self.driver).click(element).perform()
                        sleep(0.1) # 100ms
                except Exception:
                    pass
                # Exception for element which dissapear after
                # an action.

    def move_mouse_to_element(self, element):
        """
        Moves the mouse to the middle of the element given.

         - If element is a list of len > 1, does nothing.
        """

        if type(element) is list and len(element) > 1:
            return
        elif type(element) is list:
            element = element[0]
        elif type(element) is str:
            element = self.get_elements(element)[0]

        ActionChains(self.driver).move_to_element(element).perform()

    def scroll_to_element_class(self, element):
        """
        Scrolls up to set a element_class in view position.
        """
        self.scripting("document.getElementByClassName('{0}').scrollIntoView();".format(element))

    def clear_content(self, elements):
        """
        Clears input, textarea, etc.
        """

        if type(elements) is not list:
            elements = [elements]

        for element in elements:
            element.clear()

    def screenshot(self, elements, filename=None):
        """
        Takes a screenshot of the element given.

         - If element is a list, repeats with each one.
         - If any of the capture returns False, the function returns False.
         - If it doesn't receives a name, use internal format.
        """

        if type(elements) is not list:
            elements = [elements]

        for element in elements:
            i = elements.index(element)
            if i == 0:
                element.screenshot(filename + '.png')
            else:
                element.screenshot(filename + str(i) + '.png')

    def remove_elements(self, elements):
        """
        Remove an element or a list of elements from the DOM.
        """
        if elements is not list:
            elements = [elements]

        for element in elements:
            class_name = self.get_properties("class", element)[0]
            self.scripting("return document.\
                getElementsByClassName('{}')[0].remove();".format(class_name))

    def get_properties(self, name, elements=None):
        """
        Gets properties or attributes of the element.

         - If element == None, if the driver.
         - If it doesn't exists, return None.
        """
        if elements == None:
            elements = self.driver
        elif type(elements) is not list:
            elements = [elements]

        attributes = []
        for element in elements:
            if name == 'display':
                attributes.append(element.is_displayed())
            elif name == 'enabled':
                attributes.append(element.is_enabled())
            elif name == 'selected':
                attributes.append(element.is_selected())
            else:
                properties = self.get_all_properties(elements)[0]
                if name in properties:
                    attributes.append(properties[name])

        return attributes

    def get_all_properties(self, elements=None):
        """
        Gets all properties of the element.

         - If the argument is a list of elements, does the same
           for each one.
         - If no element is given, use the driver.
        """
        properties = list()

        if elements == None:
            elements = self.driver
        elif type(elements) is not list:
            elements = [elements]

        for element in elements:
            properties.append(self.driver.execute_script(' \
                    var items = {}; \
                    for (index = 0; index < arguments[0].attributes.length; ++index) { \
                        items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value \
                    }; \
                    return items;',
                    element))

        return properties

    def scripting(self, code=None, filename=None):
        """
        Executes a JS script.

         - If code is a list, executes each one.
        """
        if filename != None:
            file = open(filename, 'r')
            code = file.read()
            file.close()

        script_response = None

        if type(code) is list:
            script_response = list()
            for script in code:
                response = self.driver.execute_script(script)
                script_response.append(response)
        else:
            script_response = self.driver.execute_script(code)

        return script_response

def main():
    scrapper = WebScrapper(
        "/home/joel/Apps/chromedriver",
        "https://www.youtube.com"
    )

    element = scrapper.get_elements(".ytd-rich-shelf-renderer")[0]

    sleep(5)

    scrapper.quit()

if __name__ == "__main__":
    main()
