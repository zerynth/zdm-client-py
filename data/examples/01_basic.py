"""
basic.py

Show the basic example of a ZdmClient that sends a stream of messages to the ZDM.
Each message is published into a random tag with a random temperature value.

"""
import random
import time

import zdm

device_id = '*** PUT YOU DEVICE ID HERE ***'
password = '*** PUT YOUR PASSWORD HERE ***'

device_id = "dev-4si5ird6tslp"
password = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZXYtNHNpNWlyZDZ0c2xwIiwidXNlciI6ImRldi00c2k1aXJkNnRzbHAiLCJrZXkiOjEsImV4cCI6MjUxNjIzOTAyMn0.MDVPyMlqTVwniLX-N-fnm4G_fBT7Zjed929fIGcy9UQ"

device = zdm.ZDMClient(device_id=device_id)
device.set_password(password)
device.connect()

tags = ["bathroom", "bedroom", "living room"]

while True:
    time.sleep(2)
    temp = random.randint(10, 30)  # random temperature
    tag = random.choice(tags)  # random choice of the tag
    payload = {"temp": temp}
    device.publish_data(tag, payload)
