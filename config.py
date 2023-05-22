import os
import sys

KL_COMMAND_LIST = []

# Default environmental variables
TYPE_TEMPLATE_PATH = r"C:\Users\dabaird\Desktop\HIV_Surveillance\type_template.txt"

# ANY NEW CONFIG VARIABLE SHOULD BE ADDED HERE FOR ENVIRONMENTAL VARIABLE IMPORTING
env_variable_fields = [
    'TYPE_TEMPLATE_PATH',
]

def load_env():
    """ Load '.env' variables into config file.  """
    this_module = sys.modules[__name__] # https://stackoverflow.com/a/35904211
    dict_env_variables = os.environ
    for k,v in os.environ.items():
        # Assign each environmental variable to config file module if on the list.
        if k in env_variable_fields:
            setattr(this_module, k, v)
load_env()