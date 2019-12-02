import click

from .rpc import commands as rpc
from .device import commands as device

@click.group()
def main():
    """CLI of the ADM SDK."""
    click.echo('Hello from ADM dev!')

main.add_command(rpc.rpc)
main.add_command(device.device)