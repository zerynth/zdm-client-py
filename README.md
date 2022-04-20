# Zerynth ZDM Client Python Library

A python library that emulates a device for the  ZDM (Zerynth Device Manager).
The library permits: to connect to the ZDM, to send data and to receive jobs.

## Installation

The latest stable version [is available on PyPI](https://pypi.org/project/zdm-client-py/). Either add `zdm-client-py` to your `requirements.txt` file or install with pip:
```
pip install zdm-client-py==1.0.1
```
    
## Usage

Follow the steps:

1. Login to the [Zerynyth Cloud](https://cloud.zerynth.com) 
2. Select a workspace
3. Create a device. "Devices" -> "New" -> "Device"
4. Generate the credentials file for the device and save it locally. Select a Device -> "Security" -> "Confirm" -> "Download" (the file is named `zdevice.json`).
5. Create a new folder and add the following files:
    - The device credential `zdevice.json` file. 
    - A Python file `zdm_basic.py` containing the following script:

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
  5. Run the example `python zdm_basic.py`
  6. In the example, the Client connects to the Cloud and it sends an infinite stream of messages every 5 second. Every message is published with a tag "weather" containing a random temperature and humidity.

You can find other examples in the `data/examples` folder.


