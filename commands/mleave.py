class M_LEAVE:

  def run(self, sid, mgroupid, router):
    subnet = router.get_subnet(sid)

    if subnet.isOnGroup(mgroupid):
       subnet.leave_group(mgroupid)
    else:
      print(f"Não foi possível remover: {sid} => {router.rid} mleave {mgroupid}")
      return

    if not subnet.isOnGroup(mgroupid):
      print(f"{sid} => {router.rid} : mleave {mgroupid};")
    else:
      print("ERRO AO REMOVER DO GRUPO!")