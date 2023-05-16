import os

import pynput
from pynput.keyboard import Key

import config


# KEYBOARD CONTROLLER STUFF
class KeyListenerCommand:
    """ A command obj containing function to call based on key press. """
    keys_to_press : None

    def __init__(self, key_presses:)

class MyKeyboardListener(pynput.keyboard.Controller):
    """ 
    A Keyboard Listener with additional methods and properties. 
    It is also a singleton.
    """
    __kl_listener = None

    keyboard_keys_holddown = set()

    keyboard_commands = list()

    def __init__(self, *args, **kwargs):
        """ NB. SIngleton """
        if isinstance(self.__kl_listener, MyKeyboardListener):
            raise AttributeError("Cannot have multiple instances of a singleton.")
        else:
            # New singleton
            MyKeyboardListener.__kl_listener = self

    @classmethod
    def get_keyboard_listener(cls)->'MyKeyboardListener':
        """ Return MyKeyboardListener instance else return None """
        return cls.__kl_listener if isinstance(cls.__kl_listener,MyKeyboardListener) else None
    @classmethod
    def stop(cls, verbose=1):
        """ Stops the Keyboard listener """
        if isinstance(cls.__kl_listener, MyKeyboardListener):
            if verbose:
                print("Stopped MyKeyboardListener")
            cls.stop()

    @classmethod
    def add_command(cls, kl_cmd:KeyListenerCommand)->None:
        """ 
        Add a command to keyboard listener to look-out for. 
        TODO: Add any other command filters.
            example: make sure the type input doesn't exist already.
        """
        if isinstance(kl_cmd, KeyListenerCommand):
            cls.keyboard_commands.append(kl_cmd)

    @classmethod
    def remove_command(cls, key:tuple)->None:
        """ 
        Remove a command 
        TODO: Do a check based on key presses?
        """

    def call_func_mapped_to_key(self, def_callback=lambda:None)->None:
        """ 
        Call a function according to the keys pressed / held down in 'keyboard_keys_pressed'.
        Comparison map is 'keyboard_callback_functions'
        """
        callback_func = def_callback
        # TODO: The following code structure needs to be unittest to confirm proper behavior of keys selected to function
        for key_tup in keyboard_callback_functions.keys():
            if all(k in key_tup for k in self.keyboard_keys_holddown):
            # if all(k in keyboard_keys_pressed for k in key_tup):
                callback_func = keyboard_callback_functions[key_tup]
                break
        # Now, call the function
        callback_func()
        return None

    def on_press_keyboard_callback(self, key, verbose=0):
        """ Callback for 'start_keyboard_listener' function """
        # Logging
        if verbose > 0:
            try:
                print('alphanumeric key {0} pressed'.format(
                    key.char))
            except AttributeError:
                print('special key {0} pressed'.format(
                    key))

    def on_release_keyboard_callback(self, key, verbose=0):
        """ Callback for 'start_keyboard_listener' function """
        # Logging
        if verbose > 0:
            print('{0} released'.format(
                key))
        if key == pynput.keyboard.Key.esc:
            # Stop listener
            self.stop()
            return False
        # Finally, Remove the character from the set
        if key not in self.keyboard_keys_holddown:
            # Once a new button is pressed, do the check
            self.keyboard_keys_holddown.add(key)
            print(self.keyboard_keys_holddown, " Keys held down.")
            # Call the key callback function now. 
            self.call_func_mapped_to_key()
        if key in self.keyboard_keys_holddown:
            self.keyboard_keys_holddown.remove(key)


# Computer to Keyboard Typer
keyboard_typer = pynput.keyboard.Controller()


# MAIN LIBRARY FUNCTIONS
def type_header(sep="\t"):
    """ When called, types automatically the header information according to config.py """
    # TODO
    pass

def read_text_file(file_path)->str:
    """ Read file and return text. """
    text = ""
    with open(file_path, mode="r") as file:
        text = "".join(file.readlines())
    return text

def type_type_template_file(type_template_path=config.TYPE_TEMPLATE_PATH)->None:
    """ Read type_template.txt file, type-out each character in the file. """
    text = read_text_file(type_template_path)
    keyboard_typer.type(text)


# Default KeyboardListener Commands
MyKeyboardListener.add_command()
KeyListenerCommand

    keyboard_callback_functions = {
        # (Key.shift, pynput.keyboard.KeyCode(char='l'), ): lambda: print("We made it."),
        (pynput.keyboard.KeyCode(char='j'), ): lambda: print("A 'j' was pressed."),
        # (pynput.keyboard.KeyCode(char='~'), ): lambda: print("I pressed it."),
        # (Key.shift, Key.ctrl_l, pynput.keyboard.KeyCode(char='~'), ): type_type_template_file,
        (Key.f9, ): type_type_template_file,
    }


def start_keyboard_listener()->None:
    """ Listen to keyboard inputs and execute appropriate commands. """
    keyboard_listener = MyKeyboardListener()
    keyboard_listener.start()

def end_keyboard_listener()->None:
    """ Stop the keyboard listener. """
    MyKeyboardListener.stop()