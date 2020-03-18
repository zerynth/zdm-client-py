import json

from .mqtt import MQTTClient
from ..logging import MyLogger
import time
logger = MyLogger().get_logger()


class VirtualDevice:
    def __init__(self, mqtt_id, rpc=None):
        self.mqtt_id = mqtt_id
        self.rpc = rpc
        self.mqttClient = MQTTClient(mqtt_id=mqtt_id)

        self.data_topic = '/'.join(['j', 'data', mqtt_id])
        self.up_topic = '/'.join(['j', 'up', mqtt_id])
        self.dn_topic = '/'.join(['j', 'dn', mqtt_id])

    def connect(self):
        for _ in range(5):
            try:
                print("VirtualDevice.connect attempt")
                self.mqttClient.connect(host='rmq.adm.zerinth.com')
                break
            except Exception as e:
                print("VirtualDevice.connect", e)
                pass
        time.sleep(2)
        if not self.mqttClient.connected:
            raise Exception("Failed to connect")

        self.subscribe_down()

    def subscribe_down(self):
        self.mqttClient.subscribe(self.dn_topic, callback=self.handle_dn_msg)

    def id(self):
        return self.mqtt_id

    def send_manifest(self):
        payload = {
            'key': '__manifest',
            'value': [k for k in self.rpc]
        }
        self.mqttClient.publish(self.up_topic, json.dumps(payload))

    def set_password(self, pw):
        self.mqttClient.set_username_pw(self.mqtt_id, pw)

    def publish_data(self, tag, payload):
        """ Publish into the ingestion queue on the tag TAG wih the PAYLOAD"""
        topic = self.build_ingestion_topic(tag)
        self.mqttClient.publish(topic, payload)

    def publish_up(self, payload):
        topic = self.up_topic
        self.mqttClient.publish(topic, payload)

    def handle_dn_msg(self, client, data, msg):
        payload = json.loads(msg.payload)
        try:
            if "key" not in payload:
                raise Exception(
                    "The key  is not present into the RPC payload {}".format(payload))
            if "value" not in payload:
                raise Exception(
                    "The value  is not present into the RPC payload {}".format(payload))

            method = payload["key"]
            value = payload["value"]
            args = value["args"]

            if method.startswith('@'):
                method = method[1:]

            if method in self.rpc:
                result = self.rpc[method](self, args)
                logger.info("[{}] rpc {} executed with result res:{} ".format(
                    self.id, method, result))

                rpc_response = {
                    "key": "@" + method,
                    "value": {"status": "done", "result": result}
                }

                self.publish_up(json.dumps(rpc_response))
            else:
                logger.info("[{}] rpc {} not supported ".format(
                    self.id, method))

                rpc_response = {
                    "key": "@" + method,
                    "value": {"status": "failed", "message": "method not supported"}
                }

                self.publish_up(json.dumps(rpc_response))

        except Exception as e:
            logger.error("Error", e)

    def build_ingestion_topic(self, tag):
        """ build the topic for the ingestion
        ex.  data/<deviceid>/<TAG>/

        """
        return '/'.join([self.data_topic, tag])

    def start_loop(self):
        self.mqttClient.loop()
