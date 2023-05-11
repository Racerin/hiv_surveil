import time

import click

import lib

@click.group()
# Add verbose
def cli():
    pass

@cli.command()
def hello_world():
    click.echo("It works.")

@cli.command()
def type_header_on_screen():
    lib.type_header()

@cli.command()
def start_keyboard_listener():
    click.echo("Keyboard listener initiated.")
    lib.start_keyboard_listener()
    while lib.keyboard_listener is not None:
        time.sleep(1)
        click.echo("Broke-out the loop.")
    time.sleep(1e4)
    click.echo("Keyboard listener terminated.")

cli.add_command(type_header_on_screen)
cli.add_command(start_keyboard_listener)
cli.add_command(hello_world)

if __name__ == '__main__':
    cli()