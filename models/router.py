from state.RouterCenter import RouterCenter
from helpers.ip import ip_to_network, ip_in_same_subnet


class Router:
    def __init__(self, rid, numifs, ips, subnets):
        self.rid = rid
        self.numifs = numifs
        self.ips = ips
        self.subnets = subnets
        self.routing_table = {}  # Tabela de roteamento
        self.groups = {}
        self.router_center = RouterCenter.get_instance()

    def add_route(self, netaddr: str, nexthop: str, ifnum: str):
        self.routing_table[netaddr] = (nexthop, ifnum)

    def get_subnet(self, sid):
        return self.subnets[sid]

    def add_subnet_to_group(self, mgroupid: str, subnet_addr: str):
        if mgroupid in self.groups:
            self.groups[mgroupid].append(subnet_addr)
            return
        self.groups[mgroupid] = [subnet_addr]

    def remove_subnet_from_group(self, mgroupid: str, subnet_addr: str):
        self.groups[mgroupid].remove(subnet_addr)

    def start_ping(self, subnet_id: str, mgroupid: str, msg: str):
        originSubnetAddress = self.subnets[subnet_id].netaddr
        self._flood_routers(subnet_id, mgroupid, msg,  originSubnetAddress)

    def receive_from_router(
        self,
        subnet_id: str,
        mgroupid: str,
        msg: str,
        original_address: str,
        last_address: str,
        received_from_last_router_id: str
    ) -> dict:
        # Reverse path forwarding
        originalAdressNetworkAdress = ip_to_network(original_address)
        pathAdress = self.routing_table.get(originalAdressNetworkAdress)[0]
        if pathAdress == last_address:
            # print(f'{self.rid} flooding')
            self._flood_routers(subnet_id, mgroupid, msg, original_address)

        routerCenter = RouterCenter.get_instance()
        for id in routerCenter.router_ids:
            if id != self.rid and id != received_from_last_router_id:
                print(f'{self.rid} >> {id} : mflood {mgroupid};')
        is_ok = self._prune(mgroupid, received_from_last_router_id)

        return { self.rid: { 'is_ok': is_ok }}

    def _prune(self, mgroupid: str, router_id: str):
        if mgroupid not in self.groups or len(self.groups[mgroupid]) == 0:
            print(f'{self.rid} >> {router_id} : mprune {mgroupid}')
            return False
        return True

    def _ping_subnets(self, subnet_id: str, mgroupid: str, router) -> list:
        subnets_to_ping = []
        for sid, subnet in router.subnets.items():
            if sid != subnet_id and subnet.isOnGroup(mgroupid):
                subnets_to_ping.append(subnet)
        return subnets_to_ping

    def _flood_routers(
        self,
        subnet_id: str,
        mgroupid: str,
        msg: str,
        original_address: str,
    ):
        pruned_items = {}
        pinged_items = []
        flood_flow = ''

        for router in self.routing_table.values():
            router_address = router[0].split('/')[0]
            if router[0] == '0.0.0.0':
                continue
            router_dict = self.router_center.get_routers()

            current_subnet_especific_ip = ip_in_same_subnet(router_address, self.ips)

            if not current_subnet_especific_ip:
                return
            net_mask: str = current_subnet_especific_ip.split('/')[1]
            dest_router: Router = router_dict[router[0]+ "/" + net_mask]
            is_destine_router_ok = dest_router.receive_from_router(subnet_id, mgroupid, msg, original_address, current_subnet_especific_ip, self.rid)
            pruned_items = {**pruned_items, **is_destine_router_ok}
            pinged_items = [*pinged_items, *self._ping_subnets(subnet_id, mgroupid, dest_router)]
            flood_flow += f'{self.rid} >> {dest_router.rid}, '

        if flood_flow:
            print(f'{flood_flow[:-2]} : mflood {mgroupid}')

        for item in pruned_items.items():
            if not item[1]['is_ok']: # prune
                print(f'{self.rid} >> {item[0]} : mprune {mgroupid}')

        for subnet in pinged_items:
            subnet.receive_from_router(subnet_id, mgroupid, msg)

        for sid in self.subnets:
            subnet = self.get_subnet(sid)
            if subnet.sid != subnet_id and subnet.isOnGroup(mgroupid):
                subnet.receive_from_router(subnet_id, mgroupid, msg)
