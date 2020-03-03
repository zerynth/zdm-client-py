from adm import VirtualDevice
import time
import json
import jwt
"""
Emulate a VirtualDevice that receives an FOTA

"""


# RPC function for on/off a led 
def rpc_set_led(obj, args):
    print("Recevied set_led RPC with args: {}".format(args))
    if "led" in args:
        # do something to the values (on or off the led)
        print("Setted teh led status to: {}".format(args['led']))
    return json.dumps({"msg":"led setted correctly to"})
    
# define the list of custom RPC offered by the device
custom_rpc = {
    "set_led": rpc_set_led
}

DEV_ID =
EXP =
KEY_ID =
KEY =
jwt = jwt.encode({'sub': DEV_ID, 'user':DEV_ID, 'exp': exp, 'key': KEY_ID}, KEY, algorithm='HS256')

device = VirtualDevice("dev01", hostname="rmq.localhost", port=1883, rpc=custom_rpc)
device.connect()
device.mqqt.loop()


