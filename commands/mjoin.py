class M_JOIN:

    def run(self, sid, group, router):

        subnet = router.get_subnet(sid)

        if subnet.isOnGroup(group):
            print(f"Já está no grupo {group}")
            return
        subnet.join_group(group)

        if subnet.isOnGroup(group):
            print(f"{sid} => {router.rid} : mjoin {subnet.isOnGroup(group)};")
        else:
            print("ERRO AO ADICIONAR O GRUPO!")