class Workspace:
    """Workspace class represent a device"""

    def __init__(self, id, name, account_id=None):
        self.id = id
        self.name = name
        self.account_id = account_id

    @staticmethod
    def from_json(json):
        # {"Workspace":{"id":"wks-4lvz89ccmepv", "name":"do","account_id":"",
        # "Description":"","Fleets":null,"created_at":"2020-01-21T15:49:39.230924Z"}}
        wks = json["workspace"]
        return Workspace(wks["id"], wks["name"], wks["account_id"] if wks["account_id"] is not "" else None)

    def __str__(self):
        return "Workspace: id: {}, name:{}, account:{}".format(self.id, self.name, self.account_id)