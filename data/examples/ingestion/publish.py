import adm
import random
import time

"""
Create a VirutalDevice that sends messages to the ingestion queue of the ADM.
"""

# use the deviceconf.py script to obtain a device id
DEVICE_ID = "dev-4m30sc96ycxv"


NUM_MESSAGES = 100    # number of messages to send
TAGS = ["caffe", "cibo", "bevande", "armadi",
        "case", "tutto"]  # tags where to publish
NAMES= ["prova1", "prova2", "prova3", "prova4"]


device = adm.Device(DEVICE_ID, secret=DEVICE_SECRET, authkey_id=DEVICE_AUTHKEY_ID, hostname="rmq.localhost",port=1883)

# print("JWT {}".format(device.encode_jwt(auth_keyid=DEVICE_AUTHKEY_ID, secret=DEVICE_SECRET,exp=DEVICE_AUTHKEY_EXPIRATION)))

device.connect()

for x in range(NUM_MESSAGES):
    time.sleep(2)
    temp = random.randint(-20, 40)  # temperature
    tag = random.choice(TAGS)
    name = random.choice(NAMES)
    payload = {"temp": temp, "name": name}
    device.publish_data(tag, payload)

device.mqqt.loop()