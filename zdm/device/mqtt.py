import json

import paho.mqtt.client as mqtt

from ..logging import ZdmLogger

from .constants import MQTT_PREFIX_JOB, MQTT_PREFIX_REQ_DEV, MQTT_PREFIX_PRIVATE_STATUS, MQTT_PREFIX_STRONG_PRIVATE_STATUS
import sys

logger = ZdmLogger().get_logger()

# def on_message(c, u, m):
#     print("###############################")

class MQTTClient:

# MQTTClient(mqtt_id=self._creds.device_id,
#            clean_session=self._cfg.clean_session,
#            cycle_timeout=self._cfg.cycle_timeout,
#            command_timeout=self._cfg.command_timeout)
    def __init__(self, mqtt_id, clean_session=False, ssl_ctx=None):
        self.client = mqtt.Client(mqtt_id, clean_session=clean_session)
        self.ssl_ctx = ssl_ctx

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message #on_message #
        self.client.on_publish = self.on_publish

        self._ready_msg = {}  # used only for caching the messages to be sent, and print the when they are effectively sent to the broker

        self.connected = False

    def set_username_pw(self, username, password):
        self.client.username_pw_set(username=username, password=password)

    def connect(self, host, port=1883):
        self.client.connect(host, port=port, )
        self.client.loop_start()
        logger.info("Connecting to: {}:{}".format(host, port))

    def on_connect(self, client, userdata, flags, rc):
        # self.connected = True
        # 0: Connection successful
        # 1: Connection refused - incorrect protocol version
        # 2: Connection refused - invalid client identifier
        # 3: Connection refused - server unavailable
        # 4: Connection refused - bad username or password
        # 5: Connection refused - not authorised 6-255: Currently unused.
        logger.info("On connect flags:{}, rc:{}".format(flags, mqtt.error_string(rc)))
        if rc == 0:
            self.connected = True
            logger.info("Successfully connected. Returned code={}".format(rc))
        else:
            self.connected = False
            logger.error("Error in connection. Returned code={}".format(rc))

    def on_disconnect(self, client, userdata, rc):
        logger.info("On disconnect rc:{}".format(rc))
        if rc != 0:
            logger.error("Unexpected disconnection. Return code={}".format(rc))
        else:
            logger.warning("Client disconnected after disconnect() is called. Return code={}".format(rc))
        # TODO; call loop_stop() ??
        # loop_stop

    def publish(self, topic, payload=None, qos=1):
        if isinstance(payload, dict):
            payload_str = json.dumps(payload)
        else:
            payload_str = payload
        try:
            ret = self.client.publish(topic, payload_str, qos=qos)
            self._ready_msg[ret.mid] = payload
        except Exception as e:
            logger.error("Error" + e)

    def on_publish(self, client, userdata, mid):
        payload = self._ready_msg[mid]
        if "key" in payload:
            k = payload["key"]
            if k.startswith((MQTT_PREFIX_JOB, MQTT_PREFIX_REQ_DEV, MQTT_PREFIX_PRIVATE_STATUS, MQTT_PREFIX_STRONG_PRIVATE_STATUS)):
                logger.debug("Publish message: {}".format(payload))
            else:
                logger.info("Publish message: {}".format(payload))
        else:
            logger.info("Publish message: {}".format(payload))
        self._ready_msg.pop(mid, None)

    def on_message(self, client, userdata, msg):
        logger.info("#################### Message received: {}".format(msg))

    def subscribe(self, topic, callback=None, qos=1):
        self.client.subscribe(topic=topic, qos=qos)
        logger.debug("Subscribed to topic: {}".format(topic))
        if callback:
            self.client.message_callback_add(topic, callback)
