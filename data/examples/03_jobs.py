################################################################################
# Zerynth Device Manager
#
# Created by Zerynth Team 2020 CC
# Authors: E.Neri, D.Neri
###############################################################################

"""
jobs.py

A basic example showing ZDM Jobs and how to handle them.
Write your own jobs, then add them in the jobs dictionary with a custom key.

Once your device is connected to the ZDM, you can send it job commands using the key you defined and your device
will execute functions remotely.
"""

import time
import random
import zdm


# This job generates and returns a random number
def job_random(zdmclient, arg):
    print("Executing Job random ...")
    return {
        'rnd': random.randint(0, 100),
    }


# This job adds two numbers (num1, num2) and return the result.
def job_adder(zdmclient, arg):
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

# create a ZDM Device instance and pass to it the the jobs dictionary
device = zdm.ZDMClient(jobs_dict=my_jobs)
device.connect()

while True:
    print("waiting for jobs...")
    time.sleep(3)
