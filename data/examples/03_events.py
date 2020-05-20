"""
events.py

Show a simple example of how to send events to the ZDM.

"""
import time

from zdm import ZDMClient

device_id = '*** PUT YOU DEVICE ID HERE ***'
password = '*** PUT YOUR PASSWORD HERE ***'

device = ZDMClient(device_id=device_id)
device.set_password(password)
device.connect()

while True:
    device.send_event({"name": "low_battery", "value": "20%"})
    time.sleep(3)
