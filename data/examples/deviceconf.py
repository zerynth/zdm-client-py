import adm

# client = adm.ADMClient(fleetdev_url="http://api.zerinth.com/v1",
#                        workspace_url="http://api.zerinth.com/v1")

ADM_URL = "http://api.localhost/v1"

client = adm.ADMClient(fleetdev_url=ADM_URL, workspace_url=ADM_URL)

DEV_ID = "dev-4m30sc96ycxv"  # on local test
DEV_NAME = "my-device"

DEVICE_SECRET = "alsdkadklj"
DEVICE_AUTHKEY_ID = 1
DEVICE_AUTHKEY_EXPIRATION = '09/19/18 13:55:26'

WORKSPACE_NAME = "my-workspace"
FLEET_NAME = "my-fleet"
#
try:
    device = client.get_device(DEV_ID)
except adm.NotFoundError:
    print("Device NOT found, creating...")
    workspace = client.create_workspace(WORKSPACE_NAME)
    print(workspace)
    fleet = client.create_fleet(FLEET_NAME, workspace_id=workspace.id)
    device = client.create_device(DEV_NAME, fleetId=fleet.id)
    print("Device created".format(device))

fleet = client.get_fleet(device.fleet_id)
workspace = client.get_device_workspace(device.id)
print("Device id: {}".format(device.id))
print("Belong to fleet: {}".format(fleet.id))
print("Belong to workspace: {}".format(workspace.id))

# provision with a symmetric key
# curl -d '{"name":"prova"}' POST http://api.zerinth.com/v1/device/dev-4m2vxgc5k935/key
# key = POST http://api.zerinth.com/v1/device/dev-4m2vxgc5k935/key {"name":"prova"}
# key.id
# key.raw
# exp =  '09/19/18 13:55:26'
# jwt = device.encode_jwt(auth_keyid=key.id, secret=key.raw, exp=DEVICE_AUTHKEY_EXPIRATION)))
# jwt is the password for the device

# DEV_ID = "dev-4omytnuzcem9"
# KEY ="qea/CM1N1gOidM294wpCflPRSl1805EfMWiXA61wm1o="
# exp = "1583144016" # datetime.utcnow() + timedelta(days=31)
# KEY_ID = 1
#
# jwt = jwt.encode({'sub': DEV_ID, 'user':DEV_ID, 'exp': exp, 'key': KEY_ID}, KEY, algorithm='HS256')
# print(jwt.decode("utf-8"))
