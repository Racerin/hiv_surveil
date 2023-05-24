import os
from dataclasses import dataclass, Field, fields
import json

import pynput
from pynput.keyboard import Key

import config


# KEYBOARD CONTROLLER STUFF
@dataclass
class KeyListenerCommand:
    """ A command obj containing function to call based on key press. """
    name : str
    on_press_vs_on_release : bool
    key_combinations : tuple['pynput.keyboard.KeyCode']
    callback_func : None = lambda: None

    def __call__(self):
        """ Call the callback function """
        self.callback_func()

    def __le__(self, other):
        """ 
        Do check to see if KeyListenerCommand (KLC) contains key presses commands
        that are in another.
        TODO: 
            Checks for function keys (exclude KLC with only function key codes;)
            When doing check, take into account key sequence. ex. W+A+S+D vs A+S+D+W
        """
        if isinstance(other, KeyListenerCommand):
            # Ensure KLC's have some command length
            if len(other.key_combinations) < 0:
                ValueError("Other KLC '{}' needs some keys to press".format(other))
            else:
                # Check for keys
                other_keys = set(other.key_combinations)
                return all(self_key in other_keys for self_key in self.key_combinations)
        else:
            super().__le__(other)

    def __str__(self):
        return "KL Command: name='{}', Keys:{}".\
            format(self.name, self.key_combinations)

    @classmethod
    def _klc_from_dict(cls, dict1:dict):
        """ 
        Return KeyListenerCommand (KLC) object from dict. 
        """
        klc_fields = fields(cls)
        holder = dict()
        for fld in klc_fields:
            try:
                val = dict1.get(fld)
                holder.update({fld:val})
            except KeyError:
                pass
        klc = KeyListenerCommand(**holder)
        return klc

    @classmethod
    def from_json(cls, json_text:str)->list['KeyListenerCommand']:
        """ 
        Create KeyListenerCommand's (KLC) from json text.
        """
        assert isinstance(json_text, str), "text needs to be a str. {}".format(type(json_text))
        klc_obj_objs = json.loads(json_text)
        # Manage outputs
        if isinstance(klc_obj_objs, dict):
            ans = [cls._klc_from_dict(klc_obj_objs)]
        elif isinstance(klc_obj_objs, list):
            for ele in klc_obj_objs:
                cls._klc_from_dict(ele)
        else:
            raise TypeError("Deserializing the json text did not return the correct file.")
        return ans


