"""
jobs.py

Show a simple example of how to define a custom job and pass it to the ZdmClient.

"""
import time
import random
import zdm

device_id = 'Your-device-id'
password = 'Device-Password'


# This job generates and returns a random number
def job_random(device, arg):
    print("Executing Job random ...")
    return {
        'rnd': random.randint(0, 100),
    }


# This job adds two numbers (num1, num2) and return the result.
def job_adder(device, arg):
    print("Executing Job adder ...")
    if "num1" in arg and "num2" in arg:
        res = arg['num1'] + arg["num2"]
        return {"res": res}
    else:
        return {"err": "Bad arguments. Arguments 'num1' and 'num2' must be provided."}


# define the list of jobs exposed by the device.
# A job is a function that receives two parameters (the device instance itself, and the arguments in a dictionary)
# and returns the result as a dictionary.
my_jobs = {
    'jobRandom': job_random,
    'jobAdder': job_adder,
}

device = zdm.ZDMClient(device_id=device_id, jobs_dict=my_jobs)
device.set_password(password)
device.connect()

while True:
    print("waiting for jobs...")
    time.sleep(3)
