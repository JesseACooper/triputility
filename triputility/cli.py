import click
import os
import sys

# from triputility.config import Config
from triputility.commands.map import maptrip

@click.group(help="Query various details about trips")
@click.pass_context
def cli(ctx):
    aws_key = os.environ.get('AWS_ACCESS_KEY_ID')
    if aws_key == None:
        click.echo("Aborting: AWS credentials not set - did you run aws-login?")
        sys.exit()

    # config = Config(os.path.join(os.path.expanduser("~"), ".triputility-cli.ini"))
    # config = Config("config.ini")


cli.add_command(maptrip)