from models.router import Router

class M_PING:

  def run(self, sid: str, mgroupid: str, router: Router, msg: str):
    router.start_ping(sid, mgroupid, msg)
    return