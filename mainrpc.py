import adm


client = adm.ADMClient(rpc_url="http://127.0.0.1:7777")

rpc = {'method': 'get_temp', 'parameters': None, "devices":["dev01"]}
client.send_rpc(payload=rpc)