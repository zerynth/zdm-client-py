"""
basic.py

Show the basic example of a ZdmClient that sends a stream of messages to the ZDM.
Each message is published into a random tag with a random temperature value.

"""
import random
import time
import zdm


device_id = 'Here your device Id'
password = 'Here your device password'


device = zdm.ZDMClient(device_id=device_id, endpoint="rmq.zdm.zerynth.com")
device.set_password(password)
device.connect()

time.sleep(5)

tags = ["bathroom", "bedroom", "living room"]

while True:
    time.sleep(5)
    temp = random.randint(10, 30)  # random temperature
    tag = random.choice(tags)      # random choice of the tag
    payload = {"temp": temp}
    device.publish_data(tag, payload)
