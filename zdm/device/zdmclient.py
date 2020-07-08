"""
.. module:: zerynthzdmclient

.. _lib.zerynth.zdmclient:

**********************
ZDM Client Python
**********************

The Zerynth ZDM Client is a Python implementation of a client of the ZDM.
It can be used to emulate a Zerynth device and connect it to the ZDM.

    """

import datetime
import json
import logging
import time

from .constants import MQTT_PREFIX_REQ_DEV, MQTT_PREFIX_JOB, MQTT_PREFIX_STRONG_PRIVATE_STATUS, MQTT_KEY_FOTA
from .mqtt import MQTTClient
from ..logging import ZdmLogger

logger = ZdmLogger().get_logger()

ENDPOINT = "mqtt.zdm.zerynth.com"
PORT = 1883


class ZDMClient:
    """
================
The ZDMClient class
================

.. class:: ZDMClient(device_id, jobs=None, endpoint=ENDPOINT, verbose=False, time_callback=None)

    Creates a ZDM client instance with device id :samp:`device_id`. All other parameters are optional and have default values.

    * :samp:`device_id` is the id of the device.
    * :samp:`jobs` is the dictionary that defines the device's available jobs (default None).
    * :samp:`condition_tags` is the list of condition tags that the device can open and close (default []).
    * :samp:`endpoint` is the url of the ZDM broker (default rmq.zdm.zerynth.com).
    * :samp:`verbose` boolean flag for verbose output (default False).
    * :samp:`on_timestamp` called when the ZDM responds to the timestamp request. on_timestamp(client, timestamp)
    * :samp:`on_open_conditions` called when the ZDM responds to the open conditions request. on_open_conditions(client, conditions)

    """
    def __init__(self, device_id,
                 endpoint=ENDPOINT,
                 jobs_dict={},
                 condition_tags=[],
                 verbose=False,
                 on_timestamp=None,
                 on_open_conditions=None):
        self.mqtt_id = device_id
        self.jobs = jobs_dict
        self.condition_tags = condition_tags

        self.zdm_endpoint = endpoint
        self.mqttClient = MQTTClient(mqtt_id=device_id)

        self._on_timestamp = on_timestamp
        self._on_open_conditions = on_open_conditions

        self.data_topic = '/'.join(['j', 'data', device_id])
        self.up_topic = '/'.join(['j', 'up', device_id])
        self.dn_topic = '/'.join(['j', 'dn', device_id])
        if verbose:
            logger.setLevel(logging.DEBUG)


    def id(self):
        """
.. method:: id(pw)

        Return the device id.
        """
        return self.mqtt_id

    def connect(self):
        """
.. method:: connect()

        Connect your device to the ZDM. You must set device's password first. It also enable your device to receive incoming messages.
        """
        for _ in range(5):
            try:
                logger.info("ZDMClient.connect attempt")
                self.mqttClient.connect(host=self.zdm_endpoint, port=PORT)
                break
            except Exception as e:
                logger.error("ZDMClient.connect", e)
                pass
        time.sleep(2)
        if not self.mqttClient.connected:
            raise Exception("Failed to connect")

        self._subscribe_down()
        self.request_status()
        self._send_manifest()

    def set_password(self, pw):
        """
    .. method:: set_password(pw)

        Set the device password to :samp:`pw`. You can generate a password using the ZDM, creating a key for your device
        """
        self.mqttClient.set_username_pw(self.mqtt_id, pw)

    # @Deprecated. Use the method publish()
    def publish_data(self, tag, payload):
        """
    .. method:: publish_data(tag, payload)

        Publish a message to the ZDM.

        * :samp:`tag`, is a label for the device's data into your workspace. More than one device can publish message to the same tag
        * :samp:`payload` is the message payload, represented by a dictionary
        """
        topic = self._build_ingestion_topic(tag)
        self.mqttClient.publish(topic, payload)
        logger.info("Message published correctly. Msg: {}, topic:{}".format(payload, topic))

    def publish(self, tag, payload):
        """
    .. method:: publish(tag, payload)

        Publish a message to the ZDM.

        * :samp:`tag`, is a label for the device's data into your workspace. More than one device can publish message to the same tag
        * :samp:`payload` is the message payload, represented by a dictionary
        """
        topic = self._build_ingestion_topic(tag)
        self.mqttClient.publish(topic, payload)

    # # @Deprecated.  Use the get_condition() and open() and close() method
    # def send_event(self, value):
    #     """
    # .. method:: send_event(tag, value)
    #
    #    Publish an event to the ZDM.
    #
    #    * :samp:`value`, the value of the event as dictionary.
    #    """
    #     self._send_up_msg('', 'event', value)

    def request_status(self):
        self._send_up_msg(MQTT_PREFIX_REQ_DEV, "status")
        logger.debug("Status requested")

    def request_timestamp(self):
        self._send_up_msg(MQTT_PREFIX_REQ_DEV, "now")
        logger.debug("Timestamps requested")

    def request_open_conditions(self):
        """
    .. method:: request_open_conditions()

    Request all the open conditions of the device not yet closed.
    """
        self._send_up_msg(MQTT_PREFIX_REQ_DEV, "conditions")

    def new_condition(self, condition_tag):
        """
    .. method:: new_condition()

    Create and return a new condition.
         * :samp:`condition_tag`, the tag of the new condition.
    """
        if condition_tag in self.condition_tags:
            return Condition(self, condition_tag)
        else:
            raise Exception(
                "Condition tag '{}' not found. Please initialize condition tag in the constructor.".format(
                    condition_tag))

    def _handle_dn_msg(self, client, data, msg):
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
            logger.debug("ZdmClient._handle_dn_msg receive message: {}".format(payload))
            if "key" not in payload:
                raise Exception(
                    "The key is not present into the message {}".format(payload))
            if "value" not in payload:
                raise Exception(
                    "The value is not present into the message {}".format(payload))

            method = payload["key"]
            value = payload["value"]

            if method.startswith(MQTT_PREFIX_JOB):
                delta_method = method[1:]
                self._handle_job_request(delta_method, args)
            elif method.startswith(MQTT_PREFIX_REQ_DEV):
                delta_method = method[1:]
                self._handle_delta_request(delta_method, value)
            else:
                print("zlib_zdm.Device.handle_dn_msg received custom key")
                # TODO: mange the custom key, with callback ??
        except Exception as e:
            logger.error("Error", e)

    def _handle_job_request(self, job, args):
        if "args" in args:
            args = args["args"]
        else:
           logger.warning("ZdmClient.handle_dn_msg args key not present.")

        if job == 'fota':
            logger.error("FOTA is not supported on ZdmClient")
            self._reply_job(job, {"error": "FOTA is not supported in the zdm client py."})
        elif job == 'reset':
            logger.error("Reset is not supported on ZdmClient")
            self._reply_job(job, {"error": "Reset is not supported in the zdm client py."})
        elif job in self.jobs:
            try:
                res = self.jobs[job](self, args)
                logger.info("[{}] job {} executed with result res: {}".format(self.mqtt_id, job, res))
                self._reply_job(job, res)
            except Exception as e:
                print("zlib_zdm.Device.handle_job_request", e)
                res = 'exception'
                self._reply_job(job, {"error": str(e)})
        else:
            print("zlib_zdm.Device.handle_job_request invalid job request")
            self._reply_job(job, {"error": "Job {} not supported".format(job)})

    def _handle_delta_request(self, delta_key, args):
        if delta_key == 'status':
            self._handle_delta_status(args)
        elif delta_key == 'now':
            self._handle_delta_timestamp(args)
        elif delta_key == 'conditions':
            self._handle_delta_conditions(args)
        else:
            print("zlib_zdm.Device.handle_delta_request received user-defined delta")
            # TODO pass custom delta_key and arg to user callback?

    def _handle_delta_timestamp(self, arg):
        if self._on_timestamp is None:
            logger.error("to ask timestamp, you must initialize a time_callback first")
            raise Exception("No timestamp callback initialized")
        else:
            self._on_timestamp(self, arg)

    def _handle_delta_status(self, arg):
        logger.debug("Received a delta status. Msg:{}".format(arg))

        if ('expected' in arg) and (arg['expected'] is not None):
            if MQTT_KEY_FOTA in arg['expected']:
                logger.warning("FOTA is not supported on ZdmClient")
            else:
                # handle other keys
                for expected_key in arg['expected']:
                    value = arg['expected'][expected_key]['v']

                    if expected_key.startswith(MQTT_PREFIX_JOB):
                        delta_method = expected_key[1:]
                        self._handle_job_request(delta_method, value)
                    else:
                        logger.warning(
                            "ZdmClient._handle_delta_status expected key '{}' not recognized ".format(expected_key))
                        # TODO: what to do if the expected key if not a job ? whey the zdm lib save it into the expected ?
                        # self.expected.update({expected_key: value})

        # TODO check if ('current' in arg) and (arg['current'] is not None):  where the current status contains something to do...

    def _handle_delta_conditions(self, open_conditions):
        op_conditions = []
        # {'1593073070356.4473': {'tag': 'epspplzzjz', 'start': '2020-06-25T08:17:50Z'},
        for uuid, value in open_conditions.items():
            if "tag" in value:
                c = Condition(self, value['tag'])
                c.uuid = uuid
                if 'start' in value:
                    c.start = value['start']
                else:
                    logger.warning("Start time not set in condition {}".format(uuid))
                op_conditions.append(c)
            else:
                raise Exception("Bad open condition received. No tag present")
        if self._on_open_conditions is None:
            raise Exception("Open Conditions callback is not defined.")
        else:
            self._on_open_conditions(self, op_conditions)

    def _reply_job(self, key, value):
        self._send_up_msg(MQTT_PREFIX_JOB, key, value)

    def _subscribe_down(self):
        logger.debug("ZdmClient._subscribe_down subscribed to topic: {}".format(self.dn_topic))
        self.mqttClient.subscribe(self.dn_topic, callback=self._handle_dn_msg)

    def _send_manifest(self):
        value = {
            'jobs': [k for k in self.jobs],
            'conditions': self.condition_tags
        }
        value = [k for k in self.jobs]

        self._send_up_msg(MQTT_PREFIX_STRONG_PRIVATE_STATUS, "manifest", value)

    def _send_up_msg(self, prefix, key, value={}):
        msg = {
            'key': prefix + key,
            'value': value
        }
        logger.info(msg)
        self.mqttClient.publish(self.up_topic, msg)

    # @deprecated method. Use the send_up_msg
    def _publish_up(self, payload):
        topic = self.up_topic
        self.mqttClient.publish(topic, payload)
        logger.debug("Msg published on UP topic correctly. Msg: {}, topic:{}".format(payload, topic))

    def _build_ingestion_topic(self, tag):
        # build the topic for the ingestion topic
        # ex.  data/<deviceid>/<TAG>/
        return '/'.join([self.data_topic, tag])

