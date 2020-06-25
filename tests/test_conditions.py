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

received = False


class ConditionsTest(unittest.TestCase):

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

    def test_open_close_condition(self):
        tag = self._rand_name()

        self.device.conditions = [tag]

        c = self.device.new_condition(tag)

        c.open({"data": "ok-test"})
        time.sleep(5)
        cond = self.zapi.conditions.list(self.d.workspace_id, tag, device_id=self.d.id)
        self.assertEqual(1, len(cond))
        c.close()
        time.sleep(5)
        cond_close = self.zapi.conditions.list(self.d.workspace_id, tag, device_id=self.d.id, status="closed")
        cond_open = self.zapi.conditions.list(self.d.workspace_id, tag, device_id=self.d.id, status="open")
        self.assertEqual(1, len(cond_close))
        self.assertEqual(0, len(cond_open))
        c.reset()

    def test_get_non_existing(self):
        with self.assertRaises(Exception) as context:
            self.device.new_condition("not-ed")
        self.assertTrue('not found' in str(context.exception))

    def _rand_name(self):
        # printing lowercase
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(10))

    def test_request_conditions(self):
        """
        Simulate the case in which the device open two conditions.
        Than it requests the open conditions and close them.
        """
        def on_open_conditions(client, conditions):
            for c in conditions:
                c.close()

        self.device._on_open_conditions = on_open_conditions

        tag = self._rand_name()
        tag1 = self._rand_name()
        self.device.conditions = [tag, tag1]
        c = self.device.new_condition(tag)
        c.open({"data": "0"})
        cond = self.zapi.conditions.list(self.d.workspace_id, tag, device_id=self.d.id, status="open")
        self.assertEqual(1, len(cond))
        time.sleep(2)
        self.device.request_open_conditions()
        # wait close conditions
        time.sleep(5)
        cond = self.zapi.conditions.list(self.d.workspace_id, tag, device_id=self.d.id, status="open")
        self.assertEqual(0, len(cond))
        cond_close = self.zapi.conditions.list(self.d.workspace_id, tag, device_id=self.d.id, status="closed")
        self.assertEqual(1, len(cond_close))

