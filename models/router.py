
from helpers.ip import ip_to_network, ip_in_same_subnet
from models.subnet import Subnet
from message_types.base_message import BaseMessage
from message_types.flood_message import FloodMessage
from message_types.ok_message import OkMessage
from message_types.ping_message import PingMessage
from message_types.prune_message import PruneMessage
from message_types.join_message import JoinMessage
from message_types.leave_message import LeaveMessage


class Router:
    def __init__(self, rid, numifs, ips, subnets):
        from state.RouterCenter import RouterCenter
        
        self.rid = rid
        self.numifs = numifs
        self.ips = ips
        self.subnets = subnets
        self.routing_table = {}  # Tabela de roteamento
        self.groups = {}
        self.router_center = RouterCenter.get_instance()

    # router building methods
    def add_route(self, netaddr: str, nexthop: str, ifnum: str):
        self.routing_table[netaddr] = (nexthop, ifnum)
        # print(f"Added route {netaddr} -> {nexthop} on router {self.rid}")

    # helper methods
    def get_nextHop_and_interface_from_net_addr(self, netaddr_with_no_mask: str):
        for netaddr, (next_hop, interface) in self.routing_table.items():
            netaddr_with_no_mask, mask = netaddr.split('/')
            if netaddr == netaddr_with_no_mask:
                return next_hop, interface


    #handle message receivals methods

    def receive_from_router(self, package: BaseMessage):        
        match package:
            case FloodMessage():
                self._handle_flood_message(package)
                pass
            case OkMessage():
                print("OkMessage")
                pass
            case PruneMessage():
                print("PruneMessage")
                pass
            case PingMessage():
                print("PingMessage")
                pass
            case JoinMessage():
                pass
            case LeaveMessage():
                pass

    def _handle_flood_message(self, package: FloodMessage):
        # print(f"Router {self.rid} received flood message from {package.origin_adress} to {package.destination_adress}")
        # print(package)
        # #reverse path forwarding
        # origin_address = package.origin_adress
        # origin_net_address = ip_to_network(origin_address)
        # correct_hop_addr_to_origin = self.get_nextHop_and_interface_from_net_addr(origin_net_address)
        # print(correct_hop_addr_to_origin)
        # if ip_to_network(package.get_last_address()) == correct_hop_addr_to_origin:
        #     pass
        # answer and forward

        pass

    def _handle_ok_message(self, package: OkMessage):
        pass

    def _handle_prune_message(self, package: PruneMessage):
        pass

    def _handle_ping_message(self, package: PingMessage):
        pass

    # start flooding

    def start_ping(self, sid: str, mgroupid: str, ping_msg: str ):
        self.start_flood(mgroupid)


    def start_flood(self, mgroupid: str):
        already_flooded_neighbours = []
        for destination_net_address, (next_hop, interface) in self.routing_table.items():
            local_subnet_address = "0.0.0.0"
            if next_hop != local_subnet_address and next_hop not in already_flooded_neighbours:
                next_router_instance = self.router_center.get_router_instance(next_hop)
                this_router_address, mask = self.ips[int(interface)].split('/')
                flood_message = FloodMessage(this_router_address, next_hop, this_router_address, mgroupid)
                already_flooded_neighbours.append(next_hop)
                next_router_instance.receive_from_router(flood_message)
                
 
    # not used methods

    def get_subnet(self, sid):
        return self.subnets[sid]

    def add_subnet_to_group(self, mgroupid: str, subnet_addr: str):
        if mgroupid in self.groups:
            self.groups[mgroupid].append(subnet_addr)
            return
        self.groups[mgroupid] = [subnet_addr]

    def remove_subnet_from_group(self, mgroupid: str, subnet_addr: str):
        self.groups[mgroupid].remove(subnet_addr)