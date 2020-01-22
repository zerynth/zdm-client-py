class Device:
    """Device class represent a device"""

    def __init__(self, id, name, fleet_id=None):
        self.id = id
        self.name = name
        self.fleet_id = fleet_id

    @staticmethod
    def from_json(json):
        # {"Device":{"id":"dev-4lvyidx953wh","name":"dica","fleet_id":"","created_at":"2020-01-21T15:41:35.837857Z"}}
        dev = json["device"]
        return Device(dev["id"], dev["name"], dev["fleet_id"] if dev["fleet_id"] is not "" else None)

    def __str__(self):
        return "Device: id: {}, name:{}, fleetid :{}".format(self.id, self.name, self.fleet_id)