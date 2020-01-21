from   paho.mqtt.client import Client as  PahoClient
import  json 

from ..logging import MyLogger

logger = MyLogger().get_logger()

class MyMqttClient(PahoClient):

    def __init__(self, hostname="localhost", port=1883, user="admin", password="Z3rynthT3st"):
        super().__init__()

        # must be called before connect()
        super().username_pw_set(username=user, password=password)
        super().
       
        self.hostname =  hostname
        self.port = port

        # super(MyMqttClient, self).on_connect = self.on_connect
        # super().on_message = self.on_message
        
    # @PahoClient.on_connect.setter
    # def on_connect(self, new_importance):
    #     # You can change the order of these two lines:
    #     assert new_importance >= 3
    #     Node.importance.fset(self, new_importance)

    def connect(self):
        super().connect(self.hostname, self.port, 60)
        # logger.info("Connected succesfully to MQTT boker.".format(self.hostname, self.port))



    # def publish(self, topic, payload=None):
    #     print("publishing {} into {}".format(payload,  topic))
    #     if type(payload) is dict:
    #         print("DICTIONARY")
    #         payload = json.dumps(payload)
    #     self.mqttc.publish(topic, payload)

    # # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        # print("Connected with result code "+str(rc))
        logger.info("Connected succesfully to MQTT boker.".format(self.hostname, self.port))



    # The callback for when a PUBLISH message is received from the server.
    # def on_message(self, client, userdata, msg):
    #     print(msg.topic+" "+str(msg.payload))

    # def subscribe(self, topic, qos=0):
    #     self.mqttc.subscribe(topic, qos)

    # def loop(self):
    #     self.mqttc.loop_forever()
