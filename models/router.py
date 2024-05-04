from state.RouterCenter import RouterCenter
import ipaddress


def ip_in_same_subnet(ip_to_check, ip_list):
    # Convert the target IP to an IP network object
    target_network = ipaddress.ip_network(ip_to_check, strict=False)

    # Check each IP in the list
    for ip in ip_list:
        # Convert the list IP to an IP address object (not a network)
        current_ip = ipaddress.ip_address(ip.split('/')[0])

        # Check if the current IP is in the same network as the target IP
        if current_ip in target_network:
            return current_ip
    return None


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
        # RVSP HERE
        #self._pingSubnets(subnet_id, mgroupid, msg)
        self._pingRouters(subnet_id, mgroupid, msg, self.rid, self.rid)

    def _pingSubnets(self, subnet_id: str, mgroupid: str, msg: str):
        for sid, subnet in self.subnets.items():
            if sid != subnet_id and subnet.isOnGroup(mgroupid):
                subnet.receive_from_router(self.rid, mgroupid, msg)

    def _pingRouters(
        self,
        subnet_id: str,
        mgroupid: str, msg: str,
        original_address: str,
        last_address: str
    ):
        for router in self.routing_table.values():
            router_address = router[0].split('/')[0]
            print(f"{self.rid} =>> {router_address}: mping {mgroupid}")
            if router[0] == '0.0.0.0':
                continue
            routerDict = self.router_center.get_routers()
            current_ip = ip_in_same_subnet(router_address, self.ips)

            if not current_ip:
                return

            routerDict[router_address].broadcast(subnet_id, mgroupid, msg, original_address, current_ip)
