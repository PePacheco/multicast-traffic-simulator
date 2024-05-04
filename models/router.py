from state.RouterCenter import RouterCenter


class Router:
    def __init__(self, rid, numifs, ips, subnets):
        self.rid = rid
        self.numifs = numifs
        self.ips = ips
        self.subnets = subnets
        self.routing_table = {}  # Tabela de roteamento
        self.router_center = RouterCenter.get_instance()

    def add_route(self, netaddr: str, nexthop: str, ifnum: str):
        self.routing_table[netaddr] = (nexthop, ifnum)

    def get_subnet(self, sid):
        return self.subnets[sid]

    def broadcast(self, subnet_id: str, mgroupid: str, msg: str):
        print(f"{subnet_id} =>> {self.rid} : mping {mgroupid} {msg}")
        for sid, subnet in self.subnets.items():
            if sid != subnet_id and subnet.isOnGroup(mgroupid): # Nao envia para a subnet que recebeu
                subnet.receive_from_router(self.rid, mgroupid, msg)
        # print(f'{self.rid} self.routing_table', self.routing_table)
        for destination, router in self.routing_table.items():
            router_address = router[0]
            if router_address == '0.0.0.0':
                continue
            print(router_address)
        print(self.router_center.get_routers())
