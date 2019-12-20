import click
import adm

@click.group()
def workspace():
    """Manage the Workspaces"""
    pass

@workspace.command()
@click.option('--workspace-url', default='http://127.0.0.1:8000', help='URL of the Fleet Service')
@click.argument('name')
def create(workspace_url, name):
    """Create a workspace"""
    client = adm.ADMClient(workspace_url=workspace_url)
    client.workspace_create(name)
    
# @workspace.command()
# @click.option('--workspace-url', default='http://127.0.0.1:8000', help='Fleet endpoint')
# def all(workspace_url):
#     """Get all the workspaces"""
#     client = adm.ADMClient(workspacedev_url=workspace_url)
#     client.get_workspaces()

# @workspace.command()
# @click.option('--workspace-url', default='http://127.0.0.1:8000', help='Fleet endpoint')
# @click.argument('id')
# def get(workspace_url, id):
#     """Get a single workspace"""
#     client = adm.ADMClient(workspacedev_url=workspace_url)
#     client.get_workspace(id)
       