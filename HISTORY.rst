=======
History
=======

0.1.0 (2020-05-14)
----------------------------
* added wait_for_publish() to the published msg in order to guarantee that the message is sent to the ZDM
* added the send_event() method for sending events to the ZDM.

0.0.11 (2020-05-04)
----------------------------
* fix json load arguments of job

0.0.10 (2020-04-27)
----------------------------
* Changed default endpoint to "mqtt.zdm.zerynth.com"
* Fix args of Jobs as ./json


0.0.7 (2020-04-09)
----------------------------
* modified examples
* copy examples in /usr/share/zdm/examples folder

0.0.6 (2020-03-30)
----------------------------

* Fix error in _handle_dn_msg decode msg to str with python3.5


0.0.5 (2020-03-29)
----------------------------

* Fix error manifest with empty jobs.


0.0.4 (2020-03-29)
----------------------------
New functionality:

* Verbose parameter to ZdmClient class


0.0.3 (2020-03-27)
----------------------------
Release with support Python >3

* Create ZDmClient
* Publish messages to ZDM
* Received Jobs from ZDM
