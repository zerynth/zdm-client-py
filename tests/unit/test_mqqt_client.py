
from unittest import TestCase
from adm.device.mymqtt import MyMqttClient


import unittest


class TestADMMqttClient(TestCase):

      def test_create_client(self):
        hostname="rmq.zerinth.com"
        port=1883 
        user="mqtt"
        password="mqtt"

        c = MyMqttClient(hostname, port, user, password)
        c.connect()
        c.publish("data/test", "prova")
        c.loop_forever()
        # self.assertIsInstance(MQTTClient, c)