import click

import lib

@click.group()
def cli():
    pass

def type_header_on_screen():
    lib.type_header()

def start_keyboard_listener():
    lib.start_keyboard_listener()

cli.add_command(type_header_on_screen)


if __name__ == '__main__':
    cli()