import click


@click.group()
@click.version_option(package_name="conflook")
def cli():
    pass


@cli.command(help="Show summarised structure or value at keypath.")
@click.option("--raw", "is_raw", is_flag=True, help="Show full value.")
@click.argument("file", type=click.File("rb"))
@click.argument("keypath")
def get(file, keypath, is_raw):
    click.echo("get")


@cli.command(help="Set the value at keypath.")
@click.option("--use-editor", is_flag=True)
@click.argument("file", type=click.File("rb+"))
@click.argument("keypath")
@click.argument("value", nargs=-1)
def set(file, keypath, value, is_raw, use_editor):
    click.echo("set")


if __name__ == "__main__":
    cli()