import click
import os
import sys

from triputility.config import Config
from triputility.redash_client import RedashClient
from triputility.commands.map import map_
from triputility.commands.info import info

@click.group(help="Query various details about trips")
@click.pass_context
def cli(ctx):
    config = Config(os.path.join(os.path.expanduser("~"), ".triputility-cli.ini"))

    if not config.redash_api_key or config.redash_api_key == '':
        click.echo("Aborting: No Redash api key set - see README for configuration instructions")
        sys.exit()

    redash_client = RedashClient(config)
    ctx.obj = redash_client

cli.add_command(map_)
cli.add_command(info)