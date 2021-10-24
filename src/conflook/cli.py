"""
Entry point to command line interface.
"""

import os
import sys
from collections.abc import Mapping

import click

from .filetypes import JSONDoc, TOMLDoc


@click.command(help="Show summarised structure or value at keypath.")
@click.version_option(package_name="conflook")
@click.option("--raw", "is_raw", is_flag=True, help="Show full value.")
@click.argument("file", type=click.File("rb"))
@click.argument("keypath", default="", required=False)
# pylint: disable=unused-argument
def cli(file, keypath, is_raw):
    """
    1. Check for valid config file.
    2. Process it into dictonary.
    3. Find value at keypath.
    4. Echo summarised representation of value to terminal.
    """

    if TOMLDoc.has_compatible_suffix(file.name):
        doc = TOMLDoc(file)
    elif JSONDoc.has_compatible_suffix(file.name):
        doc = JSONDoc(file)
    else:
        print(f"Cannot read '{file.name}'.", file=sys.stderr)
        return

    value, actual_path = doc.follow_keypath(keypath, approx=True)

    if value is None:
        print(actual_path, file=sys.stderr)
        return

    if actual_path:
        print(actual_path + ", ", end="")

    print(doc.get_type_description(value))

    if isinstance(value, Mapping):
        table = []
        for key, val in value.items():
            table.append((key, doc.get_type_description(val), str(val)))
        ncol1, ncol2, _ = (max(map(len, r)) + 1 for r in zip(*table))
        termwidth, _ = os.get_terminal_size(0)
        for acol, bcol, ccol in table:
            print(acol + " " * (ncol1 - len(acol)), end="")
            print(bcol + " " * (ncol2 - len(bcol)), end="")
            print(ccol[: termwidth - ncol1 - ncol2])
    else:
        print(value)


if __name__ == "__main__":
    # params filled in by click
    # pylint: disable=no-value-for-parameter
    cli()
