class M_LEAVE:

    def run(self, sid, mgroupid, router):
        subnet = router.get_subnet(sid)

        if not subnet.isOnGroup(mgroupid):
            print(f"Não foi possível remover: {sid} => {router.rid} mleave {mgroupid}")
            return
        subnet.leave_group(mgroupid)

        if not subnet.isOnGroup(mgroupid):
            print(f"{sid} => {router.rid} : mleave {mgroupid};")
        else:
            print("ERRO AO REMOVER DO GRUPO!")