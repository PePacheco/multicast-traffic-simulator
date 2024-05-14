class M_JOIN:

  def run(self, sid, group, router):

    subnet = router.get_subnet(sid)

    if not subnet.isOnGroup(group):
      return