from adm.device import Device
import time
import json 


# RPC to read opto iso channels
def rpc_get_temp(obj, *args):
    print("RPC GET TEMP CALLED")
    return json.dumps({"temp":45})
    


# RPC custom dict
custom_rpc = {
    "get_temp": rpc_get_temp
}


device = Device("dev01", rpc=custom_rpc)
device.mqqt.connect()


device.subscribe_down()


# for x in range (2000):
#     time.sleep(2)
#     device.publish_data("{} prova".format(x))


device.mqqt.loop()


