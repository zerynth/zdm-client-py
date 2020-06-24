"""
conditions.py

Show a simple example of how to send conditions to the ZDM.

"""
import time

from zdm import ZDMClient

device_id = '*** PUT YOU DEVICE ID HERE ***'
password = '*** PUT YOUR PASSWORD HERE ***'

condition_tag = "tag1"

device = ZDMClient(device_id=device_id, conditions=[condition_tag])

device.set_password(password)
device.connect()

while True:
    condition = device.get_condition(condition_tag)
    condition.open(payload={"door": "1"})
    # simulate a time that the dor is open
    time.sleep(15)
    condition.close()
    condition.reset()
