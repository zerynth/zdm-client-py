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

    def __init__(self, rpc_url="http://127.0.0.1:7777", fleetdev_url="http://127.0.0.1:8000"):
        self.rpc_url = rpc_url
        self.fleet_dev_url = fleetdev_url
    
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
        payload = {"name": name, "FleetID":fleetId}
        print("Creating device {}".format(name))
        path = "{}/device/".format(self.fleet_dev_url)
        print(path)
        r = requests.post(path, data=json.dumps(payload))
        print(r.status_code)
        print(r.text)
    
    def get_device(self, id):
        path = "{}/device/{}".format(self.fleet_dev_url, id)
        print("Get a singel device")
        r  = requests.get(path)
        print(r.text)

    def create_fleet(self, name):
        payload = {"Name": name}
        path = "{}/fleet/".format(self.fleet_dev_url)
        print(path)
        r = requests.post(self.fleet_dev_url, payload)
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
        logger.info("Get a single fleet".format(path))
        r = requests.get(path)
        print(r.status_code)
        print(r.text)