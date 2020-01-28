import click
import adm

@click.group()
def fleet():
    """Manage the Fleet"""
    pass

@fleet.command()
@click.option('--fleet-url', default='http://api.zerinth.com/v1', help='URL of the Fleet Service')
@click.argument('name')
def create(fleet_url, name):
    """Create a fleet"""
    client = adm.ADMClient(fleetdev_url=fleet_url)
    client.create_fleet(name)
    
@fleet.command()
@click.option('--fleet-url',default='http://api.zerinth.com/v1', help='Fleet endpoint')
def all(fleet_url):
    """Get all the fleets"""
    client = adm.ADMClient(fleetdev_url=fleet_url)
    client.get_fleets()

@fleet.command()
@click.option('--fleet-url', default='http://api.zerinth.com/v1', help='Fleet endpoint')
@click.argument('id')
def get(fleet_url, id):
    """Get a single fleet"""
    client = adm.ADMClient(fleetdev_url=fleet_url)
    client.get_fleet(id)
       