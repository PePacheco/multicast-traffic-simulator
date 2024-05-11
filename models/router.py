from state.RouterCenter import RouterCenter
from helpers.ip import ip_to_network, ip_in_same_subnet
from models.subnet import Subnet


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

    def _find_router(self, router_id: str) :
        for router in RouterCenter.get_instance().get_routers():
            if router.rid == router_id:
                return router
        return None

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
            print(f'{flood_flow[:-2]} : mflood {mgroupid};')

        for item in pruned_items.items():
            if not item[1]['is_ok']: # prune
                print(f'{self.rid} >> {item[0]} : mprune {mgroupid};')

        for item in pruned_items.items():
            if item[1]['is_ok']: # not pruned
                print(f'{self.rid} =>> {item[0]} : mping {mgroupid} {msg};')

        for subnet in pinged_items:
            subnet.receive_from_router(subnet_id, mgroupid, msg)

        local_recv_flow = ''
        local_ping_flow = ''
        for sid in self.subnets:
            subnet = self.get_subnet(sid)
            if subnet.sid != subnet_id and subnet.isOnGroup(mgroupid):
                local_recv_flow += subnet.receive_from_router(subnet_id, mgroupid, msg)
                local_ping_flow += f'{self.rid} =>> {subnet.sid}, '

        if local_ping_flow:
            print(f'{local_ping_flow[:-2]} : mping {mgroupid} {msg};')

        for string in local_recv_flow.split(','):
            if string:
                print(string)
