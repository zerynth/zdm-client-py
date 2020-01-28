import click
import adm

@click.group()
def workspace():
    """Manage the Workspaces"""
    pass

@workspace.command()
@click.option('--workspace-url', default='http://api.zerinth.com/v1', help='URL of the Fleet Service')
@click.argument('name')
def create(workspace_url, name):
    """Create a workspace"""
    client = adm.ADMClient(workspace_url=workspace_url)
    client.create_workspace(name)
    
@workspace.command()
@click.option('--workspace-url', default='http://api.zerinth.com/v1', help='URL of the Fleet Service')
@click.argument('id')
def get(workspace_url, id):
    """Get a workspace"""
    client = adm.ADMClient(workspace_url=workspace_url)
    client.get_workspace(id)

@workspace.command()
@click.option('--workspace-url',default='http://api.zerinth.com/v1', help='Fleet endpoint')
def all(workspace_url):
    """Get all the workspaces"""
    client = adm.ADMClient(workspace_url=workspace_url)
    client.workspace_all()

       