class MyKeyboardListener(pynput.keyboard.Listener):
    """ 
    A Keyboard Listener with additional methods and properties. 
    It is also a singleton.
    """
    __kl_listener = None

    keyboard_keys_holddown = set()

    keylistener_commands = list()

    @classmethod
    def get_keyboard_listener(cls)->'MyKeyboardListener':
        """ Return MyKeyboardListener instance else return None """
        return cls.__kl_listener if isinstance(cls.__kl_listener,MyKeyboardListener) else None

    @classmethod
    def exists(cls)->bool:
        """ Returns a boolean stating whether a listener exists and is running. """
        if cls.__kl_listener:
            if cls.__kl_listener.running:
                return True
        return False

    @classmethod
    def stop(cls, verbose=1):
        """ Stops the Keyboard listener """
        if isinstance(cls.__kl_listener, MyKeyboardListener):
            if verbose:
                print("Stopped MyKeyboardListener")
            cls.stop()

    @classmethod
    def __check_command_registered_already(cls, kl_command:KeyListenerCommand)->bool:
        """ Check to see if a key listener command (KLC)
         exists already by name and by key combinations in a list of commands """
        # Check to see if any KLC names are the same
        command_name_exists = any((kl_command.name==kl_cmd.name for kl_cmd in cls.keylistener_commands))
        # Check to see if any KLC combo presses are being used already
        key_combination_exists = False
        key_combination_exists = any(kl_command<=kl_cmd for kl_cmd in cls.keylistener_commands)
        return (command_name_exists or key_combination_exists)

    @classmethod
    def register_command(cls, kl_cmd:KeyListenerCommand)->None:
        """ 
        Add a command to keyboard listener to look-out for. 
        Add any other command filters.
        """
        if not isinstance(kl_cmd, KeyListenerCommand):
            raise TypeError("This is not a KeyListenerCommand.{}".format(kl_cmd))
        elif cls.__check_command_registered_already(kl_cmd):
            raise ValueError("KeyListenerCommand already exists.")
        else:
            cls.keylistener_commands.append(kl_cmd)

    @classmethod
    def unregister_command(cls, key:str, quiet=False)->KeyListenerCommand:
        """ 
        Remove a KeyboardListenerCommand 
        """
        if isinstance(key, str):
            for kl_cmd in cls.keylistener_commands:
                if kl_cmd.name == key:
                    return cls.keylistener_commands.pop()
            else:
                if not quiet:
                    raise ValueError("Key '{}' doesn't exists.".format(key))
        else:
            TypeError("'{}' is not a str.".format(key))

    @classmethod
    def list_commands(cls)->str:
        """ Return a list of commands registered in a nice format. """
        each = list()
        for cmd in cls.keylistener_commands:
            each.append(str(cmd))
        text = "\n".join(each)
        return text


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
    
    @classmethod
    def compare_new_key_to_klcommands(cls, new_key, filters:dict=dict())->None:
        """ 
        Essentially, use new_key and keys already pressed to determine which command to call.
        filters : If filters is populated, does a check to filter kl_cmd whose attribute/key matches the value/value
        """
        kl_cmds_post_filter = list()
        if isinstance(filters, dict):
            bigger_temp_set = set(MyKeyboardListener.keylistener_commands())
            for k,v in filters.items():
                for kl_cmd in MyKeyboardListener.keylistener_commands:
                    temp_set = set()
                    try:
                        val = getattr(kl_cmd, k)
                        if val == v:
                            temp_set.add(kl_cmd)
                    except AttributeError:
                        pass
                bigger_temp_set.intersection(temp_set)
            kl_cmds_post_filter = list(bigger_temp_set)
        else:
            kl_cmds_post_filter = MyKeyboardListener.keylistener_commands
        # TODO: Separate this function?
        if len(kl_cmds_post_filter):
            for kl_cmd in kl_cmds_post_filter:
                # Check the active/new_key, see if it is in a command 
                if new_key in kl_cmd.key_combinations:
                    # and if it is, check the other buttons if they are pressed already 
                    if all((key in MyKeyboardListener.keyboard_keys_holddown for key in kl_cmd.key_combinations)):
                        # and if they are, call the command
                        kl_cmd.callback_func()
                        return None

                    

    def on_press_keyboard_callback(self, key, verbose=0):
        """ Callback for 'start_keyboard_listener' function """
        # TODO: Connect callback to keylistener commands
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
        # TODO: Connect callback to keylistener commands
        # Logging. TODO: Switch to logger in cli
        if verbose > 0:
            print('{0} released'.format(
                key))
        if key == pynput.keyboard.Key.esc:
            # Stop listener
            self.stop()
            return False
        
        # TODO: To rename the following method
        # Call callback_function
        MyKeyboardListener.compare_new_key_to_klcommands(key, filters=dict(on_press_vs_on_release=True,))

        # Finally, Remove the character from the set
        if key not in self.keyboard_keys_holddown:
            # Once a new button is pressed, do the check
            self.keyboard_keys_holddown.add(key)
            print(self.keyboard_keys_holddown, " Keys held down.")
            # Call the key callback function now. 
            self.call_func_mapped_to_key()
        if key in self.keyboard_keys_holddown:
            self.keyboard_keys_holddown.remove(key)

    def __init__(self, on_press=on_press_keyboard_callback, on_release=on_release_keyboard_callback):
        """ NB. Singleton """
        if isinstance(self.__kl_listener, MyKeyboardListener):
            raise AttributeError("Cannot have multiple instances of a singleton.")
        else:
            # New singleton
            MyKeyboardListener.__kl_listener = self
            #  Deploy listener
            # super(MyKeyboardListener, self).__init__(
            super().__init__(
                on_press=on_press,
                on_release=on_release
                )


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
    try:
        text = read_text_file(type_template_path)
        keyboard_typer.type(text)
    except FileNotFoundError as e:
        raise FileNotFoundError("This file '{}' cannot be found".format(type_template_path)) from e


# Default KeyboardListener Commands
fx1 = lambda:print("Hello World")
MyKeyboardListener.register_command(
    KeyListenerCommand(
        name="hello_world", 
        on_press_vs_on_release=False,
        callback_func=fx1,
        key_combinations=(Key.f7,),
        )
    )
fx2 = lambda:print("We made it.")
MyKeyboardListener.register_command(
    KeyListenerCommand(
        name="made_it", 
        on_press_vs_on_release=False,
        callback_func=fx2,
        key_combinations=(Key.f8,),
        )
    )
MyKeyboardListener.register_command(
    KeyListenerCommand(
        name="type_out_template", 
        on_press_vs_on_release=True,
        callback_func=type_type_template_file, 
        key_combinations=(Key.f9,),
        )
    )

# TODO: Convert to KeyListenerCommand
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
    print("+++++++++", dir(keyboard_listener))
    keyboard_listener.start()

def end_keyboard_listener()->None:
    """ Stop the keyboard listener. """
    MyKeyboardListener.stop()