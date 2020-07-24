"""
basic.py

Show the basic example of a ZdmClient that sends a stream of messages to the ZDM.
Each message is published into a random tag with a random value.

"""
import zdm
import os
from zdm.device.zdmclient import ZDMClient
import time
import inspect
import os


device = ZDMClient()

device.connect()

while True:
    print("waiting for jobs...")
    device.publish({"Hello":"world"}, "tag")
    time.sleep(3)

time.sleep


