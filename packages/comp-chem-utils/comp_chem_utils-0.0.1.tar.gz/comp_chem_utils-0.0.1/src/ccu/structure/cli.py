"""This module contains the ccu.structure package CLI logic."""


import pathlib

import click

from ccu.structure import resizecell


@click.group()
def main():
    """Structure manipulation tools."""


@main.command()
@click.argument(
    'structure',
    required=True,
    type=click.Path(exists=True, path_type=pathlib.Path),
)
@click.argument('c-vector', default=10, type=click.FLOAT)
def resize_and_centre(structure, c_vector):
    """Resizes c-vector of given structure and centres the atoms within the
    cell.

    Args:
        STRUCTURE is the structure to be resized and centred.
        C_VECTOR is the new magnitude of the c-vector.
    """
    resizecell.run(structure, c_vector)
