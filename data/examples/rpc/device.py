import json

from adm import VirtualDevice

"""
Emulate a Device that receives an RPC from the ADM.

The RPC is a function for  setting the led to 'on' or 'off'
"""


# RPC function for on/off a led 
def rpc_set_led(obj, args):
    print("Recevied set_led RPC with args: {}".format(args))
    if "led" in args:
        # do something to the values (on or off the led)
        print("Setted teh led status to: {}".format(args['led']))
    return json.dumps({"msg": "led setted correctly to"})


def _get_rpc():
    print("received manaifest")


# define the list of custom RPC offered by the device
custom_rpc = {
    "set_led": rpc_set_led,
    "manifest": _get_rpc
}

DEVICE_ID = "dev-4pc2ycnlob9h"
DEVICE_PASSWORD = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZXYtNHBjMnljbmxvYjloIiwidXNlciI6ImRldi00cGMyeWNubG9iOWgiLCJrZXkiOjEsImV4cCI6MjUxNjIzOTAyMn0.9UgGhvG4O7rbl9QA9VDB8W6mOA8s_dlfpleUtadlvpY"

device = VirtualDevice(DEVICE_ID, username=DEVICE_ID, password=DEVICE_PASSWORD, hostname="rmq.localhost", port=1883,
                       rpc=custom_rpc)

device.connect()
