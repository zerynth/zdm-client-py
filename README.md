# adm-py

ADM SDK for python
It permits to:
   - emulate a device (publish data to the ADM, receive and responde to RPC.
   - mange RPC


#### Usage

```
$ pip install git+ssh://git@repo.zerynth.com:10022/zerynth-adm/adm-py.git@master#egg=adm-py

$ adm-py 

Generate new instance
Usage: adm-py [OPTIONS] COMMAND [ARGS]...

  CLI of the ADM SDK.

Options:
  --help  Show this message and exit.

Commands:
  device  Emulated a Device
  rpc     Manage the RPC
```