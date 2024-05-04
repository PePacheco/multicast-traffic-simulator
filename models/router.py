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
       
       #self._pingSubnets(subnet_id, mgroupid, msg)
        self._pingRouters(subnet_id, mgroupid, msg)

    def _pingSubnets(self, subnet_id: str, mgroupid: str, msg: str):
        for sid, subnet in self.subnets.items():
            if sid != subnet_id and subnet.isOnGroup(mgroupid):
                subnet.receive_from_router(self.rid, mgroupid, msg)

    def _pingRouters(self, subnet_id: str, mgroupid: str, msg: str):
        
        for router in self.routing_table.values():
            router_address = router[0]
            if router_address == '0.0.0.0':
                continue
            routerDict = self.router_center.get_routers()            
            routerDict[router_address].broadcast(subnet_id, mgroupid, msg)
            print(f"{self.rid} =>> {router_address}: mping {mgroupid}")
