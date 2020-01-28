import click
import adm

@click.group()
def gates():
    """Manage the gates service"""
    pass


@gates.command()
@click.option('--gates-url', default='http://api.zerinth.com/v1', help='URL of the gates service')
@click.argument('name')
@click.argument('url')
@click.argument('content_type')
@click.argument('period')
@click.argument('tag')
@click.argument('workspace_id')
@click.option('--start', default=None, help='starting time for the query to tsmanager')
@click.option('--end', default=None, help='end time for the query to tsmanager')
@click.option('--device_id', default=None, help='device id for the query to tsmanager')
@click.option('--custom', default=None, help='custom query fields for the query to tsmanager')
def create_webhook(gates_url, name, url, content_type, period, tag, workspace_id, start, end, device_id, custom):
    """Create a webhook gate"""
    client = adm.ADMClient(gates_url=gates_url)
    client.create_webhook(name, url, content_type, period, tag, workspace_id, start, end, device_id, custom)


@gates.command()
@click.option('--gates-url', default='http://api.zerinth.com/v1', help='URL of the gates service')
@click.argument('gate_id')
def get_gate(gates_url, gate_id):
    """Get a gate by its id"""
    client = adm.ADMClient(gates_url=gates_url)
    client.get_gate(gate_id)


@gates.command()
@click.option('--gates-url', default='http://api.zerinth.com/v1', help='URL of the gates service')
@click.option('--status', default=None, help='Use active or disabled to filter results on status')
def get_all_gates(gates_url, status):
    """Get the list of all gates created filtering on status. If no status is passed it get all of them"""
    client = adm.ADMClient(gates_url=gates_url)
    client.get_all_gates(status)

@gates.command()
@click.option('--gates-url', default='http://api.zerinth.com/v1', help='URL of the gates service')
@click.argument('gate_id')
@click.option('--tag', default=None, help="the new tag")
@click.option('--workspace_id', default=None, help="the new workspace_id")
@click.option('--status', default=None, help='the new status for the web hook')
@click.option('--period', default=None, help='the new period for the web hook')
@click.option('--url', default=None, help='the new url for the web hook')
@click.option('--content-type', default=None, help='the new content-type for the web hook')
@click.option('--start', default=None, help='starting time for the query to tsmanager')
@click.option('--end', default=None, help='end time for the query to tsmanager')
@click.option('--device_id', default=None, help='device id for the query to tsmanager')
@click.option('--custom', default=None, help='custom query fields for the query to tsmanager')
def update_webhook(gates_url, gate_id, status, period, url, content_type, tag, workspace_id, start, end, device_id, custom):
    """Update a web hook (status, period, url, content-type, query-string"""
    print(status)
    client = adm.ADMClient(gates_url=gates_url)
    client.update_webhook(gate_id, status, period, url, content_type, tag, workspace_id, start, end, device_id, custom)

@gates.command()
@click.option('--gates-url', default='http://api.zerinth.com/v1', help='URL of the gates service')
@click.argument('gate_id')
def delete_gate(gates_url, gate_id):
    """Delete an existing gate"""
    client = adm.ADMClient(gates_url=gates_url)
    client.delete_gate(gate_id)
