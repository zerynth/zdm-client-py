################################################################################
# Zerynth Device Manager
#
# Created by Zerynth Team 2020 CC
# Authors: E.Neri, D.Neri
###############################################################################
"""
timestamp.py

Show a simple example of how to received the timestamp from the ZDM.

"""
import time

import zdm

def time_callback(zdmclient, arg):
    print("Timestamp received: {}".format(arg))

device = zdm.ZDMClient( on_timestamp=time_callback)
device.connect()


while True:
    # Request the timestamp
    device.request_timestamp()
    print("Time requested ...")
    time.sleep(2)
