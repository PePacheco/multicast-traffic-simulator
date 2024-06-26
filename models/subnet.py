from logs.Logger import Logger
class Subnet:
  def __init__(self, sid, netaddr):
      self.sid = sid
      self.netaddr = netaddr
      self.groups = set()
      self.logger = Logger.get_instance()

  def join_group(self, mgroupid):
      return self.groups.add(mgroupid)

  def leave_group(self, mgroupid):
      self.groups.discard(mgroupid)

  def isOnGroup(self, mgroupid):
    for m in self.groups:
        if m == mgroupid:
          return (m)
    return (False)
  
  def receive_ping_from_router(self, sender_rid: str, mgroupid: str, message: str):
        self.logger.received_ping_from_router(sender_rid, self.sid, message)
        return