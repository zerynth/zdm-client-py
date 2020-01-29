import click
import adm

@click.group()
def account():
    """Manage the account"""
    pass

@account.command()
@click.option('--accounts-url', default='http://api.zerinth.com/v1', help='URL of the Account Service')
@click.argument('name')
@click.argument('password')
@click.argument('email')
def add_account(accounts_url, name, password, email):
    """Register an Account"""
    client = adm.ADMClient(accounts_url=accounts_url)
    client.add_account(name, password, email)


@account.command()
@click.option('--accounts-url', default='http://api.zerinth.com/v1', help='Accounts endpoint')
@click.option('--email', prompt=True)
@click.option("--password", prompt=True, hide_input=True)
def login(accounts_url, email, password):
    """Login an account"""
    client = adm.ADMClient(accounts_url=accounts_url)
    client.account_login(email, password)
    
@account.command()
@click.option('--accounts-url', default='http://api.zerinth.com/v1', help='Accounts endpoint')
@click.argument("account_id")
@click.argument("name")
@click.argument('email')
@click.argument("password")
def add(accounts_url,account_id,  name, email, password):
    """Add a new user to an account"""
    client = adm.ADMClient(accounts_url=accounts_url)
    client.add_user(account_id, name, password, email)
    # bpipCUGKYb

@account.command()
@click.option('--accounts-url', default='http://api.zerinth.com/v1', help='Accounts endpoint')
@click.argument("account_id")
def users(accounts_url, account_id):
    """Get users of an account"""
    client = adm.ADMClient(accounts_url=accounts_url)
    client.get_users(account_id)

@account.command()
@click.option('--accounts-url', default='http://api.zerinth.com/v1', help='Accounts endpoint')
@click.option("--email", prompt=True)
@click.option("--password", prompt=True, hide_input=True)
def user_login(accounts_url,email, password):
    """Login an user"""
    client = adm.ADMClient(accounts_url=accounts_url)
    client.user_login(email, password)

@account.command()
@click.option('--accounts-url', default='http://api.zerinth.com/v1', help='Accounts endpoint')
@click.argument("account_id")
def get(accounts_url, account_id):
    """Get an account"""
    client = adm.ADMClient(accounts_url=accounts_url)
    client.get_account(account_id)