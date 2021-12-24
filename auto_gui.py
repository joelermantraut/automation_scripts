#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Class to simplify the use of PyAutoGUI to multiple applications.
"""

import pyautogui
from time import sleep
from files_use import FileUse
from threading import Thread

class AutoGUI(object):
    """Class to simplify the use of PyAutoGUI to multiple applications."""
    def __init__(self):
        super(AutoGUI, self).__init__()
        self.special_keys = [
                "alt", "altleft", "altright", "enter", "ctrl", "ctrlleft", "ctrlright", "capslock",
                "esc", "escape", "up", "down", "left", "right", "shift", "shiftleft", "shiftright",
                "space", "tab"] + ["f" + str(i) for i in range(1, 25)]
        self.init()

    def init(self):
        """
        Inits file control.
        """
        self.files_control = FileUse()

    def send_keys(self, keys_list=None):
        """
        Press keys or write keys_list content.

         - If it receives keys between '+', press modifiers and press
           the last key in the list.
         - If only receives modifiers, retains them.
        """
        if keys_list:
            for key in keys_list:
                if "+" in key and len(key) > 1:
                    keys = key.split("+") # Divide la cadena para obtener las teclas

                    pyautogui.hotkey(*keys)
                elif key in self.special_keys:
                    pyautogui.press(key)
                else:
                    pyautogui.typewrite(key)

    def mouse_move(self, move=None, rel=False, drag=False, function=None, iters=1):
        """
        Moves the mouse.

         - If receives a function, executes the function before each cycle.
         - If rel, enables relative move.
         - If drag, retains press the left button.
         - If move is none, return mouse current position.
        """
        if move == None:
            return pyautogui.position()

        if drag:
            pyautogui.mouseDown()
            if rel:
                pyautogui.moveRel(move[0], move[1])
            else:
                pyautogui.moveTo(move[0], move[1])

            pyautogui.mouseUp()

        if function:
            for i in range(iters):
                x, y = function()
                pyautogui.moveTo(x, y)
        else:
            if rel:
                pyautogui.moveRel(move[0], move[1])
            else:
                pyautogui.moveTo(move[0], move[1])

    def click(self, mode=None, clicks=1):
        """
        Clicks in the position where the mouse is.

        mode: Button to click.
        clicks: number of clicks.
        """

        if mode == None:
            button = 'left'
        else:
            button = mode

        pyautogui.click(button=button, clicks=clicks)

    def scroll(self, amount, percent=False):
        """
        Scrolls up or down.

         - If percent, moves that precentage of screen.
        """
        if percent:
            amount = int((amount / 100) * self.get_screen_properties()[0])

        pyautogui.scroll(amount)

    def get_screen_properties(self):
        """
        Returns screen propierties.
        """
        return list(pyautogui.size())

    def save_screenshot(self, filename=""):
        """
        Get a snapshot and saves it in a file.
        """
        file = self.files_control.create_file(filename, extension = "png")

        return pyautogui.screenshot(file.name)

    def get_on_screen(self, image, confidence=0.5):
        """
        Search for a image on screen.

         - If OpenCV is in use, it enables an advance searching.
         - confidence parameter defines precision of searching. Needs OpenCV.

        If no image was found, returns None.
        """
        try:
            if confidence < 0.9:
                grayscale = True
            else:
                grayscale = False

            coordenadas = pyautogui.locateCenterOnScreen(image, grayscale=grayscale, confidence=confidence)
        except pyautogui.ImageNotFoundException:
            coordenadas = None
        except NotImplementedError:
            coordenadas = pyautogui.locateCenterOnScreen(image, grayscale=grayscale)

        return coordenadas

    def gui_functions(self, kind, options):
        """
        Function that decides which interface use and generates it.
        """
        if kind == "alert":
            result = pyautogui.alert(title=options[0], text=options[1], button=options[2])
        elif kind == "confirm":
            result = pyautogui.confirm(title=options[0], text=options[1], buttons=options[2])
        elif kind == "prompt":
            result = pyautogui.prompt(title=options[0], text=options[1], default=options[2])
        elif kind == "password":
            result = pyautogui.password(title=options[0], text=options[1], default=options[2], mask='*')

        options[3](result)
        # Function called with the answer

    def gui(self, kind, options, asyncronous=False):
        """
        Includes all posible GUI that pyautogui offers in a function.

         - type defines the type of the GUI.
         - options is a list with the needed parameters. If it receives less
           than needed, returns None. If it receives more, use only needed.
        """
        if len(options) != 4:
            return None
        # PyAutoGUI function uses three parameters, the last one is
        # the function which receives the result.

        if asyncronous:
            self.hilo = Thread(target=self.gui_functions, args=(kind, options,))
            self.hilo.start()
        else:
            self.gui_functions(kind, options)

def main():
    autogui = AutoGUI()
    autogui.mouse_move((500, 500))
    autogui.click(mode="right")

if __name__ == "__main__":
    main()
