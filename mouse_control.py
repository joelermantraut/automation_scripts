# -*- coding: utf-8 -*-

"""

Class to simplify the use of the mouse.

TODO:

    - Añadir las funciones de monitoreo.

"""

from pynput import mouse
from screeninfo import get_monitors

class MouseControl(object):
    """Class to simplify the use of the mouse"""

    def __init__(self):
        super(MouseControl, self).__init__()

        self.mouse_buttons = {
            'left': mouse.Button.left,
            'middle': mouse.Button.middle,
            'right': mouse.Button.right
        }
        self.init()

    def init(self):
        """
        Runs some init functions.

         - Inits controller.
        """
        self.controller = mouse.Controller()

    def mouse_move(self, move=None, rel=False, drag=False, function=None, iters=1):
        """"
        Moves the mouse taking care of:

            - If receives a function, executes it before each cycle.
            - If rel, enables relative move.
            - If drag, moves the mouse with the left button pressed.
            - If move == None, return the current position of the mouse.
        """

        if move == None:
            return self.controller.position()

        if drag:
            self.controller.press(mouse.Button.left)
            if rel:
                self.controller.move(*move)
            else:
                self.controller.position = move

            self.controller.release(self.mouse_buttons['left'])

        if function:
            for i in range(iters):
                x, y = function()
                self.controller.position = (x, y)
        else:
            if rel:
                self.controller.move(*move)
            else:
                self.controller.position = move

    def click(self, button, clicks=1):
        """
        Click in the current position of the mouse. 
        """

        button = self.mouse_buttons[button]

        self.controller.click(button, clicks)

    def scroll(self, amount, percent=False):
        """
        Scrolls up or down.

         - If percent, moves that percent of the screen.
        """
        if percent:
            first_monitor_height = get_monitors()[0].height

            amount = (amount // 100) * first_monitor_height

        self.controller.scroll(0, -amount)

def main():
    mouse_controller = MouseControl()

    mouse_controller.mouse_move((0, 0))

if __name__ == "__main__":
    main()
