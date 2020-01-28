import click
import adm

@click.group()
def tsmanager():
    """Manage the timescale db and workspaces tables"""
    pass

@tsmanager.command()
@click.option('--tsmanager-url', default='http://api.localhost/v1/tsmanager', help='URL of the TSManager service')
@click.argument('workspace_id')
def create_workspace_table(tsmanager_url, workspace_id):
    """Create a workspace table"""
    client = adm.ADMClient(tsmanager_url=tsmanager_url)
    client.create_workspace_table(workspace_id)

@tsmanager.command()
@click.option('--tsmanager-url', default='http://api.zerinth.com/v1/tsmanager', help='URL of the TSManager service')
@click.argument('timestamp_device')
@click.argument('tag')
@click.argument('device_id')
@click.argument('payload')
@click.argument('workspace_id')
def insert_row(tsmanager_url, timestamp_device, tag, device_id, payload, workspace_id):
    """Insert row in a workspace table"""
    client = adm.ADMClient(tsmanager_url=tsmanager_url)
    client.insert_row(timestamp_device, tag, device_id, payload, workspace_id)

@tsmanager.command()
@click.option('--tsmanager-url', default='http://api.zerinth.com/v1/tsmanager', help='URL of the TSManager service')
@click.argument('workspace_id')
def list_workspace_tags(tsmanager_url, workspace_id):
    """List workspace tags"""
    client = adm.ADMClient(tsmanager_url=tsmanager_url)
    client.list_workspace_tags(workspace_id)

@tsmanager.command()
@click.option('--tsmanager-url', default='http://api.zerinth.com/v1/tsmanager', help='URL of the TSManager service')
@click.argument('workspace_id')
@click.argument('tag')
@click.option('--start', default=None, help='starting time')
@click.option('--end', default=None, help='end time')
@click.option('--device_id', default=None, help='device id')
@click.option('--custom', default=None, help='custom query fields')
def get_tag(tsmanager_url, workspace_id, tag, start, end, device_id, custom):
    """Get workspace tags with a custom query """
    client = adm.ADMClient(tsmanager_url=tsmanager_url)
    client.get_tag(workspace_id, tag, start, end, device_id, custom)