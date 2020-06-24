import logging
import sys
import time
import unittest
import random
import string

import zdm
from zdevicemanager import ZdmClient as zdmapi
from zdevicemanager.base.cfg import env

from .context import ENDPOINT

log = logging.getLogger("ZDM_cli_test")
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

isTimeReceived = False

class TimeTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.zapi = zdmapi(base_url=env.zdm)
        self.d = self.zapi.devices.create("TestZDmclient")
        key = self.zapi.keys.create(self.d.id, "testkey")
        jwt = key.as_jwt(exp_delta_in_days=90)
        log.info("Created device {}, password {}".format(self.d.id, jwt))


        self.device = zdm.ZDMClient(device_id=self.d.id, endpoint=ENDPOINT)

        self.device.set_password(jwt)
        self.device.connect()

    def test_timestamp(self):

        def time_callback(zdmclient, arg):
            global isTimeReceived
            isTimeReceived = True
            print("{} Timestamp received: {}".format(isTimeReceived, arg))

        self.device._time_callback = time_callback

        self.device.request_timestamp()
        time.sleep(5)
        self.assertTrue(isTimeReceived)

    def test_no_timestamp_cb(self):
        self.device.request_timestamp()
        time.sleep(5)