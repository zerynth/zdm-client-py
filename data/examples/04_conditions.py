################################################################################
# Zerynth Device Manager
#
# Created by Zerynth Team 2020 CC
# Authors: E.Neri, D.Neri
###############################################################################
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
import zdm

logger = zdm.ZdmLogger().get_logger()


condition_tag = "battery"

# this function asks to ZDM for open conditions, then close it
def on_open_conditions(zdmclient, conditions):
    for c in conditions:
        print("Closing: ", c)
        c.close(payload={"callback": "condition closed by callback"})


device = zdm.ZDMClient(condition_tags=[condition_tag], on_open_conditions=on_open_conditions)
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

device.request_open_conditions()

while not done:
    if battery_lvl_curr > 80:
        if recharge and infoLevel.is_open():
            print("[INFO] close condition")
            infoLevel.close(payload={"status": "INFO", "lvl": battery_lvl_curr})
            done = True

    elif 60 < battery_lvl_curr <= 80:
        if not recharge and not infoLevel.is_open():
            print("[INFO] open condition")
            infoLevel.open(payload={"status": "INFO", "lvl": battery_lvl_curr})
        else:
            if warningLevel.is_open():
                print("[WARNING] close condition")
                warningLevel.close(payload={"status": "WARNING", "lvl": battery_lvl_curr})

    elif 40 < battery_lvl_curr <= 60:
        if not recharge and not warningLevel.is_open():
            print("[WARNING] open condition")
            warningLevel.open(payload={"status": "WARNING", "lvl": battery_lvl_curr})
        else:
            if criticalLevel.is_open():
                print("[CRITICAL] close condition")
                criticalLevel.close(payload={"status": "CRITICAL", "lvl": battery_lvl_curr})

    elif 20 < battery_lvl_curr <= 40:
        if not recharge and not criticalLevel.is_open():
            print("[CRITICAL] open condition")
            criticalLevel.open(payload={"status": "CRITICAL", "lvl": battery_lvl_curr})
        else:
            if fatalLevel.is_open():
                print("[FATAL] close condition")
                fatalLevel.close(payload={"status": "FATAL", "lvl": battery_lvl_curr})
    elif 10 < battery_lvl_curr <= 20:
        if not recharge and not fatalLevel.is_open():
            print("[FATAL] open condition")
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
