import time
import logging

import click

import lib

@click.group()
@click.option('-v', '--verbose', count=True, default=1, help="Set the logging level of program.")
# def cli(verbose=None):
def cli(verbose):
    # Set verbose
    lib.verbose_set_logging_level(verbose)

@cli.command()
def start_keyboard_listener():
    click.echo("Keyboard listener initiated.")
    lib.start_keyboard_listener()

if __name__ == '__main__':
    cli()