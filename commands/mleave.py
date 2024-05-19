class M_LEAVE:

  def run(self, sid, mgroupid, router):
    subnet = router.get_subnet(sid)
    if subnet.isOnGroup(mgroupid):
      router.remove_subnet_from_group(mgroupid, subnet.netaddr, subnet.sid)
      subnet.leave_group(mgroupid)
