import os

from zdevicemanager.base import init_all

init_all()

# before running the test
# $ export ZERYNTH_TESTMODE = X (0 prod, 1 localhost, 2 test, 3 stage)
# $ zdm login

# TODO: login with
#  user: testzdm@zeryth.com
#  password: Pippo123
if os.environ['ZERYNTH_TESTMODE'] == '1':
    ENDPOINT = "rmq.localhost"
    os.environ.setdefault("ZERYNTH_ZDM_URL", "http://api.adm.localhost")
elif os.environ['ZERYNTH_TESTMODE'] == '2':
    ENDPOINT = "mqtt.zdm.test.zerynth.com"
elif os.environ['ZERYNTH_TESTMODE'] == '3':
    ENDPOINT = "mqtt.zdm.stage.zerynth.com"
elif os.environ['ZERYNTH_TESTMODE'] == '0':
    ENDPOINT = "mqtt.zdm.zerynth.com"
else:
    print("Bad zerynth test mode value")
    exit(1)


