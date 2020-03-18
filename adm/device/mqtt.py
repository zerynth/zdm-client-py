import paho.mqtt.client as mqtt
import json

from ..logging import MyLogger

logger = MyLogger().get_logger()


class MQTTClient:

    def __init__(self, mqtt_id, ssl_ctx=None):
        self.client = mqtt.Client(mqtt_id)
        self.ssl_ctx = ssl_ctx

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish

        self.connected = False

    def set_username_pw(self, username, password):
        self.client.username_pw_set(username=username, password=password)

    def connect(self, host, port=1883):
        self.client.connect(host, port=port)
        self.client.loop_start()
        logger.info("Connecting to: {}:{}".format(host, port))

    def on_connect(self, client, userdata, flags, rc):
        print("on_connect")
        self.connected = True
        if rc == 0:
            print("connected OK Returned code=", rc)
        else:
            print("Bad connection Returned code=", rc)

    def on_disconnect(self, client, userdata, rc):
        print("Unexpected disconnection.")
        self.client.loop_stop()

    def publish(self, topic, payload=None, qos=1):
        if type(payload) is dict:
            payload = json.dumps(payload)
        try:
            self.client.publish(topic, payload, qos=qos)
            logger.info("Msg published to topic: {}".format(topic))
        except Exception as e:
            print("Error" + e)

    def on_publish(self, client, userdata, mid):
        logger.info("Msg published from {} succesfully. {}. mid {}".format(client, userdata, mid))

    def on_message(client, userdata, msg):
        logger.info("Message received: {}".format(msg))

    def subscribe(self, topic, callback=None, qos=1):
        self.client.subscribe(topic=topic, qos=qos)
        logger.info("Subscribed to topic: {}".format(topic))

        if callback:
            self.client.message_callback_add(topic, callback)

    def loop(self):
        self.client.loop_forever()
