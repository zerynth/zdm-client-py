import json

from .mqtt import MQTTClient
from ..logging import MyLogger

logger = MyLogger().get_logger()

class VirtualDevice:

    def __init__(self, uuid, username, password, hostname="localhost", port=1883, rpc=None):
        self.uuid = uuid
        self.rpc = rpc

        if uuid != username:
            raise Exception("The Device id must be equal to the MQTT username. Given {},{}", uuid, username)

        logger.info("User: {}".format(username))
        logger.info("Password: {}".format(password))

        self.mqtt = MQTTClient(hostname, username, password,  port)

        self.topic_data = "j/data"  # topic for the ingestion queue
        self.topic_up = "j/up/"     # topic for the up queue
        self.topic_down = "j/dn/#"  # topic for the down queue

    def connect(self):
        self.mqtt.connect()
        self.subscribe_down()  # subscribe to the down queue to receive data from the adm cloud

    def connect(self):
        for _ in range(5):
            try:
                logger.info("Trying to connect...")
                self.mqtt.connect()
                self.mqtt.loop()
                break
            except Exception as e:
                print("Virtual device", e)
                pass
        else:
            raise IOError
        self._config()

    def _config(self):
        self.subscribe_down()

    @property
    def id(self):
        return self.uuid

    def publish_data(self, tag, payload):
        """ Publish into the ingestion queue on the tag TAG wih the PAYLOAD"""
        topic = self.build_ingestion_topic(self.id, tag)
        self.mqtt.publish(topic, payload, qos=1)


    def publish_up(self, payload):
        topic = self.topic_up + self.uuid
        self.mqtt.publish(topic, payload)


    def subscribe_down(self):
        self.mqtt.subscribe(self.topic_down, qos=1)
        self.mqtt.mqttc.message_callback_add(
            self.topic_down, self._on_message_down_queuue)

    def _on_message_down_queuue(self, client, userdata, msg):
        payload = json.loads(msg.payload)
        logger.info("[{}] received from topic: {}, payload: {}".format(
            self.id, msg.topic, str(payload)))
        try:
            if "key" not in payload:
                raise Exception(
                    "The key  is not present into the RPC payload {}".format(payload))
            if "value" not in payload:
                raise Exception(
                    "The value  is not present into the RPC payload {}".format(payload))
                # if "args" not in payload:
                #    raise Exception(
                #        "The key 'args' is not present into the RPC payload {}".format(payload))
            if payload["key"] == "rpc":
                result = self.rpc[payload['method']](self, payload["args"])

                logger.info("[{}] rpc {} executed with result res:{} ".format(
                    self.id, payload['method'], result))
                rpc_response = {
                    "rpc": payload["rpc"],
                    "method": payload["method"],
                    "args": payload["args"],
                    "status": "done",
                    "result": result
                }
                self.publish_up(json.dumps(rpc_response))
            else:
                raise Exception(
                    "BAd format key ".format(payload))

        except Exception as e:
            logger.error("Error", e)

    def build_ingestion_topic(self, device_id, tag):
        """ build the topic for the ingestion
        ex.  data/<deviceid>/<TAG>/

        """
        return "{}/{}/{}/".format(self.topic_data, device_id, tag)
