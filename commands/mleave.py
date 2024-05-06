class M_LEAVE:

  def run(self, sid, mgroupid, router):
    subnet = router.get_subnet(sid)

    if subnet.isOnGroup(mgroupid):
       subnet.leave_group(mgroupid)
       router.remove_subnet_from_group(mgroupid, subnet.netaddr)
       print(f"{sid} => {router.rid} : mleave {mgroupid};")
    else:
      print(f"Não foi possível remover: {sid} => {router.rid} mleave {mgroupid}")
      return

