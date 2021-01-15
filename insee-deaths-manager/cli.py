import click

from cli_check import cli_check
from cli_manage import cli_manage
from cli_patch import cli_patch


@click.group()
def cli():
    pass


if __name__ == '__main__':
    cli.add_command(cli_check)
    cli.add_command(cli_manage)
    cli.add_command(cli_patch)
    cli()