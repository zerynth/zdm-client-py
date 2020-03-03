import paho.mqtt.client as mqtt
import json

from ..logging import MyLogger

logger = MyLogger().get_logger()


class MQTTClient(object):

    def __init__(self, hostname="localhost", user="admin", password="Z3rynthT3st",port=1883):
        self.hostname = hostname
        self.port = port
        self.user = user
        self.password = password

        logger.debug("Creating clinet")
        self.mqttc = mqtt.Client(client_id=user)

        self.mqttc.username_pw_set(username=user, password=password)

        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_disconnect = self.on_disconnect
        self.mqttc.on_message = self.on_message
        self.mqttc.on_publish = self.on_publish

    def on_disconnect(client, userdata, rc):
        logger.info("DISCONNECTED {}".format(client))

    def connect(self):
        logger.info("Connecting to {} {} ".format(self.hostname, self.port))
        self.mqttc.connect(self.hostname, self.port, 60)
        # logger.debug("Connected to {}:{}. user:{}, password:{}".format(self.hostname, self.port, self.user, self.password))

    def publish(self, topic, payload=None, qos=1):
        if type(payload) is dict:
            payload = json.dumps(payload)
        self.mqttc.publish(topic, payload, qos)
        # logger.info("Publish on Topic: {}, Data:{}".format(topic, payload))

    def on_connect(self,vclient, userdata, flags, rc):
        logger.info("Connected succesfully with code: {}.".format(str(rc)))

    def on_publish(self, client, userdata, mid):
        logger.info("Msg published from {} succesfully. {}. mid {}".format(client, userdata, mid))

    def on_message(client, userdata, msg):
        logger.info("Message received from topic: {}, data:{}".format(
            msg.topic, str(msg.payload)))

    def subscribe(self, topic, qos=0):
        self.mqttc.subscribe(topic, qos)
        logger.info("Subscried to topic: {}".format(topic))

    def loop(self):
        self.mqttc.loop_forever()
