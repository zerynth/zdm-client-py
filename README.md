# Zerynth ZDM Client Python Library

A python library that emulates a device for the  ZDM (Zerynth Device Manager).
The library permits: to connect to the ZDM, to send data and to receive jobs.

## Installation

The latest stable version [is available on PyPI](https://pypi.org/project/zdm-client-py/). Either add `zdm-client-py` to your `requirements.txt` file or install with pip:
```
pip install zdm-client-py
```
    
## Usage

Follow the guide [here](https://docs.zerynth.com/latest/deploy/getting_started_with_rpi/)

1. Login to the ZDM platform (by using the [ZDM Web](https://zdm.zerynth.com) or the [ZDM CLI](https://www.zerynth.com/blog/docs/zdm/getting-started/the-zdm-command-line-interface/)).
2. Create a device
3. Generate the credentials for the device (file `zdevice.json`)
4. Create a new Python project with your preferred editor and paste the `zdevice.json` file inside it. 
5.  Create a Python file `zdm_basic.py` and paste this simple code into it:

```python
import zdm
import random
import time

def pub_temp_hum():
    # this function publish into the tag weather two random values: the temperature and the humidity
    tag = 'weather'
    temp = random.randint(19, 38)
    hum = random.randint(50, 70)
    payload = {'temp': temp, 'hum': hum}
    device.publish(payload, tag)
    print('Published: ', payload)


# connect to the ZDM using credentials in zdevice.json file
device = zdm.ZDMClient()
device.connect()

# infinite loop
while True:
    pub_temp_hum()
    time.sleep(5)
```
In the example, the Client connects to the ZDM with the username e password.
Then it sends an infinite stream of messages onto three different tags ("bathroom", "bedroom", "living room") with a random temperature.

You can find other examples in the `data/examples` folder.
