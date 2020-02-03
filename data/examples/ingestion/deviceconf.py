import adm

# client = adm.ADMClient(fleetdev_url="http://api.zerinth.com/v1",
#                        workspace_url="http://api.zerinth.com/v1")

client = adm.ADMClient(fleetdev_url="http://api.zerinth.com/v1",
                       workspace_url="http://api.zerinth.com/v1")

DEV_ID = "dev-4m30sc96ycxv"  # on local test
#DEV_ID = "dev-4m30sc96ycxv"  # on test zrinth.com
DEV_NAME = "my-device"
DEVICE_SECRET = "alsdkadklj"
DEVICE_AUTHKEY_ID = 1
DEVICE_AUTHKEY_EXPIRATION = '09/19/18 13:55:26'

WORKSPACE_NAME = "my-workspace"
FLEET_NAME = "my-fleet"

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

## provision with a symmetric key

print("JWT {}".format(device.encode_jwt(auth_keyid=DEVICE_AUTHKEY_ID, secret=DEVICE_SECRET, exp=DEVICE_AUTHKEY_EXPIRATION)))

