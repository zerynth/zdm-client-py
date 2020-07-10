"""
basic.py

Show the basic example of a ZdmClient that sends a stream of messages to the ZDM.
Each message is published into a random tag with a random temperature value.

"""
import time
import zdm

device_id = 'device_id'
password = 'device password'

def set_temp(zdmclient, args):
    # zdmclient: is the object of the ZdmClient.
    # args     : is a json with the arguments  of the function.
    print("Executing job set_temp. Received args: {}".format(args))
    # DO SOMETHING
    # return: a json with the result of the job.
    return {"msg": "Temperature set correctly."}
jobs = {
    "aaaaa": set_temp
}
device = zdm.ZDMClient(device_id=device_id, jobs_dict=jobs, endpoint="rmq.localhost")
device.set_password(password)
device.connect()

i = 0
tag = "test"
while True:
    time.sleep(5)
    print(i)
    p = {"num": i}
    device.publish(tag, p)
    i = i + 1
