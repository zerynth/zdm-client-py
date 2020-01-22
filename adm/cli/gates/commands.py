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
def create_webhook(gates_url, name, url, content_type, period):
    """Create a webhook gate"""
    client = adm.ADMClient(gates_url=gates_url)
    client.create_webhook(name, url, content_type, period)


@gates.command()
@click.option('--gates-url', default='http://api.zerinth.com/v1', help='URL of the gates service')
@click.argument('gate_id')
def get_gate(gates_url, gate_id):
    """Get a gate by its id"""
    client = adm.ADMClient(gates_url=gates_url)
    client.get_gate(gate_id)


@gates.command()
@click.option('--gates-url', default='http://api.zerinth.com/v1', help='URL of the gates service')
@click.option('status', default=None, help='Use active or disabled to filter results on status')
def get_all_gates(gates_url, status):
    """Get the list of all gates created filtering on status. If no status is passed it get all of them"""
    client = adm.ADMClient(gates_url=gates_url)
    client.get_all_gates(status)

@gates.command()
@click.option('--gates-url', default='http://api.zerinth.com/v1', help='URL of the gates service')
@click.argument('gate_id')
@click.argument('status')
def update_status(gates_url, gate_id, status):
    """Update the status of a gate"""
    client = adm.ADMClient(gates_url=gates_url)
    client.update_gate_status(gate_id, status)

@gates.command()
@click.option('--gates-url', default='http://api.zerinth.com/v1', help='URL of the gates service')
@click.argument('gate_id')
def delete_gate(gates_url, gate_id):
    """Delete an existing gate"""
    client = adm.ADMClient(gates_url=gates_url)
    client.delete_gate(gate_id)
