from adm import Device
import time
import json 
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
    return json.dumps({"msg":"led setted correctly to"})
    
# define the list of custom RPC offered by the device
custom_rpc = {
    "set_led": rpc_set_led
}


device = Device("dev01", hostname="rmq.zerinth.com", port=1883, user="mqtt", password="mqtt", rpc=custom_rpc)
device.connect()

device.mqqt.loop()


