from adm.device import Device
import time
import json 


# #  {"rpc":1, "method":"get_temp", "args":null, "status": "pendind"}

# # RPC to read opto iso channels
def rpc_get_temp(obj, context):
    print("RPC GET TEMP CALLED")
    print(json.dumps(context))
    print("END RPC GET")
    return json.dumps({"temp":45})

# {"rpc":1, "method":"set_led", "args":{"value":23}, "status": "pendind"}
# RPC to read opto iso channels
def rpc_set_led(obj, context):
    print("SET LED {}".format(json.dumps(context)))
    return json.dumps({"led":context["value"]})
    

# RPC custom dict
custom_rpc = {
    "get_temp": rpc_get_temp,
    "set_led": rpc_set_led
}


device = Device("dev01", hostname="rmq.zerinth.com", port=1883, user="mqtt", password="mqtt", rpc=custom_rpc)
device.connect()

# Publish message into the topic "data/<devid>"
for x in range (2000):
    time.sleep(2)
    payload = {"temp": 34, "msg": x}
    device.publish_data(payload)

device.mqqt.loop()


# import adm

# device = adm.Device(uuid="dev01", hostname="rmq.zerinth.com", port=1883, user="mqtt", password="mqtt", )
# device.connect()
# payload = {"temp": 34}
# device.publish_data(payload)

# for x in range (2000):

#     payload = {"temp": x}
#     print("[{}] sent:  {}".format(x, payload))
#     device.publish_data(payload)
#     time.sleep(2)


# import adm

# device = adm.Device(uuid="dev01", hostname="rmq.zerinth.com", port=1883, user="mqtt", password="mqtt")
# device.connect()
# payload = {"temp": 34}
# device.publish_data(payload)

# time.sleep(2)
# device.start()
