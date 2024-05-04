from state.RouterCenter import RouterCenter
import ipaddress


def ip_in_same_subnet(ip_to_check, ip_list):
    # Convert the target IP to an IP address object
    target_ip = ipaddress.ip_address(ip_to_check)

    # Check each IP in the list
    for ip_with_mask in ip_list:
        # Split the IP address and the subnet mask
        ip, subnet_mask = ip_with_mask.split('/')
        # Convert the list IP to an IP address object
        current_ip = ipaddress.ip_address(ip)
        
        # Create a network object using the IP address and subnet mask
        current_network = ipaddress.ip_network(ip_with_mask, strict=False)
        
        # Check if the target IP is within the current network
        if target_ip in current_network:
            ipWithMask = str(current_ip)+'/'+subnet_mask
            return ipWithMask
    
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
        print("broadcast")
        for thisRouterIp in self.ips: 
            # acho que tem um jeito melhor de fazer, isso mas o RPF deve solucionar qualquer problema gerado por isso
            # qual problema? é um roteador com mais de uma subrede enviar mensagens através das subredes erradas para seus vizinhos
            self.sendPing(subnet_id, mgroupid, msg, thisRouterIp)

    def receive_from_router(
        self,
        subnet_id: str,
        mgroupid: str,
        msg: str,
        original_address: str,
        last_address: str
    ):
        print("original_address", original_address)
        print(last_address)
        print("receive_from_router")
        
        print(self.routing_table)
        #fazer RPF aqui e tirar o return
        return
        self.sendPing(subnet_id, mgroupid, msg, original_address)
            
        

    def sendPing(
        self,
        subnet_id: str,
        mgroupid: str,
        msg: str,
        original_address: str,
        ):
            print("sendPing")
            #self._pingSubnets(subnet_id, mgroupid, msg)
            self._pingRouters(subnet_id, mgroupid, msg, original_address)

    def _pingSubnets(self, subnet_id: str, mgroupid: str, msg: str):
        for sid, subnet in self.subnets.items():
            if sid != subnet_id and subnet.isOnGroup(mgroupid):
                subnet.receive_from_router(self.rid, mgroupid, msg)

    def _pingRouters(
        self,
        subnet_id: str,
        mgroupid: str, 
        msg: str,
        original_address: str,
    ):
        print("_pingRouters")
        for router in self.routing_table.values():
            
            router_address = router[0].split('/')[0]
            print(f"{self.rid} =>> {router_address}: mping {mgroupid}")
            if router[0] == '0.0.0.0':
                continue
            routerDict = self.router_center.get_routers()
            
            current_subnet_especific_ip = ip_in_same_subnet(router_address, self.ips)
            
            if not current_subnet_especific_ip:
                return
            netMask = current_subnet_especific_ip.split('/')[1]
            destRouter = routerDict[router[0]+ "/"+netMask]
            
            destRouter.receive_from_router(subnet_id, mgroupid, msg, original_address, current_subnet_especific_ip)