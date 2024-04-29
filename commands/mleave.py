class M_LEAVE:

  def run(self, subnet, group):
    if subnet.isOnGroup(group):
       subnet.leave_group(group)
    else:
      print(f"Não tem essa bosta ai {group}")
      return

    if not subnet.isOnGroup(group):
      print(f"M_LEAVE {subnet.sid} {group}")
    else:
      print("ERRO AO REMOVER O GRUPO!")
      pass
