"""
Entry point to command line interface.
"""

import os
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Sequence

import click

from .filetypes import JSONDoc, TOMLDoc, YAMLDoc
from .utils import make_printable

FILETYPES = [TOMLDoc, JSONDoc, YAMLDoc]


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

    for cls in FILETYPES:
        if cls.has_compatible_suffix(file.name):
            doc = cls(file)
            break
    else:
        print(f"Unsupported file format '{Path(file.name).suffix}'.", file=sys.stderr)
        supported = []
        for cls in FILETYPES:
            supported.extend(cls.compatible_suffixes())
        print(f"Supported formats: {' '.join(supported)}")
        return

    value, actual_path = doc.follow_keypath(keypath, approx=True)

    if value is None:
        print(actual_path, file=sys.stderr)
        return

    if actual_path:
        print(actual_path + ", ", end="")

    print(doc.get_type_description(value))

    if isinstance(value, Mapping) and not isinstance(value, Sequence):
        table = []
        for key, val in value.items():
            str_val = ""
            if hasattr(val, "__str__"):
                # so that str_val is printed on a single line with \n for newlines etc,
                # escape control characters \t \r \n etc and replace unprintible unicode
                # characters with '?'
                str_val = make_printable(doc.str_of(val))

            table.append((key, doc.get_type_description(val), str_val))

        if len(table) > 0:
            ncol1, ncol2, _ = (max(map(len, r)) + 1 for r in zip(*table))
            termwidth, _ = os.get_terminal_size(0)

            for acol, bcol, ccol in table:
                print(acol + " " * (ncol1 - len(acol)), end="")
                print(bcol + " " * (ncol2 - len(bcol)), end="")
                print(ccol[: termwidth - ncol1 - ncol2])
    elif isinstance(value, Sequence) and not isinstance(value, str):
        for val in value:
            print(doc.str_of(val))
    else:
        print(doc.str_of(value))


if __name__ == "__main__":
    # params filled in by click
    # pylint: disable=no-value-for-parameter
    cli()
