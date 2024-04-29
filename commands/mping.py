class M_PING:

  def run(self, sid, mgroupid, router, msg):
    self.m_flooding(router, sid, mgroupid, msg)
    self.m_pruning(router, sid, mgroupid, msg)
    self.m_ping(router, sid, mgroupid, msg)

  def m_flooding(self, router, sid, mgroupid, msg):
    router.receive_from_subnet(sid, mgroupid, msg)

  def m_pruning(self, router, sid, mgroupid, msg):
    print("M_PRUNING")
    # for rid, neighbor_router in self.routers.items():
    #     if rid != router.rid:
    #         print(f"{router.rid} =>> {neighbor_router.rid}: mprune {mgroupid};")

  def m_ping(self, router, sid, mgroupid, msg):
    print("M_PING")
