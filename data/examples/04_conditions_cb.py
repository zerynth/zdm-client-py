"""
conditions.py

The example shows how to request the open conditions (the conditions that are not closed) to the ZDM.

"""
import time

from zdm import ZDMClient

device_id = '*** PUT YOU DEVICE ID HERE ***'
password = '*** PUT YOUR PASSWORD HERE ***'

condition_tag = "battery"

# this function is called when the list of open conditions are received.
def on_open_conditions(zclient, conditions):
    for c in conditions:
        print("### closing the condition: {}".format(c))
        c.close()

device = ZDMClient(device_id=device_id, condition_tags=[condition_tag], on_open_conditions=on_open_conditions, endpoint="mqtt.zdm.test.zerynth.com")
device.set_password(password)
device.connect()


condition = device.new_condition(condition_tag)
# open the condition with a payload
condition.open(payload={"low_battery": True})
#
# do other stuff
#
time.sleep(2)
# the device requests the open conditions
device.request_open_conditions()

while True:
    time.sleep(5)
