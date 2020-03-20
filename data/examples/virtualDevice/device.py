import json
import random
import time
from adm import VirtualDevice


# RPC function for on/off a led
def set_led(obj, args):
    print("Received led on rpc with args: {}".format(args))
    if "led" in args:
        # do something to the values (on or off the led)
        print("Set the led status to: {}".format(args['led']))
    return json.dumps({"msg": "led set correctly"})


# define the list of custom RPC offered by the device
custom_rpc = {
    "set_led": set_led,
}

device_id = 'DeviceId'
password = 'DevicePassword'

device = VirtualDevice(mqtt_id=device_id, rpc=custom_rpc)
device.set_password(password)
device.connect()

time.sleep(5)
messages_num = 1   # number of messages to send
tags = ["caffe", "cibo", "bevande", "armadi",
        "case", "tutto"]  # tags where to publish
names = ["prova1", "prova2", "prova3", "prova4"]

while True:
    time.sleep(5)
    temp = random.randint(10, 30)  # temperature
    tag = random.choice(tags)
    name = random.choice(names)
    payload = {"temp": temp, "name": name}
    device.publish_data(tag, payload)


