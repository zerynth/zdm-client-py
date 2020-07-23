import base64
import json
import os
import time

import jwt

from ..logging import ZdmLogger

logger = ZdmLogger().get_logger()


# def load_zdevice(path):
#     with open(os.path.join(path, 'zdevice.json')) as ff:
#         content = json.load(ff)
#         if "cacert" in content:
#             content["cacert"]=content["cacert"]+"\x00"
#         if "clicert" in content:
#             content["clicert"]=content["clicert"]+"\x00"
#         if "prvkey" in content:
#             if content["prvkey"].startswith("-----"):
#                 content["prvkey"]=content["prvkey"]+"\x00"
#             else:
#                 content["prvkey"] = base64.b64decode(content["prvkey"])
#         return content


# load credential from zdevice.json file
def load_zdevice(root_zdevice, file="zdevice.json"):
    with open(os.path.join(root_zdevice, file)) as ff:
        content = json.load(ff)
        if "cacert" in content:
            content["cacert"] = content["cacert"] + "\x00"
        if "clicert" in content:
            content["clicert"] = content["clicert"] + "\x00"
        if "prvkey" in content:
            if content["prvkey"].startswith("-----"):
                content["prvkey"] = content["prvkey"] + "\x00"
            else:
                content["prvkey"] = base64.b64decode(content["prvkey"])
        crd = Credentials(content)
        return crd


def default_time_func():
    return int(time.time())


class Credentials():

    # def __init__(self, device_id, crd_mode, prvkey, crd_key_id=0, cred_key_type="sym", endpoint_host="zmqtt.zdm.zerynth.com", endpoint_port="88883", endpoint_mode="secure",  cacert="", clicert=""):
    #     self.device_id = device_id
    #     if crd_mode is not "device_token" or "cloud_token":
    #         raise Exception("Credential mode not valid. Want %s  | %s Given".format("device_token", "cloud_token", crd_mode))
    #     self.mode = crd_mode  #"device_token" "cloud_token
    #     self.key_id = crd_key_id
    #     self.key_type = cred_key_type
    #
    #     self.secret = prvkey
    #     self.endpoint = endpoint_host
    #     self.port = endpoint_port
    #
    #     if endpoint_mode == "secure":
    #         # cacert = zdevice.get("cacert","")
    #         # clicert = zdevice.get("clicert","")
    #         cacert = cacert
    #         clicert = clicert
    #         # self.ctx = ssl.
    #         # if self.mode=="device_token" or self.mode=="cloud_token":
    #         #     # self.ctx=ssl.create_ssl_context(cacert=cacert,options=ssl.SERVER_AUTH, hostname=self.endpoint)
    #         #     self.ctx = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=cacert, )
    #         # else:
    #         #     self.ctx=ssl.create_ssl_context(cacert=cacert,clicert=clicert,pkey=self.secret,options=ssl.CERT_REQUIRED | ssl.SERVER_AUTH, hostname=self.endpoint)
    #         #     self.secret="" #remove from memory
    #     else:
    #         self.ctx = None

    def __init__(self, root_zdevice):
        try:
            logger.debug("Read zdevice.json location path {}".format(root_zdevice))
            nfo = load_zdevice(root_zdevice)
        except Exception as e:
            logger.info("DEBUG|zdm.Credentials can't load device provisioning info", e)
            raise e
        self.device_id = nfo["devinfo"]["device_id"]
        self.mode = nfo["devinfo"]["mode"]
        self.secret = nfo["prvkey"]
        self.endpoint = nfo["endpoint"]["host"]
        self.port = nfo["endpoint"]["port"]
        self.key_id = nfo["devinfo"].get("key_id", 0)
        self.key_type = nfo["devinfo"].get("key_type", "sym")

        if nfo["endpoint"]["mode"] == "secure":
            cacert = nfo.get("cacert", "")
            clicert = nfo.get("clicert", "")
            # if self.mode=="device_token" or self.mode=="cloud_token":
            #     # self.ctx=ssl.create_ssl_context(cacert=cacert,options=ssl.SERVER_AUTH, hostname=self.endpoint)
            #     self.ctx = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=cacert, )
            # else:
            #     self.ctx=ssl.create_ssl_context(cacert=cacert,clicert=clicert,pkey=self.secret,options=ssl.CERT_REQUIRED | ssl.SERVER_AUTH, hostname=self.endpoint)
            #     self.secret="" #remove from memory
        else:
            self.ctx = None

    def configure_mqtt_client(self, client):
        if self.mode == "cloud_token":
            print("DEBUG|zdm.configure_mqtt_client setting fixed_token")
            client.set_username_pw(self.device_id, self.secret)
        elif self.mode == "device_token":
            token = self.generate_token()
            print("DEBUG|zdm.configure_mqtt_client setting token")
            client.set_username_pw(self.device_id, token)
        else:
            print("DEBUG|zdm.Credentials_configure_mqtt_client unsupported")
            raise Exception("Unsupported mode")

    def generate_token(self):
        # get current timestamp
        ts = default_time_func()
        payload = {"sub": self.device_id, "key": self.key_id, "exp": ts + 3600}
        print("DEBUG|zdm.Credentials_generate_token payload", payload)
        # encode token
        token = jwt.encode(payload, self.secret, 'HS256' if self.key_type == "sym" else "ES256")
        print("DEBUG|zdm.Credentials_generate_token token", token)
        return token


class Config():
    def __init__(self,
                 keepalive=60,
                 cycle_timeout=500,
                 command_timeout=60000):
        self.keepalive = keepalive
        # self.cycle_timeout=cycle_timeout
        # self.command_timeout=command_timeout
        self.sock_keepalive = [1, 10, 5]
        self.clean_session = True
        self.qos_publish = 0
        self.qos_subscribe = 1
