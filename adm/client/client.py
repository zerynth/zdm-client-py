import json

import requests

from ..logging import MyLogger
from .errors import NotFoundError
from .models import Device, Workspace, Fleet

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
                status_url="http://127.0.0.1:8002",
                tsmanager_url="http://127.0.0.1:8005",
                gates_url="http://127.0.0.1:8007"):
        self.rpc_url = rpc_url
        self.fleet_dev_url = fleetdev_url
        self.accounts_url = accounts_url
        self.status_url = status_url
        self.tsmanager_url = tsmanager_url
        self.workspace_url = workspace_url
        self.gates_url = gates_url

    def send_rpc(self, payload):
        # {"rpc":1, "method":"get_temp", "args":null, "status": "pendind"}
        r = requests.post(self.rpc_url + "/rpc", data=json.dumps(payload))
        print(r.status_code)
        print(r.text)

    def get_rpc(self, rpc_id, dev_id):
        # http://127.0.0.1:7777/rpc/2/device/dev01
        path = "{}/rpc/{}/device/{}".format(self.rpc_url, rpc_id, dev_id)
        logger.info("Get rpc status {}".format(path))
        r = requests.get(path)
        print(r.text)

    def create_device(self, name, fleetId=None):
        # if fleetid is None, the device is assigned to a default fleet of the account.
        payload = {"name": name, "fleet_id": None if fleetId is None else fleetId}
        path = "{}/device/".format(self.fleet_dev_url, fleetId)
        logger.info("Creating device {}: {}".format(name, path))
        r = requests.post(path, data=json.dumps(payload))
        if r.status_code == 200:
            data = r.json()
            return Device.from_json(data)
        else:
            logger.info(r.text)
            logger.error("Error creating the device")
            raise NotFoundError(r.text)

    def get_device(self, id):
        path = "{}/device/{}/".format(self.fleet_dev_url, id)
        logger.info("Getting the device {}".format(path))
        r = requests.get(path)
        if r.status_code == 200:
            data = r.json()
            return Device.from_json(data)
        else:
            logger.info(r.text)
            logger.error("Error in getting the device {}")
            raise NotFoundError(r.text)


    def update_device_fleet(self, device_id, name, fleet_id):
        path = "{}/device/{}".format(self.fleet_dev_url, device_id)
        logger.info("Updating device {}: path".format(device_id, path))
        payload = {"Name": name, "FleetID": fleet_id}
        r = requests.put(path, json=payload)
        print(r.status_code)
        print(r.text)

    def get_devices(self):
        path = "{}/device".format(self.fleet_dev_url)
        logger.info("Get all the Devices")
        r = requests.get(path)
        print(r.text)
        print(r.text)

    def get_device_workspace(self, devid):
        path = "{}/device/{}/workspace".format(self.fleet_dev_url, devid)
        logger.info("Get the workspace of a device")
        r = requests.get(path)
        if r.status_code == 200:
            data = r.json()
            return Workspace.from_json(data)
        else:
            logger.error("Error in getting the workspace of a device {}".format(r.text))
            raise NotFoundError(r.text)


    def create_fleet(self, name, workspace_id):
        payload = {"Name": name, "workspace_id":workspace_id}
        path = "{}/fleet/".format(self.fleet_dev_url)
        logger.debug("Path create fleet: {}".format(path))
        logger.info("Creating fleet: {}".format(name))
        r = requests.post(path, data=json.dumps(payload))
        if r.status_code == 200:
            data = r.json()
            return Fleet.from_json(data)
        else:
            logger.error("Error in getting the workspace {}".format(r.text))
            raise NotFoundError(r.text)


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
        if r.status_code == 200:
            data = r.json()
            return Fleet.from_json(data)
        else:
            logger.info(r.text)
            logger.error("Error in getting the fleet {}")
            raise NotFoundError(r.text)


    def register(self, name, password, email):
        path = "{}/account".format(self.accounts_url)
        logger.info("Registering an account: {}".format(path))
        payload = {"name": name, "password": password, "mail": email}
        r = requests.post(path, data=json.dumps(payload))
        if r.status_code == 200:
            logger.info("Account registered correctly")
            return True
        else:
            logger.error("Error in registering the account")
            return False

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

    def create_workspace(self, name):
        path = "{}/workspace/".format(self.workspace_url)
        logger.info("Creating a workspace: {}".format(path))
        r = requests.post(path, json={"Name": name})
        if r.status_code == 200:
            data = r.json()
            return Workspace.from_json(data)
        else:
            logger.error("Error in getting the workspace {}".format(r.text))
            raise NotFoundError(r.text)

    def workspace_all(self):
        path = "{}/workspace/".format(self.workspace_url)
        logger.info("Get all the workspaces".format(path))
        r = requests.get(path)
        print(r.status_code)
        print(r.text)

    def get_workspace(self, workspace_id):
        path = "{}/workspace/{}".format(self.workspace_url, workspace_id)
        logger.info("Get the {} workspace: {}".format(workspace_id, path))
        r = requests.get(path)
        if r.status_code == 200:
            data = r.json()
            return Workspace.from_json(data)
        else:
            logger.error("Error in getting the workspace {}".format(r.text))
            raise NotFoundError(r.text)

    def create_changeset(self, key, value, targets):
        path = "{}/changeset".format(self.status_url)
        logger.info("Creating a changeset: {}".format(self.status_url))
        payload = {"key": key, "value": value, "targets": targets}
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

    def create_workspace_table(self, workspace_id):
        path = "{}/workspacetable".format(self.tsmanager_url)
        logger.info("Creating a workspace table with id: {}".format(workspace_id))
        payload = {"workspaceID": workspace_id}
        r = requests.post(path, json=payload)
        print(r.status_code)
        print(r.text)

    def insert_row(self, timestamp_device, tag, device_id, payload, workspace_id):
        path = "{}/insertrow".format(self.tsmanager_url)
        logger.info("For current timestamp use $(date -u + \"%Y-%m-%dT%H:%M:%SZ\")")
        logger.info("Inserting a row in the workspace: {}".format(workspace_id))
        payload = {"timestampDevice": timestamp_device, "tag": tag, "deviceID": device_id, "payload": payload,
                   "workspaceID": workspace_id}
        r = requests.post(path, json=payload)
        print(r.status_code)
        print(r.text)

    def list_workspace_tags(self, workspace_id):
        path = "{}/workspace/{}/tags".format(self.tsmanager_url, workspace_id)
        logger.info("Get all the tags for the workspace with id {}: {}".format(workspace_id, path))
        r = requests.get(path)
        print(r.status_code)
        print(r.text)

    def get_tag(self, workspace_id, tag, start=None, end=None, device_id=None, custom=None):
        path = "{}/workspace/{}/tag/{}?deviceid={}&start={}&end={}&custom={}".format(self.tsmanager_url, workspace_id,
                                                                                     tag,
                                                                                     "" if device_id is None else device_id,
                                                                                     "" if start is None else start,
                                                                                     "" if end is None else end,
                                                                                     "" if custom is None else custom)
        logger.info("Get custom tag query for {} tag: {}".format(tag, path))
        payload = {'start': None if start is None else start, 'end': None if end is None else end,
                   'device_id': None if device_id is None else device_id, 'custom': None if custom is None else custom}
        r = requests.get(path, params=payload)

        print(r.status_code)
        print(r.text)

    def create_webhook(self, name, url, content_type, period):
        path = "{}/gate/".format(self.gates_url)
        logger.info("Creating a new webhook gate: {}".format(path))
        payload = {"name":name, "url":url, "content-type":content_type, "period":period}
        r = requests.post(path, json=payload)
        print(payload)
        print(r.status_code)
        print(r.text)

    def get_gate(self, gate_id):
        path = "{}/gate/{}".format(self.gates_url, gate_id)
        logger.info("Getting information of gate {}: {}".format(gate_id, path))
        r = requests.get(path)
        print(r.status_code)
        print(r.text)

    def get_all_gates(self, status=None):
        path = "{}/gate?status={}".format(self.gates_url, "" if status is None else status)
        logger.info("Getting list of gates with {} status: {}".format("any" if status is None else status, path))
        r = requests.get(path)
        print(r.status_code)
        print(r.text)

    def update_gate_status(self, gate_id, status):
        path = "{}/gate/{}".format(self.gates_url, gate_id)
        payload = {"status":status}
        r = requests.put(path, json=payload)
        print(r.status_code)
        print(r.text)

    def delete_gate(self, gate_id):
        path = "{}/gate/{}".format(self.gates_url, gate_id)
        logger.info("Deleting gate {}: {}".format(gate_id, path))
        r = requests.delete(path)
        print(r.status_code)
        print(r.text)