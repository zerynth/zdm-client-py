# from .mqtt import MQTTClient
from .mqtt import MQTTClient
import json

from ..logging import MyLogger

logger = MyLogger().get_logger()

class Device():

    def __init__(self, uuid, hostname="localhost", port=1883, user="admin", password="Z3rynthT3st",  rpc=None):
        self.uuid = uuid
        self.rpc = rpc
        self.mqqt = MQTTClient(hostname, port, user, password)
        logger.info("[{}] mqqt client: {}:{}".format(self.id, hostname, port))
     
        # self.mqqt = MyMqttClient()
        self.topic_data = "data/"
        self.topic_up = "j/up/"
        self.topic_down = "j/dn/#" # j/dn


    @property
    def id(self):
        return self.uuid
    
    def start(self):
        self.mqqt.mqttc.loop_forever()

    def publish_data(self, payload):
        topic = self.topic_data + self.uuid
        self.mqqt.publish(topic, payload)
    
    def publish_up(self, payload):
        topic = self.topic_up + self.uuid
        self.mqqt.publish(topic, payload)

    def connect(self):
        self.mqqt.connect()
        self.subscribe_down() # subscribe to the down quue
       

    def subscribe_down(self):
        logger.info("[{}] subscribed to topic: {}".format(self.id, self.topic_down))

        self.mqqt.subscribe(self.topic_down, qos=1)
        self.mqqt.mqttc.message_callback_add(self.topic_down, self._on_message_down_queuue)

    def _on_message_down_queuue(self, client, userdata, msg):
        payload = json.loads(msg.payload)
        logger.info("[{}] recevied from topic: {}, msg: {}".format(self.id, msg.topic,  str(payload)))

        try:
            result = self.rpc[payload['method']](self, payload["args"])
            print("rpc: {}, res:{} ".format(payload['method'],str(result)))
            rpc_response = {
                        "rpc": payload["rpc"],
                        "method": payload["method"],
                        "args": payload["args"],
                        "status": "done",
                        "result": result
                    }
            self.publish_up(json.dumps(rpc_response))

        except Exception as e:
            res = e
            status = "error"
            print("ERROR", e)