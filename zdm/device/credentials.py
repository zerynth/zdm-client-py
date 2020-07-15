import base64

# #-if ZERYNTH_USE_DCZ
# def load_zdevice():
#     ##-if ZDM_LOG_LEVEL <= 0
#     print("DEBUG|zdm.load_zdevice checking DCZ")
#     ##-endif
#     dc = dcz.DCZ([ZERYNTH_DCZ_MAPPING_0], serializers={'json': json})
#     dc.finalize()
#     content = {}
#     ##-if ZDM_LOG_LEVEL <= 0
#     print("DEBUG|zdm.load_zdevice loading devinfo")
#     ##-endif
#     content["devinfo"] = dc.load_resource("devinfo")
#     ##-if ZDM_LOG_LEVEL <= 0
#     print("DEBUG|zdm.load_zdevice loading endpoint")
#     ##-endif
#     content["endpoint"] = dc.load_resource("endpoint")
#     ##-if ZDM_LOG_LEVEL <= 0
#     print("DEBUG|zdm.load_zdevice loading prvkey")
#     ##-endif
#     content["prvkey"] = dc.load_resource("prvkey")
#     ##-if ZDM_LOG_LEVEL <= 0
#     print("DEBUG|zdm.load_zdevice loading clicert")
#     ##-endif
#     content["clicert"] = dc.load_resource("clicert")
#     ##-if ZDM_LOG_LEVEL <= 0
#     print("DEBUG|zdm.load_zdevice loading cacert")
#     ##-endif
#     content["cacert"] = dc.load_resource("cacert")
#     return content
#
# #-else

def load_zdevice():
    ff = open("resource://zdevice.json")
    content = ff.read(len(ff))
    content = json.loads(content)
    if "cacert" in content:
        content["cacert"]=content["cacert"]+"\x00"
    if "clicert" in content:
        content["clicert"]=content["clicert"]+"\x00"
    if "prvkey" in content:
        if content["prvkey"].startswith("-----"):
            content["prvkey"]=content["prvkey"]+"\x00"
        else:
            content["prvkey"] = base64.standard_b64decode(content["prvkey"])
    return content
#-endif

def default_time_func():
    ntp = ntpclient.NTPClient()
    for x in range(0, 5):
        try:
            #-if ZDM_LOG_LEVEL <= 0
            print("DEBUG|Default_time_func get ntp time", x)
            #-endif
            ts = ntp.get_time(unix_timestamp=True)
            break
        except Exception as e:
            #-if ZDM_LOG_LEVEL <= 0
            print("DEBUG|zdm.default_time_func can't get time", e)
            #-endif
            sleep(2000)
    else:
        raise Exception
    return ts

class Credentials():
    def __init__(self):
        try:
            nfo=load_zdevice()
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
            if self.mode=="token" or self.mode=="fixed_token":
                self.ctx=ssl.create_ssl_context(cacert=cacert,options=ssl.SERVER_AUTH, hostname=self.endpoint)
            else:
                self.ctx=ssl.create_ssl_context(cacert=cacert,clicert=clicert,pkey=self.secret,options=ssl.CERT_REQUIRED | ssl.SERVER_AUTH, hostname=self.endpoint)
                self.secret="" #remove from memory
        else:
            self.ctx = None


    def configure_mqtt_client(self, client):
        if self.mode == "fixed_token":
            # secret is the token
            print("DEBUG|zdm.configure_mqtt_client setting fixed_token")
            client.set_username_pw(self.device_id, self.secret)
        elif self.mode == "token":
            token = self.generate_token()
            print("DEBUG|zdm.configure_mqtt_client setting token")
            client.set_username_pw(self.device_id, token)
        else:
            print("DEBUG|zdm.Credentials_configure_mqtt_client unsupported")
            raise Exception("Unsupported credential")

    def generate_token(self):
        # get current timestamp
        ts = default_time_func()
        # build payload
        payload = {"sub": self.device_id,"key": self.key_id, "exp": ts + 3600 }
        print("DEBUG|zdm.Credentials_generate_token payload", payload)
        # encode token
        token = jwt.encode(json.dumps(payload), self.secret,jwt.HS256 if self.key_type=="sym" else jwt.ES256)
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
