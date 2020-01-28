import click
import adm

@click.group()
def device():
    """Manage the Device"""
    pass

@device.command()
@click.option('--fleet-url',  default='http://api.zerinth.com/v1', help='URL of the Fleet Service')
@click.option('--fleet-id', default='null', help='Fleet ID where the device is assigned')
@click.argument('name')
def create(fleet_url, fleet_id, name):
    """Create a device"""
    client = adm.ADMClient(fleetdev_url=fleet_url)
    client.create_device(name, fleet_id)


@device.command()
@click.option('--fleet-url',  default='http://api.zerinth.com/v1', help='Fleet endpoint')
@click.argument('id')
def get(fleet_url, id):
    """Get a single device"""
    client = adm.ADMClient(fleetdev_url=fleet_url)
    client.get_device(id)
    
@device.command()
@click.option('--fleet-url', default='http://api.zerinth.com/v1', help='Fleet endpoint')
def all(fleet_url):
    """Get all the devices"""
    client = adm.ADMClient(fleetdev_url=fleet_url)
    client.get_devices()

@device.command()
@click.option('--fleet-url', default='http://api.zerinth.com/v1', help='Fleet endpoint')
@click.option('--fleet-id', default=None, help='Id of the  new fleet')
@click.option('--name', default=None, help='Name of the device')
@click.argument('id')
def update(fleet_url, id, fleet_id, name):
    """Update a devie"""
    client = adm.ADMClient(fleetdev_url=fleet_url)
    client.update_device_fleet(id, name, fleet_id)