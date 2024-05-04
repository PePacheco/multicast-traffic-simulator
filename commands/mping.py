from models.router import Router

class M_PING:

  def run(self, sid: str, mgroupid: str, router: Router, msg: str):
    self.m_flooding(router, sid, mgroupid, msg)
    self.m_pruning(router, sid, mgroupid, msg)
    self.m_ping(router, sid, mgroupid, msg)

  def m_flooding(self, router: Router, sid: str, mgroupid: str, msg: str):
    router.broadcast(sid, mgroupid, msg)

  def m_pruning(self, router: Router, sid: str, mgroupid: str, msg: str):
    print("M_PRUNING")
    # for rid, neighbor_router in self.routers.items():
    #     if rid != router.rid:
    #         print(f"{router.rid} =>> {neighbor_router.rid}: mprune {mgroupid};")

  def m_ping(self, router: Router, sid: str, mgroupid: str, msg: str):
    print("M_PING")
