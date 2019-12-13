import click
import adm

@click.group()
def device():
    """Manage the Device"""
    pass

@device.command()
@click.option('--fleet-url', default='http://127.0.0.1:8000', help='URL of the Fleet Service')
@click.option('--fleet-id', default='null', help='Fleet ID where the device is assigned')
@click.argument('name')
def create(fleet_url, fleet_id, name):
    """Create a device"""
    client = adm.ADMClient(fleetdev_url=fleet_url)
    client.create_device(name, fleet_id)


@device.command()
@click.option('--fleet-url', default='http://127.0.0.1:8000', help='Fleet endpoint')
@click.argument('id')
def get(fleet_url, id):
    """Get a single device"""
    client = adm.ADMClient(fleetdev_url=fleet_url)
    client.get_device(id)