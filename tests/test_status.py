import logging
import sys
import time
import unittest

import zdm
from zdevicemanager import ZdmClient as zdmapi
from zdevicemanager.base.cfg import env

from .context import ENDPOINT

log = logging.getLogger("ZDM_cli_test")
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

received = False


class StatusTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.zapi = zdmapi(base_url=env.zdm)
        self.d = self.zapi.devices.create("Test")
        key = self.zapi.keys.create(self.d.id, "testkey")
        self.jwt = key.as_jwt(exp_delta_in_days=90)
        log.info("Created device {}, password {}".format(self.d.id, self.jwt))

    def test_expected_status(self):
        """"
        Test the expected status.
        Simulate the case in whicj the cloud schedule a job but the device is not online.
        when the device connect the fist time. it requests the status and execute the jobs
        """
        job = "myJob"

        self.zapi.jobs.schedule(job, {"value": 45}, [self.d.id], on_time="")

        status = self.zapi.jobs.status_expected(job, self.d.id)
        self.assertEqual("@" + job, status.key)

        def test_job(zdmclient, args):
            global received
            received = True
            v = args["value"]
            print("Executing job. Received args: {}".format(args))
            return {"value": v + 1}

        my_jobs = {
                job: test_job,
        }
        self.device = zdm.ZDMClient(device_id=self.d.id, jobs=my_jobs, endpoint=ENDPOINT)
        self.device.set_password(self.jwt)
        self.device.connect()

        time.sleep(6)
        self.assertEqual(True, received)
        status = self.zapi.jobs.status_current(job, self.d.id)
        self.assertEqual("@" + job, status.key)

        status = self.zapi.jobs.status_expected(job, self.d.id)
        self.assertEqual(None, status)

        # self.assertEqual(1, v)
