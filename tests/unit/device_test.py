import adm 

import unittest


class DeviceTest(unittest.TestCase):

    def test_events(self):
        d = adm.device.Device("dev1")
        assert d.id == "dev01"