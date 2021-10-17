"""
.
"""


import click


@click.group()
@click.version_option(package_name="conflook")
def cli():
    """
    .
    """


@cli.command(help="Show summarised structure or value at keypath.")
@click.option("--raw", "is_raw", is_flag=True, help="Show full value.")
@click.argument("file", type=click.File("rb"))
@click.argument("keypath")
# pylint: disable=unused-argument
def get(file, keypath, is_raw):
    """
    .
    """


@cli.command(name="set", help="Set the value at keypath.")
@click.option("--use-editor", is_flag=True)
@click.argument("file", type=click.File("rb+"))
@click.argument("keypath")
@click.argument("value", nargs=-1)
# pylint: disable=unused-argument
def set_(file, keypath, value, is_raw, use_editor):
    """
    .
    """


if __name__ == "__main__":
    cli()
