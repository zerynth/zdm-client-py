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
            print("Executing job. Received args: {}".format(args))
            ct = args['count']
            return {"count": ct + 1}

        job = "myJob"
        my_jobs = {
            job: test_job,
        }

        self.device.jobs = my_jobs

        self.zapi.jobs.schedule(job, {"count": 0}, [self.d.id], on_time="")
        time.sleep(6)
        self.assertEqual(True, received)
        status = self.zapi.jobs.status_current(job, self.d.id)
        self.assertEqual("@" + job, status.key)
        self.assertEqual(1, status.value['count'])

    def test_fota_not_supported(self):
        job = "fota"
        self.zapi.jobs.schedule(job, {}, [self.d.id], on_time="")
        time.sleep(6)
        status = self.zapi.jobs.status_current(job, self.d.id)
        self.assertEqual("@" + job, status.key)
        self.assertIn("error", status.value)

    def test_job_not_supported(self):
        job = "not-existing"
        self.zapi.jobs.schedule(job, {}, [self.d.id], on_time="")
        time.sleep(6)
        status = self.zapi.jobs.status_current(job, self.d.id)
        # self.assertEqual("@" + job, status.key)
        self.assertIn("error", status.value.keys())

    def test_job_raise_expection(self):
        job = "myJobException"

        def job_exc(zdmclient, args):
            raise Exception("Some error occur")

        my_jobs = {
            job: job_exc,
        }

        self.device.jobs = my_jobs

        self.zapi.jobs.schedule(job, {}, [self.d.id], on_time="")
        time.sleep(6)
        status = self.zapi.jobs.status_current(job, self.d.id)
        self.assertEqual("@" + job, status.key)
        self.assertIn("error", status.value.keys())