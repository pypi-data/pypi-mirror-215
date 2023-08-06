import click
from finditcli.finder import finder
from finditcli.exceptions import FileFinderError


def cli():
    try:
        finder()
    except FileFinderError as err:
        click.echo(click.style(f"❌ {err}", bg="black", fg="red", italic=True))
