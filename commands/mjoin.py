class M_JOIN:

  def run(self, sid, group, router):
    subnet = router.get_subnet(sid)
    if not subnet.isOnGroup(group):
      router.add_subnet_to_group(group, subnet.netaddr, subnet.sid)
      subnet.join_group(group)