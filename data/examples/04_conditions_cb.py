"""
conditions.py

The example show how to use conditions for monitoring the level of a battery.
It create a new condition with the tag "battery" and it open it when the battery is low,
and close it when the battery is high.
In order to reopen the same condition on the same tag, the reset method is used.

"""
import time

from zdm import ZDMClient

device_id = '*** PUT YOU DEVICE ID HERE ***'
password = '*** PUT YOUR PASSWORD HERE ***'

device_id = 'dev-51blblqx01jh'
password = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOjEsImV4cCI6MTYyNDYxMTI5MywiaWF0IjoxNTkzMDc1MjkzLCJzdWIiOiJkZXYtNTFibGJscXgwMWpoIn0.wVRsQ1-ieSmaN0BY4IqqJu9F3Wtrb-tUX_ubu2r3K3Q'

condition_tag = "battery"

# this function is called when the list of open conditions are received.
def on_open_conditions(zclient, conditions):
    for c in conditions:
        print("Open condition: {}".format(c))

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
