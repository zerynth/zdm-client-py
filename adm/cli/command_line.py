import click

from .rpc import commands as rpc
# from .device import commands as thing
from .fleet.commands import fleet
from .device.commands import device
from .account.commands import account
from .status.commands import status
from .tsmanager.commands import tsmanager

@click.group()
def main():
    """CLI of the ADM SDK."""
    click.echo('Hello from ADM dev!')

main.add_command(rpc.rpc)
main.add_command(fleet)
main.add_command(device)
main.add_command(account)
main.add_command(status)
main.add_command(tsmanager)
#main.add_command(thing.device)