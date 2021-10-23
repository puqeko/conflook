"""
Entry point to command line interface.
"""

import sys
from collections.abc import Mapping

import click

from .filetypes.toml import TOMLDoc


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

    doc = TOMLDoc(file)
    value, actual_path = doc.follow_keypath(keypath, approx=True)

    if value is None:
        print(actual_path, file=sys.stderr)
        return

    if actual_path:
        print(actual_path + ", ", end="")

    print(doc.get_type_description(value))

    if isinstance(value, Mapping):
        row_width = max(map(len, value.keys())) + 1
        for key, val in value.items():
            print(key + " " * (row_width - len(key)), end="")
            print(doc.get_type_description(val), str(val)[:20])
    else:
        print(value)


if __name__ == "__main__":
    # params filled in by click
    # pylint: disable=no-value-for-parameter
    cli()