class Condition:
    def __init__(self, client, tag):
        self.uuid = self._gen_uuid()
        self.tag = tag
        self.client = client

        self.start = None
        self.finish = None

    def get_id(self):
        return str(self.uuid)

    def get_tag(self):
        return self.tag

    def get_start(self):
        return str(self.start)

    def get_finish(self):
        return str(self.finish)

    def open(self, payload=None, start=None):
        if start is None:
            d = datetime.datetime.utcnow()
            self.start = d.isoformat("T") + "Z"
        else:
            self.start = start
        value = {
            'uuid': self.get_id(),
            'tag': self.get_tag(),
            'payload': payload,
            'start': self.get_start(),
        }

        self.client._send_up_msg('', 'condition', value)

    def close(self, payload=None, finish=None):
        if finish is None:
            d = datetime.datetime.utcnow()
            self.finish = d.isoformat("T") + "Z"
        else:
            self.finish = finish
        value = {
            'uuid': self.get_id(),
            'payload': payload,
            'finish': self.get_finish()
        }
        self.client._send_up_msg('', 'condition', value)

    def reset(self):
        self.uuid = self._gen_uuid()
        self.start = None
        self.finish = None

    def _gen_uuid(self):
        return str(time.time() * 1000.0)

    def __str__(self):
        return "Condition (id={}, tag={}, start={}, finish={})".format(self.uuid, self.tag, self.start, self.finish)
