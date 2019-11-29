from .mqtt import MQTTClient

class Device():

    def __init__(self, uuid):
        self.uuid = uuid
        self.mqqt = MQTTClient()
        self.topic_data = "data/"
        
    @property
    def id(self):
        return self.id
        
    def publish_data(self, payload):
        topic = self.topic_data + self.uuid
        self.mqqt.publish(topic, payload)