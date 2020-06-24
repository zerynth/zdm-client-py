"""
conditions.py

Show a simple example of how to send conditions to the ZDM.

"""
import time

from zdm import ZDMClient

device_id = '*** PUT YOU DEVICE ID HERE ***'
password = '*** PUT YOUR PASSWORD HERE ***'

device_id = 'dev-517wh76vepm8'
password = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOjEsImV4cCI6MTYyNDUyNTU3OCwiaWF0IjoxNTkyOTg5NTc4LCJzdWIiOiJkZXYtNTE3d2g3NnZlcG04In0.My5bpI1b6U_1Le7n7ciLY6T4KZAqkfmWY4kJfFGUf_8'

conditions = ['open-door']

device = ZDMClient(device_id=device_id, conditions=conditions, endpoint="mqtt.zdm.test.zerynth.com")

device.set_password(password)
device.connect()

while True:
    condition = device.get_condition('open-door')
    condition.open(payload={"door": "1"})
    # simulate a time that the dor is open
    time.sleep(15)
    condition.close()
    condition.reset()
