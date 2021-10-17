"""
Entry point to command line interface. Offers sub-commands get and set.
"""


import click


@click.group()
@click.version_option(package_name="conflook")
def cli():
    """
    Base command. Allways do this.
    """


@cli.command(help="Show summarised structure or value at keypath.")
@click.option("--raw", "is_raw", is_flag=True, help="Show full value.")
@click.argument("file", type=click.File("rb"))
@click.argument("keypath")
# pylint: disable=unused-argument
def get(file, keypath, is_raw):
    """
    1. Check for valid config file.
    2. Process it into dictonary.
    3. Find value at keypath.
    4. Echo summarised representation of value to terminal.
    """


@cli.command(name="set", help="Set the value at keypath.")
@click.option("--use-editor", is_flag=True)
@click.argument("file", type=click.File("rb+"))
@click.argument("keypath")
@click.argument("value", nargs=-1)
# pylint: disable=unused-argument
def set_(file, keypath, value, is_raw, use_editor):
    """
    1. Check for valid config file.
    2. Process it into dictonary.
    3. Find value at keypath.
    4. Process new value.
    5. Prompt if new value is not equal in type to old value.
    6. Replace value and write changes to file.
    """


if __name__ == "__main__":
    cli()
