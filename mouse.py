# -*- coding: utf-8 -*-

"""

Module created to simplify the use of mouse.

Maybe it could have problems with X.


TODO: 

 - Programar la preparacion de cadenas
   que representan las teclas apretadas.

 - Tomar en cuenta que AltGr no funciona como
   deberia.
 - Revisar otras combinaciones.

"""

from pynput import keyboard 

class KeyboardControl(object):
    """Class that simplify use of mouse in automation."""

    def __init__(self):
        super(KeyboardControl, self).__init__()
        self.block = False
        self.keyboard_modifiers = [
            keyboard.Key.alt,
            keyboard.Key.alt_gr,
            keyboard.Key.alt_l,
            keyboard.Key.alt_r,
            keyboard.Key.cmd,
            keyboard.Key.cmd_l,
            keyboard.Key.cmd_r,
            keyboard.Key.ctrl,
            keyboard.Key.ctrl_l,
            keyboard.Key.ctrl_r,
            keyboard.Key.shift,
            keyboard.Key.shift_l,
            keyboard.Key.shift_r,
        ]

        self.keyboard_special = [
            keyboard.Key.enter,
            keyboard.Key.backspace,
            keyboard.Key.caps_lock,
            keyboard.Key.delete,
            keyboard.Key.down,
            keyboard.Key.end,
            keyboard.Key.esc,
            keyboard.Key.home,
            keyboard.Key.insert,
            keyboard.Key.left,
            keyboard.Key.media_next,
            keyboard.Key.media_play_pause,
            keyboard.Key.media_previous,
            keyboard.Key.media_volume_down,
            keyboard.Key.media_volume_mute,
            keyboard.Key.media_volume_up,
            keyboard.Key.menu,
            keyboard.Key.num_lock,
            keyboard.Key.page_down,
            keyboard.Key.page_up,
            keyboard.Key.pause,
            keyboard.Key.print_screen,
            keyboard.Key.right,
            keyboard.Key.scroll_lock,
            keyboard.Key.up,
            keyboard.Key.f1,
            keyboard.Key.f2,
            keyboard.Key.f3,
            keyboard.Key.f4,
            keyboard.Key.f5,
            keyboard.Key.f6,
            keyboard.Key.f7,
            keyboard.Key.f8,
            keyboard.Key.f9,
            keyboard.Key.f10,
            keyboard.Key.f11,
            keyboard.Key.f12,
            keyboard.Key.f13,
            keyboard.Key.f14,
            keyboard.Key.f15,
            keyboard.Key.f16,
            keyboard.Key.f17,
            keyboard.Key.f18,
            keyboard.Key.f19,
            keyboard.Key.f20,
            keyboard.Key.space,
            keyboard.Key.tab,
        ]
        self.block_key = "<ctrl>+<esc>"
        self.on_press_f = None
        self.on_release_f = None

    def set_block(self):
        """
        Enables the variable that defines which key
        combination disables the blocking.
        """
        self.block = True

    def prepare_keys(self, key):
        """
        Formats the string that represents the key.
        """
        pass

    def on_press(self, key):
        """
        Function called by the listener to prepare
        the key to be passed to the function given
        as argument.

        Also, this includes the blocking cancel
        key combination listening.
        """
        key = key.__str__()

        #  if self.block and key == self.block_key:
            #  return False

        print(key)

    def on_release(self, key):
        """
        Function called by the listener to prepare
        the key to be passed to the function given
        as argument.
        """
        pass

    def start_listening(
            self,
            on_press_f=None,
            on_release_f=None,
            blocking=False
        ):
        """
        Function that configures the listening using
        arguments to set all properties.
        """
        
        self.on_press_f = on_press_f
        self.on_release_f = on_release_f

        if blocking:
            self.block = True
            with keyboard.Listener(
                on_press=on_press_f,
                on_release=on_release_f
            ) as listener:
                listener.join()
        else:
            listener = keyboard.Listener(
                on_press=on_press_f,
                on_release=on_release_f
            )
            listener.start()

def main():
    keyboard_controller = KeyboardControl()

    keyboard_controller.set_block()

    keyboard_controller.start_listening(blocking=True)

main()
