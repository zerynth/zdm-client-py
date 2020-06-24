"""
timestamp.py

Show a simple example of how to received the timestamp from the ZDM.

"""
import time

from zdm import ZDMClient

device_id = '*** PUT YOU DEVICE ID HERE ***'
password = '*** PUT YOUR PASSWORD HERE ***'

isTimeReceived = False

def time_callback(zdmclient, arg):
    global isTimeReceived
    isTimeReceived = True
    print("Timestamp received: {}".format(arg))

device = ZDMClient(device_id=device_id, time_callback=time_callback, endpoint="mqtt.zdm.test.zerynth.com")

device.set_password(password)
device.connect()


device.request_timestamp()

while not isTimeReceived:
    time.sleep(1)
    print("Waiting time...")
