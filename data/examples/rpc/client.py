import adm
"""
Client of the ADM  that send an RPC to a device by calling the RPC service API
"""

client = adm.ADMClient(rpc_url="http://api.zerinth.com")

# RPC to be sent to the device
rpc = {'method': 'set_led', 'args': {"led": "on"}, "devices": ["dev01"]}

client.send_rpc(payload=rpc)
