.. module:: zerynthzdmclient

.. _lib.zerynth.zdmclient:
.. _lib.zerynth.condition:

**********************
ZDM Client Python
**********************

The Zerynth ZDM Client is a Python implementation of a client of the ZDM.
It can be used to emulate a Zerynth device and connect it to the ZDM.
====================
The ZDMClient class
===================

.. class:: ZDMClient(device_id,  endpoint=ENDPOINT, jobs=None, condition_tags=[], verbose=False, on_timestamp=None, on_open_conditions=None)

    Creates a ZDM client instance with device id :samp:`device_id`. All other parameters are optional and have default values.

    * :samp:`device_id` is the id of the device.
    * :samp:`endpoint` is the url of the ZDM broker (default mqtt.zdm.zerynth.com).
    * :samp:`jobs` is the dictionary that defines the device's available jobs (default None).
    * :samp:`condition_tags` is the list of condition tags that the device can open and close (default []).
    * :samp:`verbose` boolean flag for verbose output (default False).
    * :samp:`on_timestamp` called when the ZDM responds to the timestamp request. on_timestamp(client, timestamp)
    * :samp:`on_open_conditions` called when the ZDM responds to the open conditions request. on_open_conditions(client, conditions)

    
.. method:: id()

        Return the device id.
        
.. method:: connect()

        Connect the device to the ZDM.
        You must set device's password first.
        
.. method:: set_password(pw)

    Set the device password to :samp:`pw`. You can generate a password using the ZDM.
    
.. method:: publish(data, tag)

    Publish teh data to the ZDM.

    * :samp:`data`, is a dictionary tha contains the message to be published
    * :samp:`tag`, is a string representing the tag where the data is published.
    
.. method:: request_timestamp()

    Send a request to the ZDM to obtain the timestamp.

    
.. method:: request_open_conditions()

    Send a request to the ZDM to obtain the current open conditions.
.. method:: new_condition()

Create and return a new condition.

     * :samp:`condition_tag`, the tag of the new condition.
====================
The Condition class
===================

.. class:: Conditions(client. tag)

Creates a new Condition assocaited to a tag.

* :samp:`client` is the reference to a ZDMClient object
* :samp:`tag` is the tag of the condition

    
.. method:: open(payload=None, start=None)

    Open the condition.

        * :samp:`payload`, a dictionary for associating additional data to the opened condition (default None).
        * :samp:`start`, a date time (rfc3339) used to  set the start time, If None the current timestamp is used (default None).
    
.. method:: close(payload=None, start=None)

    Close the condition.

    * :samp:`payload`, a dictionary for associating additional data to the closed condition. Default None.
    * :samp:`finish`, a date time (rfc3339) used to  set the finish time of the condition. If None the current timestamp is used. Default None.
.. method:: reset()

    Reset the condition by generatung a new id and resetting the start and end time.
.. method:: is_open()

Return True if the condition is open. False otherwise.
