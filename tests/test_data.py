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


class DeviceTest(unittest.TestCase):

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

    def test_publish_data(self):
        num = 3
        tags = ['tag1', 'tag2']
        for x in range(num):
            for t in tags:
                value = random.randint(0, 20)
                payload = {
                    'value': value
                }
                # publish payload to ZDM
                self.device.publish_data(t, payload)
                time.sleep(1)

        for t in tags:
            data = self.zapi.data.get(self.d.workspace_id, t, self.d.id)
            self.assertEqual(num, len(data))
