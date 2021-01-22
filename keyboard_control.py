# -*- coding: utf-8 -*-

"""

Module created to simplify the use of mouse.

Maybe it could have problems with X display.
"""

from pynput import keyboard 
import re
import subprocess

class KeyboardControl(object):
    """Class that simplify use of keyboard in automation."""

    def __init__(self, alt_gr_map=None):
        super(KeyboardControl, self).__init__()
        self.block = False
        self.modifiers = {
            'alt': keyboard.Key.alt,
            'alt': keyboard.Key.alt_gr,
            'alt': keyboard.Key.alt_l,
            'alt': keyboard.Key.alt_r,
            'cmd': keyboard.Key.cmd,
            'cmd': keyboard.Key.cmd_l,
            'cmd': keyboard.Key.cmd_r,
            'ctrl': keyboard.Key.ctrl,
            'ctrl': keyboard.Key.ctrl_l,
            'ctrl': keyboard.Key.ctrl_r,
            'shift': keyboard.Key.shift,
            'shift': keyboard.Key.shift_l,
            'shift': keyboard.Key.shift_r
        }

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
                '1': '|',
                '2': '@',
                '3': '·',
                '4': '~',
                '5': '½',
                '6': '¬',
                '7': '{',
                '8': '[',
                '9': ']',
                '0': '}',
                '"': '\\',
                '¿': '¸',
                '~': '`',
                '[': '¨',
                '+': '~',
                '{': '^',
                'q': '@',
                '-': '^',
                '<': '|',
                'z': '«',
                'x': '»'
            }
        
        self.block_key = "ctrl+/esc"
        self.on_press_f = None
        self.on_release_f = None
        self.last_modifiers = []
        self.alt_gr_keycode = "<65027>"
        self.on_caps_lock = False
        self.init()

    def init(self):
        """
        Runs some init functions.

         - Inits the keyboard controller.
         - Disables CapsLock.

        """
        self.controller = keyboard.Controller()

        if self.check_lock_keys_state(0):
            self.controller.tap(keyboard.Key.caps_lock)

    def get_key_str(self, key):
        key = key.__str__().split('.')[-1]
        key = re.search(r"[^'.+]+", key).group(0)
    
        return key

    def check_lock_keys_state(self, lock_key):
        """
        Function that checks the state of
        Caps Lock, Scroll Lock, Nums Lock.

        The parameter lock_key works like:

            0: Caps Lock
            1: Nums Lock
            2: Scroll Lock

        IMPORTANT: This will only work in Linux systems.
        """
        output = subprocess.Popen(
                "xset -q | grep Caps",
                shell=True,
                stdout=subprocess.PIPE
        ).stdout.read().decode()

        lock_states = re.findall(r"on|off", output)
        # Returns on or off for each lock in order

        return True if lock_states[lock_key] == 'on' else False

    def prepare_keys(self, key):
        """
        Formats the string that represents the key.
        """

        if key in self.specials:
            key = '/' + self.get_key_str(key)
            # Escapes the special chars

            if key == '/caps_lock':
                self.on_caps_lock = not(self.on_caps_lock)
            # Have a register of the caps lock
        else:
            key = self.get_key_str(key)

            """
            Declared behaviour: Keyboard layout sublevels will
            be ignored. Always that alt_gr is in modifiers, the
            respective special character is use. If shift or other
            modifier is pressed, it will be ignored.
            """

            if "alt_gr" in self.last_modifiers:
                if key in self.alt_gr_map:
                    key = self.alt_gr_map[key]
            elif "shift" in self.last_modifiers:
                if key.isalpha():
                    key == key.upper()
            elif self.on_caps_lock and key.isalpha():
                key = key.upper()

            for modifier in self.last_modifiers:
                if modifier in ['alt_gr', 'shift']: continue
                key = modifier.__str__() + '+' + key
                
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
            key = self.get_key_str(key)
            # Expressed by default like Key.modifier

            if key not in self.last_modifiers:
                self.last_modifiers.append(key)
        elif self.get_key_str(key) == self.alt_gr_keycode:
            self.last_modifiers.append("alt_gr")
        else:
            key = self.prepare_keys(key)

            if self.block and key == self.block_key:
                return False

        if self.on_press_f != None:
            self.on_press_f()

    def on_release(self, key):
        """
        Function called by the listener to prepare
        the key to be passed to the function given
        as argument.
        """

        if key in self.modifiers:
            key = self.get_key_str(key)

            if key in self.last_modifiers:
                self.last_modifiers.remove(key)
        elif self.get_key_str(key) == self.alt_gr_keycode:
            self.last_modifiers.remove("alt_gr")
        else:
            key = self.prepare_keys(key)

        if self.on_release_f != None:
            self.on_release_f()

    def start_listening(
            self,
            on_press=None,
            on_release=None,
            blocking=False
        ):
        """
        Function that configures the listening using
        arguments to set all properties.
        """

        self.on_press_f = on_press
        self.on_release_f = on_release

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

    # --------------------------------------------------
    # ----------------- KEYBOARD CONTROL ---------------
    # --------------------------------------------------

    def get_key_from_str(self, key_str):
        """
        This function return a Key object,
        from keyboard.Key, receiving a string
        that represents it.
        """

        keys = list()

        if type(key_str) == list:
            for key in key_str:
                if key in self.modifiers:
                    keys.append(self.modifiers[key]) 
            return keys
        else:
            return self.modifiers[key_str]

    def send_keys(self, keys_list=None):
        """
        Writes the keys received as text.

         - If receives a letter, writes it.
         - If receives a combination (modifier+key)
           send it all.
         - If receives a text, writes it as text.
        """
        if keys_list:
            for key in keys_list:
                if "+" in key and len(key) > 1:
                    keys = key.split("+")

                    modifiers = self.get_key_from_str(keys[0:-1]) 
                    # Supposing all keys are modifiers except
                    # last one

                    with self.controller.pressed(*modifiers):
                        self.controller.press(keys[-1])

                elif key in self.specials:
                    key_code = keyboard.KeyCode.from_char(key)
                    self.controller.tap(key_code)
                else:
                    self.controller.type(key)

def main():
    keyboard_controller = KeyboardControl()

    keyboard_controller.send_keys(['ctrl+shift+v'])

if __name__ == "__main__":
    main()
