import click

@click.command()
def cli():
    """Example script."""
    click.secho('Hello World!',fg="blue", bold=True)