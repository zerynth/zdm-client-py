import click
import adm

@click.group()
def status():
    """Manage the changesets and device status"""
    pass

@status.command()
@click.option('--status-url', default='http://127.0.0.1:8002', help='URL of the Status service')
@click.argument('key')
@click.argument('value')
@click.argument('targets')
def register(status_url, key, value, targets):
    """Create a ChangeSet"""
    client = adm.ADMClient(status_url=status_url)
    client.create_changeset(key, value, targets)

@status.command()
@click.option('--status-url', default='http://127.0.0.1:8002', help='URL of the Status service')
@click.argument('changeset_id')
def get_changeset(status_url, changeset_id):
    """Get a ChangeSet"""
    client = adm.ADMClient(status_url=status_url)
    client.get_changeset(changeset_id)

@status.command()
@click.option('--status-url', default='http://127.0.0.1:8002', help='URL of the Status service')
@click.argument('device_id')
def get_current_status(status_url, device_id):
    """Get the current status of a device"""
    client = adm.ADMClient(status_url=status_url)
    client.get_current_status(device_id)

@status.command()
@click.option('--status-url', default='http://127.0.0.1:8002', help='URL of the Status service')
@click.argument('device_id')
def get_expected_status(status_url, device_id):
    """Get the expected status of a device"""
    client = adm.ADMClient(status_url=status_url)
    client.get_expected_status(device_id)
