import paho.mqtt.client as mqtt
import json

from ..logging import MyLogger

logger = MyLogger().get_logger()


class MQTTClient(object):

    def __init__(self, hostname="localhost", port=1883, user="admin", password="Z3rynthT3st"):
        self.hostname = hostname
        self.port = port
        self.mqttc = mqtt.Client()
        self.mqttc.username_pw_set(username=user, password=password)

        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message

    def connect(self):
        logger.debug("Connecting to {}:{}.".format(self.hostname, self.port))
        self.mqttc.connect(self.hostname, self.port, 60)

    def publish(self, topic, payload=None, qos=0):
        # print("publishing {} into {}".format(payload,  topic))
        if type(payload) is dict:
            payload = json.dumps(payload)
        self.mqttc.publish(topic, payload, qos)
        logger.info("Publish on Topic: {}, Data:{}".format(topic, payload))

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        logger.info("Connected succesfully with code:{}.".format(str(rc)))

    # The callback for when a PUBLISH message is received from the server.

    def on_message(self, client, userdata, msg):
        logger.info("Message received from topic: {}, data:{}".format(
            msg.topic, str(msg.payload)))

    def subscribe(self, topic, qos=0):
        self.mqttc.subscribe(topic, qos)
        logger.info("Subscried to topic: {}".format(topic))

    def loop(self):
        self.mqttc.loop_forever()
