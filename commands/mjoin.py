class M_JOIN:

  def run(self, sid, group, router):

    subnet = router.get_subnet(sid)

    if not subnet.isOnGroup(group):
        subnet.join_group(group)
        router.add_subnet_to_group(group, subnet.netaddr)
    else:
      print(f"Já está no grupo {group}")
      return

    if subnet.isOnGroup(group):
      print(f"{sid} => {router.rid} : mjoin {subnet.isOnGroup(group)};")
    else:
      print("ERRO AO ADICIONAR O GRUPO!")
