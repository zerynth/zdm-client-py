"""
conditions.py

Show a simple example of how to send conditions to the ZDM.

"""
import time
import string
import random
import datetime

from zdm import ZDMClient


device_id = 'dev-5012tktze9sd'
password = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZXYtNTAxMnRrdHplOXNkIiwidXNlciI6ImRldi01MDEydGt0emU5c2QiLCJrZXkiOjEsImV4cCI6MjUxNjIzOTAyMn0.YJNoFwP2PXkDQbddAuEM9Mp09kuUlFg50CuHOUGFtAU'

device = ZDMClient(device_id=device_id, endpoint="mqtt.zdm.stage.zerynth.com")
device.set_password(password)
device.connect()

while True:
    condition = device.create_condition('test-tag', {})
    condition.open()
    time.sleep(15)
    condition.close()

