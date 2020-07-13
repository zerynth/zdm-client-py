"""
basic.py

Show the basic example of a ZdmClient that sends a stream of messages to the ZDM.
Each message is published into a random tag with a random value.

"""
import zdm
import random
import time

device_id = 'Your-device-id'
password = 'Device-Password'


def pub_temp_hum():
    # this function publish into the tag weather two values: the temperature and the humidity
    tag = 'weather'
    temp = random.randint(19, 38)
    hum = random.randint(50, 70)
    payload = {'temp': temp, 'hum': hum}
    device.publish(payload, tag)
    print('Published: ', payload)


# connection to the ZDM
device = zdm.ZDMClient(device_id=device_id)
device.set_password(password)
device.connect()

# infinite loop
while True:
    pub_temp_hum()
    time.sleep(5)
