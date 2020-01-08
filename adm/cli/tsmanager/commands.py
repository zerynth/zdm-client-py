import click
import adm

@click.group()
def tsmanager():
    """Manage the timescale db and workspaces tables"""
    pass

@tsmanager.command()
@click.option('--tsmanager-url', default='http://127.0.0.1:8006', help='URL of the Status service')
@click.argument('workspace_id')
def list_workspace_tags(tsmanager_url, workspace_id):
    """List workspace tags"""
    client = adm.ADMClient(tsmanager_url=tsmanager_url)
    client.create_changeset(workspace_id)

@tsmanager.command()
@click.argument('workspace_id')
@click.argument('tag')
@click.option('--start', default='null', help='starting time')
@click.option('--end', default='null', help='end time')
@click.option('--device_id', default='null', help='device id')
@click.option('--custom', default='null', help='custom query fields')
def get_tag(tsmanager_url, workspace_id, tag, start, end, device_id, custom):
    """Get workspace tags with a custom query """
    client = adm.ADMClient(tsmanager_url=tsmanager_url)
    client.get_tag(workspace_id,tag, start, end, device_id, custom)