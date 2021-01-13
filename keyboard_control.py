# -*- coding: utf-8 -*-

"""

Module created to simplify the use of mouse.

Maybe it could have problems with X display.


TODO: 

 - Programar la combinacion con AltGr y 
   la tecla Shift que sea un modificador
   pero que no se incluya en la cadena
   de la tecla.

 - Tambien programar la funcion con CapsLock
   porque no se modifican las teclas presionadas
   como pasa con shift.

 - Tomar en cuenta que AltGr no funciona como
   deberia.
 - Revisar otras combinaciones.

"""

from pynput import keyboard 

class KeyboardControl(object):
    """Class that simplify use of mouse in automation."""

    def __init__(self, alt_gr_map=None):
        super(KeyboardControl, self).__init__()
        self.block = False
        self.modifiers = [
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

        self.specials = [
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
        if alt_gr_map == None:
            """
            PROBLEM: And a big one. In too many layouts,
            for this module, AltGr doesn't work like it,
            because it has another code. So, the only
            solution that I found, is to create a mapping.
            But it depends on the layout. This one would 
            work for me, but no for other.
            """
            self.alt_gr_map = {
                '!': '|',
                '"': '@',
                '#': '·',
                '$': '~',
                '%': '½',
                '&': '¬',
                '/': '{',
                '(': '[',
                ')': ']',
                '=': '}',
                "'": '\\',
                '?': '¸',
                '~': '`',
                '}': '¨',
                '+': '~',
                '{': '^',
                'q': '@',
                '-': '^',
                '.': '·',
                '<': '|'
            }
        
        self.block_key = "ctrl+/esc"
        self.on_press_f = None
        self.on_release_f = None
        self.last_modifiers = []
        self.alt_gr_keycode = "<65027>"
    
    def prepare_keys(self, key):
        """
        Formats the string that represents the key.
        """

        if key in self.specials:
            key = '/' + key.__str__().split('.')[-1]
            # Escapes the special chars
        else:
            key = key.__str__()

            """
            Declared behaviour: Keyboard layout sublevels will
            be ignored. Always that alt_gr is in modifiers, the
            respective special character is use. If shift or other
            modifier is pressed, it will be ignored.
            """

            if "alt_gr" in self.last_modifiers:
                if key in self.alt_gr_map.keys():
                    key = self.alt_gr_map[key]

            for modifier in self.last_modifiers:
                if modifier == 'alt_gr': continue
                key = modifier.__str__() + '+' + key
                
        print(self.last_modifiers)

        return key

    def on_press(self, key):
        """
        Function called by the listener to prepare
        the key to be passed to the function given
        as argument.

        Also, this includes the blocking cancel
        key combination listening.
        """

        if key in self.modifiers:
            key = key.__str__().split('.')[-1]
            # Expressed by default like Key.modifier

            if key not in self.last_modifiers:
                self.last_modifiers.append(key)
        elif key.__str__() == self.alt_gr_keycode:
            self.last_modifiers.append("alt_gr")
        else:
            key = self.prepare_keys(key)

            if self.block and key == self.block_key:
                return False

    def on_release(self, key):
        """
        Function called by the listener to prepare
        the key to be passed to the function given
        as argument.
        """

        if key in self.modifiers:
            key = key.__str__().split('.')[-1]

            if key in self.last_modifiers:
                self.last_modifiers.remove(key)
        elif key.__str__() == self.alt_gr_keycode:
            self.last_modifiers.remove("alt_gr")
        else:
            key = self.prepare_keys(key)

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
                on_press=self.on_press,
                on_release=self.on_release
            ) as listener:
                listener.join()
        else:
            listener = keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release
            )
            listener.start()

def main():
    keyboard_controller = KeyboardControl()

    keyboard_controller.start_listening(blocking=True)

main()
