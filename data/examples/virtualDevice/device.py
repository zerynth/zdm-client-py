import json
import random
import time
from adm import VirtualDevice


# Job function for on/off a led
def set_led(obj, args):
    print("Received led on job with args: {}".format(args))
    if "led" in args:
        # do something to the values (on or off the led)
        print("Set the led status to: {}".format(args['led']))
    return json.dumps({"msg": "led set correctly"})


# define the list of custom Jobs offered by the device
custom_jobs = {
    "set_led": set_led,
}

device_id = 'dev-4rq2qzng6p09'
password = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiZGV2LTRycTJxem5nNnAwOSIsInN1YiI6ImRldi00cnEycXpuZzZwMDkiLCJrZXkiOjEsImV4cCI6MTU4NzYzNjU5Mn0.lkpvNxPS_KavA4voDpxcxfPDqdDGCgdKl8rp3pjypx0'

device = VirtualDevice(mqtt_id=device_id, job=custom_jobs)
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


