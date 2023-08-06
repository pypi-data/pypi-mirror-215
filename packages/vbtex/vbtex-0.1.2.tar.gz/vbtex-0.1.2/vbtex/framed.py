
import click
import os
import sys
from rich.console import Console




@click.command(
    help="Renders tex expressions into png"
)
@click.option(
    '-i',
    '--inputfile',
    type=click.Path(),
    default="./main.pdf",
    show_default=True,
    help="Input file name"
)
@click.option(
    '-d',
    '--dpi',
    default=320,
    type=click.INT,
    show_default=True,
    help="DPI -> density per inch for png"
)
@click.option(
    '-r',
    '--ratio',
    nargs=2,
    default=([16, 9]),
    type=click.Tuple([int, int]),
    show_default=True,
    help="aspect ratio of the frame"
)
@click.pass_context
def framed(ctx, inputfile, dpi, ratio):
    tex = click.edit()
    click.echo(tex)
    


    


