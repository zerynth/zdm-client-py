import click
import adm

@click.group()
def rpc():
    """Manage the RPC"""
    pass

@rpc.command()
@click.option('--rpc-url', default='http://127.0.0.1:7777', help='Endpoint of the RPC Service')
@click.argument('method')
@click.argument('params')
@click.argument('device')
def create(rpc_url, method, params, device):
    """Create and send RPC to a device"""
    client = adm.ADMClient(rpc_url=rpc_url)
    rpc = {'method': method, 'parameters': params, "devices":[device]}
    client.send_rpc(payload=rpc)


@rpc.command()
@click.option('--rpc-url', default='http://127.0.0.1:7777', help='Endpoint of the RPC Service')
@click.argument('rpc')
@click.argument('device')
def get(rpc_url, rpc, device):
    """Get the status of and RPC"""
    client = adm.ADMClient(rpc_url=rpc_url)
    client.get_rpc(rpc, device)