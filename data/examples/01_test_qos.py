"""
basic.py

Show the basic example of a ZdmClient that sends a stream of messages to the ZDM.
Each message is published into a random tag with a random temperature value.

"""
import time
import zdm

device_id = 'dev-5249aeicjqbo'
password = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZXYtNTI0OWFlaWNqcWJvIiwidXNlciI6ImRldi01MjQ5YWVpY2pxYm8iLCJrZXkiOjEsImV4cCI6MjUxNjIzOTAyMn0.-qnBC6EtYmoeMsALv_jcL0Szb9NjP0LFrHoDSU_mZ2A'

device_id = 'dev-524cnl894s1v'
password = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZXYtNTI0Y25sODk0czF2IiwidXNlciI6ImRldi01MjRjbmw4OTRzMXYiLCJrZXkiOjEsImV4cCI6MjUxNjIzOTAyMn0.JqJ5pQsM7atJtLeJel5EAo_I2nZOdkhrlo1V68OCMqg'

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
