"""
conditions.py

Show a simple example of how to send conditions to the ZDM.

"""
import time

from zdm import ZDMClient

device_id = '*** PUT YOU DEVICE ID HERE ***'
password = '*** PUT YOUR PASSWORD HERE ***'

device_id = 'dev-51blblqx01jh'
password = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOjEsImV4cCI6MTYyNDYxMTI5MywiaWF0IjoxNTkzMDc1MjkzLCJzdWIiOiJkZXYtNTFibGJscXgwMWpoIn0.wVRsQ1-ieSmaN0BY4IqqJu9F3Wtrb-tUX_ubu2r3K3Q'

condition_tag = "tag1"

# this function is called when the list of open conditions are received.
def on_open_conditions(zclient, conditions):
    for c in conditions:
        print("Open condition: {}".format(c))
        c.close()


device = ZDMClient(device_id=device_id, conditions=[condition_tag], open_conditions_cb=on_open_conditions, endpoint="mqtt.zdm.test.zerynth.com")
device.set_password(password)
device.connect()

condition = device.get_condition(condition_tag)
condition.open(payload={"door": "1"})
# do other stuff
time.sleep(2)
# the device requests the open conditions
device.request_open_conditions()

while True:
    time.sleep(5)
