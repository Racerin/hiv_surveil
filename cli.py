import time

import click

import lib

@click.group()
# Add verbose
def cli():
    pass

@cli.command()
def hello_world():
    """ This script prints a basic 'Hello World' text. """
    click.echo("Hello World.")

@cli.command()
def type_header_on_screen():
    lib.type_header()

@cli.command()
def start_keyboard_listener():
    """
     Starts the Keyboard Listener. 
    Execute commands based on button pressed.
    execute 'list-commands' to see the possible commands (TO BE DONE)
    """
    click.echo("Keyboard listener initiated.")
    lib.start_keyboard_listener()
    while lib.MyKeyboardListener.exists():
        time.sleep(1)
    click.echo("Broke-out the loop.")
    # time.sleep(1e4)
    click.echo("Keyboard listener terminated.")

@cli.command()
def list_commands():
    """ List of all commands to be executed with Keyboard Listener. """
    

cli.add_command(type_header_on_screen)
cli.add_command(start_keyboard_listener)
cli.add_command(hello_world)

if __name__ == '__main__':
    cli()