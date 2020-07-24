import base64
import json
import os
import time
import tempfile
import ssl
import jwt

from ..logging import ZdmLogger

logger = ZdmLogger().get_logger()

# Load  zdevice.json file
def load_zdevice(root_zdevice, file="zdevice.json"):
    logger.info("Reading zdevice.json path {}".format(root_zdevice))
    with open(os.path.join(root_zdevice, file)) as ff:
        content = json.load(ff)
        return content


def default_time_func():
    return int(time.time())


class Credentials():

    def __init__(self, root_zdevice):
        try:
            logger.debug("Read zdevice.json location path {}".format(root_zdevice))
            nfo = load_zdevice(root_zdevice)
        except Exception as e:
            logger.error("Can't load device provisioning info", e)
            raise e
        self.device_id = nfo["devinfo"]["device_id"]
        self.mode = nfo["devinfo"]["mode"]
        self.secret = nfo["prvkey"]
        self.endpoint = nfo["endpoint"]["host"]
        self.port = nfo["endpoint"]["port"]
        self.key_id = nfo["devinfo"].get("key_id", 0)
        self.key_type = nfo["devinfo"].get("key_type", "sym")

        self.endpoint_mode = nfo["endpoint"].get("mode", "secure")
        logger.info("Credential type: '{}' Endpoint mode: '{}'".format(self.mode, self.endpoint_mode))

        if self.endpoint_mode == "secure":
            if self.mode=="device_token" or self.mode=="cloud_token":
                # Save ca_cert into temporary file
                cacert = nfo.get("cacert", "")
                if cacert != "":
                    self.caCertPath = tempfile.NamedTemporaryFile()
                    # Open the file for writing.
                    with open(self.caCertPath.name, 'w') as f:
                        f.write(cacert)
                else:
                    raise Exception("Empty ca cert file")

            else:
                # Save cli_cert and prvkey into temporary files
                clicert = nfo.get("clicert", "")
                if clicert != "":
                    self.cliCertPath = tempfile.NamedTemporaryFile()
                    with open(self.caCertPath.name, 'w') as f:
                        f.write(clicert)
                if self.secret != "":
                    self.prvKeyClientPath = tempfile.NamedTemporaryFile()
                    # Open the file for writing.
                    with open(self.prvKeyClientPath.name, 'w') as f:
                        f.write(self.secret)

    def configure_mqtt_client(self, client):
        if self.endpoint_mode == "secure":
            if self.mode=="device_token" or self.mode=="cloud_token":
                logger.debug("Reading Ca_cert path", self.caCertPath.name)
                client.client.tls_set(
                    ca_certs=self.caCertPath.name,
                    cert_reqs=ssl.CERT_REQUIRED,
                    tls_version=ssl.PROTOCOL_TLSv1_2
                )
            else:
                logger.debug("Reading cli_cert path", self.caCertPath.name)
                logger.debug("Reading prvkey path", self.caCertPath.name)
                # options=ssl.CERT_REQUIRED | ssl.SERVER_AUT
                client.client.tls_set(
                    ca_certs=self.caCertPath.name,
                    cert_reqs=ssl.CERT_REQUIRED,
                    certfile=self.cliCertPath.name,
                    keyfile=self.prvKeyClientPath.name,
                    tls_version=ssl.PROTOCOL_TLSv1_2,
                )
        if self.mode == "cloud_token":
            logger.debug("Setting cloud token")
            client.set_username_pw(self.device_id, self.secret)
        elif self.mode == "device_token":
            token = self.generate_token()
            logger.debug("Setting device token")
            client.set_username_pw(self.device_id, token)
        else:
            logger.debug("Unsupported mode")
            raise Exception("Unsupported mode")

    def generate_token(self):
        # get current timestamp
        ts = default_time_func()
        payload = {"sub": self.device_id, "key": self.key_id, "exp": ts + 3600}
        logger.debug("Token payload", payload)
        # encode token
        secret = base64.b64decode(self.secret)
        token = jwt.encode(payload, secret, 'HS256' if self.key_type == "sym" else "ES256")
        logger.debug("Token", token)
        return token


class Config():
    def __init__(self, keepalive=60):
        self.keepalive = keepalive
        # self.cycle_timeout=cycle_timeout
        # self.command_timeout=command_timeout
        self.sock_keepalive = [1, 10, 5]
        self.clean_session = True
        self.qos_publish = 0
        self.qos_subscribe = 1
