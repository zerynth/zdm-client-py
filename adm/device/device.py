from .mqtt import MQTTClient
import json

class Device():

    def __init__(self, uuid, rpc=None):
        self.uuid = uuid
        self.rpc = rpc
        self.mqqt = MQTTClient()
        self.topic_data = "data/"
        self.topic_up = "j/up/"
        self.topic_down = "j/dn/#" # j/dn


    @property
    def id(self):
        return self.id
        
    def publish_data(self, payload):
        topic = self.topic_data + self.uuid
        self.mqqt.publish(topic, payload)
    
    def publish_up(self, payload):
        topic = self.topic_up + self.uuid
        self.mqqt.publish(topic, payload)


    def subscribe_down(self):
        print("subscribed to down : {}".format(self.topic_down))
        self.mqqt.subscribe(self.topic_down, qos=1)
        self.mqqt.mqttc.message_callback_add(self.topic_down, self._on_message_down_queuue)

    def _on_message_down_queuue(self, client, userdata, msg):
        payload = json.loads(msg.payload)
        print("received from topic: {} msg: {}".format(msg.topic, str(payload)))
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