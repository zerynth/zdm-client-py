"""
conditions.py

Show a simple example of how to send conditions to the ZDM.

"""
import time
import string
import random
import datetime

from zdm import ZDMClient

device_id = '*** PUT YOU DEVICE ID HERE ***'
password = '*** PUT YOUR PASSWORD HERE ***'

device = ZDMClient(device_id=device_id)
device.set_password(password)
device.connect()

while True:
    uuid = ''.join(random.choices(string.ascii_uppercase +
                                        string.digits, k=5))
    tag = 'test-condition_'+uuid
    d = datetime.datetime.utcnow()# <-- get time in UTC
    start = d.isoformat("T") + "Z"
    payload = {
        'message': 'this is a test condition'
    }

    # opening the condition
    device.send_condition(uuid, tag, start, None, payload)
    time.sleep(5)

    # closing the condition
    d = datetime.datetime.utcnow()# <-- get time in UTC
    finish = d.isoformat("T") + "Z"
    device.send_condition(uuid, tag, start, finish, payload)
    time.sleep(5)
