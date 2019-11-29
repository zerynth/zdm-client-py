from adm.device import Device
import time


device = Device("dev01")
device.mqqt.connect()


for x in range (2000):
    time.sleep(2)
    print("{} Pubishded".format(x))
    
    device.publish_data("{} prova".format(x))


device.mqqt.loop()