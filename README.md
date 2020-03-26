# Zerynth ZDM Client Python Library

A python library that emulates a device for the  ZDM.
It permits connect to the ZDM, send data and receives jobs.

## Installation

The latest stable version [is available on PyPI](https://pypi.org/project/zdm-client-py/). Either add `zdm-client-py` to your `requirements.txt` file or install with pip:
```
pip install zdm-client-py 
```
    
## Usage
Login to the ZDM platform (by using the [ZDM Cloud](https://zdm.zerynth.com) or the [ZDM Cli](https://docs.zerynth.com/latest/)).
Add a new device and generate a new password for the device.

Copy the obtained **Device Id** and **Password** in the example below.

In the example, the Client connects to the ZDm with the username e password.
Then it sends an infinite stream of messages onto three different tag ("bathroom", "bedroom", "living room") with a random temperature.

```python
import random
import time
import zdm

device_id = '!!! PUT YOU DEVICE_ID HERE !!!'
password = '!!! PUT YOU PASSWORD HER !!!'

device = zdm.ZDMClient(device_id=device_id)
device.set_password(password)
device.connect()

time.sleep(5)

tags = ["bathroom", "bedroom", "living room"]

while True:
   
    temp = random.randint(10, 30)  # random temperature
    tag = random.choice(tags)      # random choice of the tag
    payload = {"temp": temp}
    device.publish_data(tag, payload)
    time.sleep(1)
```

You can find other examples in the `data/examples` folder.