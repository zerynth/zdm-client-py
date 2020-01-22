import adm
import random
import time

"""
Create a Device that sends messages to the ingestion queue of the ADM.
"""

NUM_MESSAGES = 100    # number of messages to send
TAGS = ["caffe", "cibo", "bevande", "armadi",
        "case", "tutto"]  # tags where to publish
NAMES= ["prova1", "prova2", "prova3", "prova4"]




exit(1)


device = adm.Device("dev01", hostname="rmq.localhost",
                    port=1883, user="admin", password="Z3rynthT3st")



device.connect()


for x in range(NUM_MESSAGES):
    time.sleep(2)
    temp = random.randint(-20, 40)  # temperature
    tag = random.choice(TAGS)
    name = random.choice(NAMES)
    payload = {"temp": temp, "name": name}
    device.publish_data(tag, payload)

device.mqqt.loop()