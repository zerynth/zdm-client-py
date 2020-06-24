import logging
import sys
import unittest
import time
import random
import zdm

from zdevicemanager import ZdmClient as zdmapi
from zdevicemanager.base.cfg import env

from .context import ENDPOINT

log = logging.getLogger("ZDM_cli_test")
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

received = False

class JobsTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.zapi = zdmapi(base_url=env.zdm)
        self.d = self.zapi.devices.create("Test")
        key = self.zapi.keys.create(self.d.id, "testkey")
        jwt = key.as_jwt(exp_delta_in_days=90)
        log.info("Created device {}, password {}".format(self.d.id, jwt))

        self.device = zdm.ZDMClient(device_id=self.d.id, endpoint=ENDPOINT)
        self.device.set_password(jwt)
        self.device.connect()

    def test_job(self):
        def test_job(zdmclient, args):
            global received
            received = True
            print("Executing job set_temp. Received args: {}".format(args))
            return {"msg": "Temperature set correctly."}

        my_jobs = {
            "myJob": test_job,
        }

        self.device.jobs = my_jobs

        self.zapi.jobs.schedule("myJob", {"value": 45}, [self.d.id], on_time="")
        time.sleep(6)
        self.assertEqual(True, received)