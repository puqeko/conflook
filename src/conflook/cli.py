"""
Entry point to command line interface.
"""

import sys

import click

from .filetypes.toml import TOMLDoc


@click.command(help="Show summarised structure or value at keypath.")
@click.version_option(package_name="conflook")
@click.option("--raw", "is_raw", is_flag=True, help="Show full value.")
@click.argument("file", type=click.File("rb"))
@click.argument("keypath", nargs=-1, required=False)
# pylint: disable=unused-argument
def cli(file, keypath, is_raw):
    """
    1. Check for valid config file.
    2. Process it into dictonary.
    3. Find value at keypath.
    4. Echo summarised representation of value to terminal.
    """

    doc = TOMLDoc(file)
    value, actual_path = doc.try_follow_keypath(keypath, approx=True)

    if value is None:
        print(actual_path, file=sys.stderr)
        return

    print(value)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()
