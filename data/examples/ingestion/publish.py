import adm
import random
import time

"""
Create a VirutalDevice that sends messages to the ingestion queue of the ADM.
"""

# use the deviceconf.py script to obtain a device id
DEVICE_ID = "dev-4pc2ycnlob9h"
DEVICE_PASSWORD ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZXYtNHBjMnljbmxvYjloIiwidXNlciI6ImRldi00cGMyeWNubG9iOWgiLCJrZXkiOjEsImV4cCI6MjUxNjIzOTAyMiwiaWF0IjoxNTE2MjM5MDIyfQ.aCggGs4pqaCkPlRFoPgl8MUPoXUDWQxl68JfxQFTWvA"

DEVICE_ID = "dev-4pc2ycnlob9h"
DEVICE_PASSWORD ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZXYtNHBjMnljbmxvYjloIiwidXNlciI6ImRldi00cGMyeWNubG9iOWgiLCJrZXkiOjEsImV4cCI6MjUxNjIzOTAyMn0.9UgGhvG4O7rbl9QA9VDB8W6mOA8s_dlfpleUtadlvpY"


NUM_MESSAGES = 100    # number of messages to send
TAGS = ["caffe", "cibo", "bevande", "armadi",
        "case", "tutto"]  # tags where to publish
NAMES = ["prova1", "prova2", "prova3", "prova4"]

device = adm.VirtualDevice(DEVICE_ID, username=DEVICE_ID, password=DEVICE_PASSWORD, hostname="rmq.adm.zerinth.com", port=1883)

device.connect()

for x in range(NUM_MESSAGES):
    time.sleep(2)
    temp = random.randint(-20, 40)  # temperature
    tag = random.choice(TAGS)
    name = random.choice(NAMES)
    payload = {"temp": temp, "name": name}

    device.publish_data(tag, payload)


# device.connect()