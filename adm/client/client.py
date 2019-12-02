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

    def __init__(self, rpc_url="http://127.0.0.1:7777"):
        self.rpc_url = rpc_url
    
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