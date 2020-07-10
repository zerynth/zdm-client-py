"""
conditions.py

The example show how to use the conditions for monitoring the charge of a battery.
The example uses four different conditions on the same tag for controlling four different battery charge levels.
 60% - 80% : info
 40% - 60% : warning
 20% - 40% : critical
 0% -  20% : fatal
Initially, the battery is 100%.
Then, every second the level of the battery is decreased, and whenever the battery is running low a certain recharge level,
the corresponding condition is opened (E.g., when the battery reaches 80% the INFO condition is opened).
When the battery runs below 10%, the battery is set on recharge state.
In recharge mode, the battery level id increased, and whenever the level reach a certain recharge level, the previous condition is closed.
(e.g., when the battery is recharged and the level is 40% the CRITICAL condition is closed).

"""
import time

from zdm import ZDMClient
from zdm.logging import ZdmLogger

logger = ZdmLogger().get_logger()

device_id = '*** PUT YOU DEVICE ID HERE ***'
password = '*** PUT YOUR PASSWORD HERE ***'

device_id = 'dev-51f1yfx47lf6'
password = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOjEsImV4cCI6MTYyNDY5NTEyMiwiaWF0IjoxNTkzMTU5MTIyLCJzdWIiOiJkZXYtNTFmMXlmeDQ3bGY2In0.nuoq52Z4G-u25KTXy3Vkde1FIA296qwhP7bx7M2fN4k'

device_id = 'dev-51fp75qtkfg6'
password = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOjEsImV4cCI6MTYyNDcxMDc1NSwiaWF0IjoxNTkzMTc0NzU1LCJzdWIiOiJkZXYtNTFmcDc1cXRrZmc2In0.mfn8CL93rqJxFp0TojuGB1FisEFo5SZaLKBeSK4QZBk'

device_id = 'dev-5216sexaivwm'
password = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOjEsImV4cCI6MTYyNTIzMjQ5MiwiaWF0IjoxNTkzNjk2NDkyLCJzdWIiOiJkZXYtNTIxNnNleGFpdndtIn0.jAJk1_v63kQou_5rha7PavgpbECZ1HIDgtHOkdhD97Y'

device_id = 'dev-51ql34p9azub'
password = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOjEsImV4cCI6MTYyNTMyNTY3NiwiaWF0IjoxNTkzNzg5Njc2LCJzdWIiOiJkZXYtNTFxbDM0cDlhenViIn0._Nf3906N2VmxgOeKTqFn_s-6k2jhzx4JkLKQZWyGOVk'

device_id = 'dev-5216sexaivwm'
password = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOjEsImV4cCI6MTYyNTMyNjAyMiwiaWF0IjoxNTkzNzkwMDIyLCJzdWIiOiJkZXYtNTIxNnNleGFpdndtIn0.AN_qoPDwcP7HkhnbrzccV5htqyoRXzh_T-96jv6cgJY'

device_id = 'dev-52i83w2lk16r'
password = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOjEsImV4cCI6MTYyNTY0MzY3MiwiaWF0IjoxNTk0MTA3NjcyLCJzdWIiOiJkZXYtNTJpODN3MmxrMTZyIn0.bo-ZxObPnrpV4fnU9z74gJ6T0fUkTCpf7SoFlhnRgUA'


condition_tag = "battery"

device = ZDMClient(device_id=device_id, condition_tags=[condition_tag], endpoint="rmq.localhost")
device.set_password(password)
device.connect()

# Create four conditions on the same tag.
# Note. The condition_tag must be passed in the conditions_tags parameter of the constructor
infoLevel = device.new_condition(condition_tag)
warningLevel = device.new_condition(condition_tag)
criticalLevel = device.new_condition(condition_tag)
fatalLevel = device.new_condition(condition_tag)

# initially the battery level is 100%
battery_lvl_curr = 100
battery_lvl_prv = 100

# indicate if the battery is in the recharge state
recharge = False
done = False

while not done:
    if battery_lvl_curr > 80:
        if recharge:
            infoLevel.close()
            done = True

    elif 60 < battery_lvl_curr <= 80:
        if not recharge:
            infoLevel.open(payload={"status": "INFO", "lvl": battery_lvl_curr})
        else:
            warningLevel.close()

    elif 40 < battery_lvl_curr <= 60:
        if not recharge:
            warningLevel.open(payload={"status": "WARNING", "lvl": battery_lvl_curr})
        else:
            criticalLevel.close()

    elif 20 < battery_lvl_curr <= 40:
        if not recharge:
            criticalLevel.open(payload={"status": "CRITICAL", "lvl": battery_lvl_curr})
        else:
            fatalLevel.close()

    elif 10 < battery_lvl_curr <= 20:
        if recharge:
            fatalLevel.open(payload={"status": "FATAL", "lvl": battery_lvl_curr})

    elif 0 < battery_lvl_curr <= 10:
        logger.info("Recharging battery")
        recharge = True

    battery_lvl_prv = battery_lvl_curr
    if recharge:
        battery_lvl_curr = battery_lvl_curr + 5
    else:
        battery_lvl_curr = battery_lvl_curr - 5
    time.sleep(2)

logger.info("Bye bye :)")