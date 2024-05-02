class Subnet:
    def __init__(self, sid, netaddr):
        self.sid = sid
        self.netaddr = netaddr
        self.groups = set()

    def join_group(self, mgroupid):
        return self.groups.add(mgroupid)

    def leave_group(self, mgroupid):
        self.groups.discard(mgroupid)

    def is_on_group(self, mgroupid):
        for m in self.groups:
            if m == mgroupid:
                return m
        return False

    def receive_from_router(self, router_id, mgroupid, msg):
        print(f"{router_id} =>> {self.sid} : mping {mgroupid} {msg}")