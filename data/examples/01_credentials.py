################################################################################
# Zerynth Device Manager
#
# Created by Zerynth Team 2020 CC
# Authors: E.Neri, D.Neri
###############################################################################


# In order to connect the ZDM client Python to the ZDM, follow the steps:
#   1) Open the ZDM GUI
#   2) Navigate into your workspace and select a device
#   3) Click into the "Security" button and select the appropriate Credentials type and Endpoint node.
#   4) Click "ok" and then "Download credentials".
#   5) The GUI generates the credential configuration file (zdevice.json) that contains the security parameter.
#   6) Save this script in folder of your choice.
#   6) Save the zdevice.json file into the same folder of your script.
#   7) Run with `python your-script.py'

import zdm
import time

device = zdm.ZDMClient()
device.connect()

while True:
    device.publish({"Hello": "world"}, "hello")
    time.sleep(3)


