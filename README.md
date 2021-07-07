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

1. Login to the ZDM platform (by using the [ZDM Web](https://zdm.zerynth.com) or the [ZDM CLI](https://www.zerynth.com/blog/docs/zdm/getting-started/the-zdm-command-line-interface/)).
2. Enter into a workspace and create a new device. "Devices" -> "Add Device"
3. Generate the credentials file (named `zdevice.json`) for the device. "Security" -> "Ok" -> "Download Credentials"
4. Create a new folfer and copy into it the:
    - The credential `zdevice.json` file. 
    - A Python file `zdm_basic.py` containing the followinf script:

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
  6
In the example, the Client connects to the ZDM with the username e password.
Then it sends an infinite stream of messages onto three different tags ("bathroom", "bedroom", "living room") with a random temperature.

You can find other examples in the `data/examples` folder.


