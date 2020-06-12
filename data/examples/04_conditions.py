"""
conditions.py

Show a simple example of how to send conditions to the ZDM.

"""
import time
import string
import random
import datetime

from zdm import ZDMClient

device_id = 'device-id'
password = 'device jwt'

device = ZDMClient(device_id=device_id, endpoint="mqtt.zdm.stage.zerynth.com")
device.set_password(password)
device.connect()

while True:
    uuid = ''.join(random.choices(string.ascii_uppercase +
                                        string.digits, k=5))
    tag = 'test-condition_'+uuid
    d = datetime.datetime.utcnow()
    start = d.isoformat("T") + "Z"
    payload = {
        'message': 'this is a test condition'
    }

    # opening the condition
    device.open_condition(uuid, tag, start, payload)
    time.sleep(15)

    # closing the condition
    d = datetime.datetime.utcnow()
    finish = d.isoformat("T") + "Z"
    device.close_condition(uuid, finish)
