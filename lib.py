import os
import logging
import time
from collections.abc import Callable

import pynput
from pynput.keyboard import Key

import config
from PARAMS import *

# KEYBOARD CONTROLLER STUFF
keyboard_typer = pynput.keyboard.Controller()
keyboard_listener = None
keyboard_keys_pressed = set()

def verbose_set_logging_level(verbose:int)->None:
    """ Using the count of verbose, set the logging level. """
    logging_level = MAP_VERBOSE_LOGGING_LEVEL.get(verbose, logging.getLogger().level)
    logging.getLogger().setLevel(logging_level)
    print("The current logging level. {0}".format(logging.getLogger().level))

def read_text_file(file_path:str)->str:
    """ Read file and return text. """
    text = ""
    logging.debug("Opening file '{0}'.".format(file_path))
    with open(file_path, mode="r") as file:
        text = "".join(file.readlines())
    logging.debug("Successfully read file '{0}'.".format(file_path))
    return text

def type_type_template_file(type_template_path:str=config.TYPE_TEMPLATE_PATH)->None:
    """ Read type_template.txt file and type-out each character in the file. """
    text = read_text_file(type_template_path)
    keyboard_typer.type(text)

mapped_keys_to_callback_functions = {
    # (Key.ctrl_l, Key.f9,): type_type_template_file,
    (Key.f9,): type_type_template_file,
}

def get_func_mapped_to_key()->Callable:
    """ 
    Call a function according to the keys pressed / held down in 'keyboard_keys_pressed'.
    Comparison map is 'keyboard_callback_functions'
    """
    global keyboard_keys_pressed
    # TODO: The following code structure needs to be unittest to confirm proper behavior of keys selected to function
    for t_keys, callback_func in mapped_keys_to_callback_functions.items():
        if all(t_key in keyboard_keys_pressed for t_key in t_keys):
            return callback_func

def on_press_keyboard_callback(key)-> None:
    """ Callback for 'start_keyboard_listener' function """
    global keyboard_keys_pressed
    logging.debug('special key {0} pressed'.format(key))
    global keyboard_keys_pressed
    keyboard_keys_pressed.add(key)
    # logging.debug("These are the keys pressed. {0}".format(keyboard_keys_pressed))

def on_release_keyboard_callback(key):
    """ Callback for 'start_keyboard_listener' function """
    logging.debug('special key {0} released'.format(key))
    # Escape Keyboard Listener function
    if key == pynput.keyboard.Key.esc:
        # Stop listener
        logging.info("Keyboard listener stopped.")
        return False
    # ONLY action the callback function when the key is released
    global keyboard_keys_pressed
    callback_func = get_func_mapped_to_key()
    keyboard_keys_pressed.discard(key)  # remove key if it is there or not
    if callback_func is not None:
        callback_func()


def start_keyboard_listener():
    """ Listen to keyboard inputs and execute appropriate commands. """
    logging.info("Start keyboard listener.")
    keyboard_listener = pynput.keyboard.Listener(
        on_press=on_press_keyboard_callback,
        on_release=on_release_keyboard_callback)
    keyboard_listener.start()
    time.sleep(LIMIT_SLEEP_TIME)
    
    # The following freezes the command line
    """ with pynput.keyboard.Listener(
        on_press=on_press_keyboard_callback,
        on_release=on_release_keyboard_callback) as kayboard_listener:
        kayboard_listener.join() """

def end_keyboard_listener():
    """ Stop the keyboard listener. """
    logging.info("End keyboard listener.")
    if keyboard_listener is not None:
        keyboard_listener.stop()