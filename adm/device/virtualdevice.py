import json

from .mqtt import MQTTClient
from ..logging import MyLogger
import time

logger = MyLogger().get_logger()


class VirtualDevice:
    def __init__(self, mqtt_id, job=None):
        self.mqtt_id = mqtt_id
        self.jobs = job
        self.mqttClient = MQTTClient(mqtt_id=mqtt_id)

        self.data_topic = '/'.join(['j', 'data', mqtt_id])
        self.up_topic = '/'.join(['j', 'up', mqtt_id])
        self.dn_topic = '/'.join(['j', 'dn', mqtt_id])

    def connect(self):
        for _ in range(5):
            try:
                print("VirtualDevice.connect attempt")
                self.mqttClient.connect(host='rmq.zdm.stage.zerynth.com')
                break
            except Exception as e:
                print("VirtualDevice.connect", e)
                pass
        time.sleep(2)
        if not self.mqttClient.connected:
            raise Exception("Failed to connect")

        self.subscribe_down()
        self.request_status()

    def subscribe_down(self):
        self.mqttClient.subscribe(self.dn_topic, callback=self.handle_dn_msg)

    def request_status(self):
        msg = {
            'key': '#status',
            'value': {}
        }
        self.publish_up(msg)
        logger.info("Status requested")

    def id(self):
        return self.mqtt_id

    def send_manifest(self):
        payload = {
            'key': '__manifest',
            'value': [k for k in self.jobs]
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

    def handle_delta_status(self, arg):
        print("zlib_zdm.Device.handle_delta_status received status delta")

        if ('expected' in arg) and (arg['expected'] is not None):
            if '@fota' in arg['expected']:
               print("fota not supported")

            else:
                # handle other keys
                for expected_key in arg['expected']:
                    value = arg['expected'][expected_key]['v']

                    if expected_key[0] == '@':
                        if expected_key[1:] in self.jobs:
                            try:
                                res = self.jobs[expected_key[1:]](self, arg)
                                logger.info("job {} executed. Result: {}".format(expected_key[1:], res))
                                job_response = {
                                    "key": expected_key,
                                    "value": {"status": "done", "result": res}
                                }
                                self.publish_up(json.dumps(job_response))
                            except Exception as e:
                                print("zlib_zdm.Device.handle_job_request", e)
                                res = 'exception'

            self.send_manifest()

    def handle_dn_msg(self, client, data, msg):
        payload = json.loads(msg.payload)
        try:
            if "key" not in payload:
                raise Exception(
                    "The key  is not present into the job payload {}".format(payload))
            if "value" not in payload:
                raise Exception(
                    "The value  is not present into the job payload {}".format(payload))

            method = payload["key"]
            value = payload["value"]
            if "args" in value:
                args = value["args"]
            else:
                args = ""

            if method.startswith('@'):
                method = method[1:]
                if method in self.jobs:
                    result = self.jobs[method](self, args)
                    logger.info("[{}] job {} executed with result res:{} ".format(
                        self.id, method, result))

                    job_response = {
                        "key": "@" + method,
                        "value": {"status": "done", "result": result}
                    }

                    self.publish_up(json.dumps(job_response))

            elif method.startswith('#'):
                self.handle_delta_status(payload['value'])

            else:
                logger.info("[{}] job {} not supported ".format(
                    self.id, method))

                job_response = {
                    "key": "@" + method,
                    "value": {"status": "failed", "message": "method not supported"}
                }

                self.publish_up(json.dumps(job_response))

        except Exception as e:
            logger.error("Error", e)

    def build_ingestion_topic(self, tag):
        """ build the topic for the ingestion
        ex.  data/<deviceid>/<TAG>/

        """
        return '/'.join([self.data_topic, tag])

    def start_loop(self):
        self.mqttClient.loop()
