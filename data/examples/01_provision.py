"""
basic.py

Show the basic example of a ZdmClient that sends a stream of messages to the ZDM.
Each message is published into a random tag with a random value.

"""
import zdm
import os
from zdm.device.zdmclient import ZDMClient
import time


zdevice_path = os.path.dirname(__file__)

print("MAIN PATH",  os.path.abspath('.'))
crd = zdm.load_zdevice(".")

device = ZDMClient(cred=crd)

device.connect()

while True:
    print("waiting for jobs...")
    device.publish({"Hello":"world"}, "tag")
    time.sleep(3)


