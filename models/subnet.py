class Subnet:
  def __init__(self, sid, netaddr):
      self.sid = sid
      self.netaddr = netaddr
      self.groups = set()

  def join_group(self, mgroupid):
      return self.groups.add(mgroupid)

  def leave_group(self, mgroupid):
      self.groups.discard(mgroupid)

  def isOnGroup(self, mgroupid):
    for m in self.groups:
        if m == mgroupid:
          return (m)
    return (False)

  def receive_from_router(self, subnet_id, mgroupid, msg) -> str:
      return f"{self.sid} box {self.sid} : {mgroupid}#{msg} from {subnet_id};,"
