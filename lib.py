import os

from pynput.keyboard import Key, Controller
from pynput import keyboard

import config

keyboard_typer = Controller()

keyboard_callback_functions = dict(
    (Key.shift, keyboard.KeyCode('l')):lambda: print("We made it."),
)

def keyboard_mapping_to_func(keys:tuple)->None:
    """ 
    Call a function according to the keys pressed / held down.
    Comparison map is 'keyboard_callback_functions'
    """


def type_header(sep="\t"):
    """ When called, types automatically the header information according to config.py """
    pass

def read_text_file(file_path)->str:
    """ Read file and return text. """
    text = ""
    with open(file_path, mode="r") as file:
        text = "".join(file.readlines())
    return text

def type_type_template_file(type_template_path)->None:
    """ Read type_template.txt file, type-out each character in the file. """
    text = read_text_file(type_template_path)
    keyboard_typer.type(text)


def on_press_keyboard_callback(key):
    """ Callback for 'start_keyboard_listener' function """
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release_keyboard_callback(key):
    """ Callback for 'start_keyboard_listener' function """
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False


def start_keyboard_listener():
    """ Listen to keyboard inputs and execute appropriate commands. """
    listener = keyboard.Listener(
        on_press=on_press_keyboard_callback,
        on_release=on_release_keyboard_callback)
    listener.start()

def en