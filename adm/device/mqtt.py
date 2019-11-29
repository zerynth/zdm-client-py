import paho.mqtt.client as mqtt
import json 

class MQTTClient(object):

    def __init__(self, hostname="localhost", port=1883, user="admin", password="Z3rynthT3st"):
        self.hostname =  hostname
        self.port = port
        self.mqttc = mqtt.Client()
        self.mqttc.username_pw_set(username=user, password=password)
        
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message
        
    
    def connect(self):
        print("connceting to {} {}".format(self.hostname, self.port))
        self.mqttc.connect(self.hostname, self.port, 60)


    def publish(self, topic, payload=None):
        print("publishing {} into {}".format(payload,  topic))
        # if isinstance(payload, dict):
        #     print("DICTIONARY")
        #     payload = json.dumps(payload)
        self.mqttc.publish(topic, payload)

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

    def loop(self):
        self.mqttc.loop_forever()