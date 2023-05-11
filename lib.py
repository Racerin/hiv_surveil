import os

import pynput
from pynput.keyboard import Key

import config


def type_header(sep="\t"):
    """ When called, types automatically the header information according to config.py """
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

# KEYBOARD CONTROLLER STUFF
keyboard_typer = pynput.keyboard.Controller()
keyboard_listener = None
keyboard_keys_pressed = set()

keyboard_callback_functions = {
    # (Key.shift, pynput.keyboard.KeyCode(char='l'), ): lambda: print("We made it."),
    (pynput.keyboard.KeyCode(char='j'), ): lambda: print("A 'j' was pressed."),
    # (pynput.keyboard.KeyCode(char='~'), ): lambda: print("I pressed it."),
    # (Key.shift, Key.ctrl_l, pynput.keyboard.KeyCode(char='~'), ): type_type_template_file,
    (Key.f9, ): type_type_template_file,
}

def call_func_mapped_to_key()->None:
    """ 
    Call a function according to the keys pressed / held down in 'keyboard_keys_pressed'.
    Comparison map is 'keyboard_callback_functions'
    """
    callback_func = lambda: None
    global keyboard_keys_pressed
    # TODO: The following code structure needs to be unittest to confirm proper behavior of keys selected to function
    for key_tup in keyboard_callback_functions.keys():
        if all(k in key_tup for k in keyboard_keys_pressed):
        # if all(k in keyboard_keys_pressed for k in key_tup):
            callback_func = keyboard_callback_functions[key_tup]
            break
    # Now, call the function
    callback_func()
    return

def on_press_keyboard_callback(key, verbose=0):
    """ Callback for 'start_keyboard_listener' function """
    global keyboard_keys_pressed
    # Logging
    if verbose > 0:
        try:
            print('alphanumeric key {0} pressed'.format(
                key.char))
        except AttributeError:
            print('special key {0} pressed'.format(
                key))

def on_release_keyboard_callback(key, verbose=0):
    """ Callback for 'start_keyboard_listener' function """
    # Logging
    if verbose > 0:
        print('{0} released'.format(
            key))
    if key == pynput.keyboard.Key.esc:
        # Stop listener
        return False
    # Finally, Remove the character from the set
    global keyboard_keys_pressed
    if key not in keyboard_keys_pressed:
        # Once a new button is pressed, do the check
        keyboard_keys_pressed.add(key)
        print(keyboard_keys_pressed, " Keys held down.")
        # Call the key callback function now. 
        call_func_mapped_to_key()
    if key in keyboard_keys_pressed:
        keyboard_keys_pressed.remove(key)


def start_keyboard_listener():
    """ Listen to keyboard inputs and execute appropriate commands. """
    keyboard_listener = pynput.keyboard.Listener(
        on_press=on_press_keyboard_callback,
        on_release=on_release_keyboard_callback)
    keyboard_listener.start()

def end_keyboard_listener():
    """ Stop the keyboard listener. """
    # pynput.keyboard.Listener.stop
    if keyboard_listener is not None:
        keyboard_listener.stop()