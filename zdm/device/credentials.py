import base64
import json
import os
import ssl
import jwt
import time

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
def load_zdevice(zdevice_path):
    print("PATH", os.path.dirname(__file__))
    print("ABSPATH",  os.path.abspath('.'))

    with open(os.path.join(zdevice_path, 'zdevice.json')) as ff:
        content = json.load(ff)
        if "cacert" in content:
            content["cacert"]=content["cacert"]+"\x00"
        if "clicert" in content:
            content["clicert"]=content["clicert"]+"\x00"
        if "prvkey" in content:
            if content["prvkey"].startswith("-----"):
                content["prvkey"]=content["prvkey"]+"\x00"
            else:
                content["prvkey"] = base64.b64decode(content["prvkey"])
        crd = Credentials(content)
        return crd


def default_time_func():
   return  int(time.time())

class Credentials():

    # def __init__(self, zdevice):
    #     self.device_id = zdevice["devinfo"]["device_id"]
    #     self.mode = zdevice["devinfo"]["mode"]
    #     self.secret = zdevice["prvkey"]
    #     self.endpoint = zdevice["endpoint"]["host"]
    #     self.port = zdevice["endpoint"]["port"]
    #     self.key_id = zdevice["devinfo"].get("key_id",0)
    #     self.key_type = zdevice["devinfo"].get("key_type","sym")
    #
    #     if zdevice["endpoint"]["mode"] == "secure":
    #         cacert = zdevice.get("cacert","")
    #         clicert = zdevice.get("clicert","")
    #         # if self.mode=="device_token" or self.mode=="cloud_token":
    #         #     # self.ctx=ssl.create_ssl_context(cacert=cacert,options=ssl.SERVER_AUTH, hostname=self.endpoint)
    #         #     self.ctx = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=cacert, )
    #         # else:
    #         #     self.ctx=ssl.create_ssl_context(cacert=cacert,clicert=clicert,pkey=self.secret,options=ssl.CERT_REQUIRED | ssl.SERVER_AUTH, hostname=self.endpoint)
    #         #     self.secret="" #remove from memory
    #     else:
    #         self.ctx = None

    def __init__(self, path_zdevjson):
        try:
            nfo=load_zdevice(path_zdevjson)
        except Exception as e:
            print("DEBUG|zdm.Credentials can't load device provisioning info",e )
            raise e
        self.device_id = nfo["devinfo"]["device_id"]
        self.mode = nfo["devinfo"]["mode"]
        self.secret = nfo["prvkey"]
        self.endpoint = nfo["endpoint"]["host"]
        self.port = nfo["endpoint"]["port"]
        self.key_id = nfo["devinfo"].get("key_id",0)
        self.key_type = nfo["devinfo"].get("key_type","sym")

        if nfo["endpoint"]["mode"] == "secure":
            cacert = nfo.get("cacert","")
            clicert = nfo.get("clicert","")
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
        payload = {"sub": self.device_id,"key": self.key_id, "exp": ts + 3600}
        print("DEBUG|zdm.Credentials_generate_token payload", payload)
        # encode token
        token = jwt.encode(payload, self.secret, 'HS256' if self.key_type=="sym" else "ES256")
        print("DEBUG|zdm.Credentials_generate_token token", token)
        return token

class Config():
    def __init__(self,
                 keepalive=60,
                 cycle_timeout=500,
                 command_timeout=60000):
        self.keepalive=keepalive
        # self.cycle_timeout=cycle_timeout
        # self.command_timeout=command_timeout
        self.sock_keepalive=[1, 10, 5]
        self.clean_session=True
        self.qos_publish=0
        self.qos_subscribe=1
