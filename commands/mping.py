from models.router import Router

class M_PING:

  def run(self, sid: str, mgroupid: str, router: Router, msg: str):
      print(f'{sid} =>> {router.rid} : mping {mgroupid} {msg};')
      router.start_ping(sid, mgroupid, msg)
