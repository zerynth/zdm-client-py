# tests/runner.py
import unittest
import logging

urllib3_logger = logging.getLogger('urllib3')
urllib3_logger.setLevel(logging.CRITICAL)

from click.testing import CliRunner
from zdevicemanager.base.base import cli

# import your test modules
# from .test_data import DeviceTest
# from .test_jobs import JobsTest
from .test_conditions import ConditionsTest

# def suite():
#     suite = unittest.TestSuite()
#     suite.addTest(DeviceTest("test_device"))
#
#     return suite


if __name__ == '__main__':
    # clir = CliRunner()
    # user = "01234567891234567890123456789012@test.com" #"testzdm@zerynth.com"
    # passord = "@Zerynth18" #"Pippo123"
    # clir.invoke(cli, ['login', "--user", user, "--passwd", passord])

    runner = unittest.TextTestRunner()
    # runner.run(suite())
