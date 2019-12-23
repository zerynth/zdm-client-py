import requests
import json

from ..logging import MyLogger

logger = MyLogger().get_logger()

class ADMClient(object):
    """
    A client for communicating with a ADM server.
    Example:
        >>> import adm
        >>> client = adm.ADMClient(rpc_url="http://127.0.0.1:8000")
    
    """

    def __init__(self, rpc_url="http://127.0.0.1:7777", 
                fleetdev_url="http://127.0.0.1:8000", 
                accounts_url="http://127.0.0.1:8001", 
                workspace_url="http://127.0.0.1:8001",
                status_url="http://127.0.0.1_8002"):
        self.rpc_url = rpc_url
        self.fleet_dev_url = fleetdev_url
        self.accounts_url = accounts_url
        self.status_url = status_url
        self.workspace_url = workspace_url
    
    def send_rpc(self, payload):
        # {"rpc":1, "method":"get_temp", "args":null, "status": "pendind"}
        r = requests.post(self.rpc_url+"/rpc", data=json.dumps(payload))
        print(r.status_code)
        print(r.text)
    
    def get_rpc(self, rpc_id, dev_id):
        # http://127.0.0.1:7777/rpc/2/device/dev01
        path = "{}/rpc/{}/device/{}".format(self.rpc_url, rpc_id, dev_id)
        logger.info("Get rpc status {}".format(path))
        r = requests.get(path)
        print(r.text)

    def create_device(self, name, fleetId=None):
        # if fleetid is None, the device is assigned to a defualt fleet of the account.
        payload = {"name": name,"FleetID":("" if fleetId is None else fleetId )}
        print("Creating device {}".format(name))
        path = "{}/device/".format(self.fleet_dev_url, fleetId)
        print(path)
        r = requests.post(path, data=json.dumps(payload))
        print(r.status_code)
        print(r.text)
    
    def get_device(self, id):
        path = "{}/device/{}".format(self.fleet_dev_url, id)
        print("Get a single device")
        r  = requests.get(path)
        print(r.text)
    
    def update_device_fleet(self, device_id, name , fleet_id):
        path = "{}/device/{}".format(self.fleet_dev_url, device_id)
        logger.info("Updating device {}: path".format(device_id, path))
        payload = {"Name": name, "FleetID": fleet_id}
        r = requests.put(path, json=payload)
        print(r.status_code)
        print(r.text)


    def get_devices(self):
        path = "{}/device".format(self.fleet_dev_url )
        logger.info("Get all the Devices")
        r  = requests.get(path)
        print(r.text)
        print(r.text)
        
    def create_fleet(self, name):
        payload = {"Name": name}
        path = "{}/fleet/".format(self.fleet_dev_url)
        logger.debug("Path create fleet: {}".format(path))
        logger.info("Creating fleet: {}".format(name))
        r = requests.post(path, data=json.dumps(payload))
        print(r.status_code)
        print(r.text)

    def get_fleets(self):
        path = "{}/fleet".format(self.fleet_dev_url)
        logger.info("Get all the fleets".format(path))
        r = requests.get(path)
        print(r.status_code)
        print(r.text)
        

    def get_fleet(self, id):
        path = "{}/fleet/{}".format(self.fleet_dev_url, id)
        logger.info("Get a single fleet: {}".format(path))
        r = requests.get(path)
        print(r.status_code)
        print(r.text)

    def register(self, name, password, email):
        path = "{}/account".format(self.accounts_url)
        logger.info("Registering an account: {}".format(path))
        payload = {"name": name, "password": password, "mail": email}
        r = requests.post(path, data=json.dumps(payload))
        print(r.status_code)
        print(r.text)

    def account_login(self, email, password):
        path = "{}/account/login/{}/{}".format(self.accounts_url, email, password)
        logger.info("Login a account: {}".format(path))
        r = requests.get(path)
        print(r.status_code)
        print(r.text)
    
    def get_account(self, account_id):
        path = "{}/account/{}".format(self.accounts_url, account_id)
        logger.info("Get an account: {}".format(path))
        r = requests.get(path)
        print(r.status_code)
        print(r.text)

    def add_user(self, account_id, name, password, email):
        path = "{}/account/{}/user".format(self.accounts_url, account_id)
        logger.info("Adding user {} to account {}: {}".format(name, account_id, path))
        payload = {"name": name, "password": password, "mail": email}
        r = requests.post(path, json=payload)
        print(r.status_code)
        print(r.text)
    
    def get_users(self, account_id):
        path = "{}/account/{}/users".format(self.accounts_url, account_id)
        logger.info("get users of account id {}: {}".format(account_id, path))
        r = requests.get(path)
        print(r.status_code)
        print(r.text)
    
    def user_login(self, email, password):
        path = "{}/user/login/{}/{}".format(self.accounts_url, email, password)
        logger.info("Login an user: {}".format(path))
        r = requests.get(path)
        print(r.status_code)
        print(r.text)

    def workspace_create(self, name):
        path = "{}/workspace/".format(self.workspace_url)
        logger.info("Creating a workspace: {}".format(path))
        r = requests.post(path, json={"Name":name})
        print(r.status_code)
        print(r.text)

    def workspace_all(self):
        path = "{}/workspace/".format(self.workspace_url)
        logger.info("Get all the workspaces".format(path))
        r = requests.get(path)
        print(r.status_code)
        print(r.text)
        
    def workspace_get(self, workspace_id):
        path = "{}/workspace/{}".format(self.workspace_url, workspace_id)
        logger.info("Get the {} workspace: {}".format(workspace_id, path))
        r = requests.get(path)
        print(r.status_code)
        print(r.text)

    def create_changeset(self, key, value, targets):
        path = "{}/changeset".format(self.status_url)
        logger.info("Creating a changeset: {}".format(self.status_url))
        payload = {"key":key, "value":value, "targets":targets}
        r = requests.post(path, json=payload)
        print(r.status_code)
        print(r.text)

    def get_changeset(self, changeset_id):
        path = "{}/changeset/{}".format(self.status_url, changeset_id)
        logger.info("Get the {} changeset: {}".format(changeset_id, path))
        r = requests.get(path)
        print(r.status_code)
        print(r.text)

    def get_current_status(self, device_id):
        path = "{}/currentstatus/{}".format(self.status_url, device_id)
        logger.info("Get the current status of {} device: {}".format(device_id, path))
        r = requests.get(path)
        print(r.status_code)
        print(r.text)

    def get_expected_status(self, device_id):
        path = "{}/expectedstatus/{}".format(self.status_url, device_id)
        logger.info("Get the expected status of {} device: {}".format(device_id, path))
        r = requests.get(path)
        print(r.status_code)
        print(r.text)