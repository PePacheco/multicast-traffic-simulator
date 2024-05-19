
from helpers.ip import ip_in_same_subnet
from message_types.base_message import BaseMessage
from message_types.flood_message import FloodMessage
from message_types.ok_message import OkMessage
from message_types.ping_message import PingMessage
from message_types.prune_message import PruneMessage
from message_types.join_message import JoinMessage
from message_types.leave_message import LeaveMessage


class Router:
    def __init__(self, rid, numifs, ips, subnets):
        from data.RouterCenter import RouterCenter
        from logs.Logger import Logger
        self.rid = rid
        self.numifs = numifs
        self.ips = ips
        self.subnets = subnets
        self.routing_table = {}  # Tabela de roteamento
        self.groups = {}
        self.router_center = RouterCenter.get_instance()
        self.logger = Logger.get_instance()


    # router building methods
    def add_route(self, netaddr: str, nexthop: str, ifnum: str):
        self.routing_table[netaddr] = (nexthop, ifnum)

    # helper methods

    def get_nextHop_and_interface_from_net_addr(self, destaddr_with_no_mask: str):
        for netaddr, (next_hop, interface) in self.routing_table.items():
            if ip_in_same_subnet(destaddr_with_no_mask, netaddr):
                return next_hop, interface

        return None # it might not find it as a destiny

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
        #reverse path forwarding
        origin_address = package.origin_adress
        correct_hop_addr_to_origin, interface = self.routing_table[origin_address]
        if package.get_last_address() == correct_hop_addr_to_origin:
            #flood here
            self.start_flood(package.multicast_group, package.origin_adress)

    def _handle_ok_message(self, package: OkMessage):
        pass

    def _handle_prune_message(self, package: PruneMessage):
        pass

    def _handle_ping_message(self, package: PingMessage):
        pass

    # start flooding

    def start_ping(self, sid: str , mgroupid: str, ping_msg: str ):
        subnet_instance = self.subnets[sid]
        origin_subnet_address = subnet_instance.netaddr
        self.start_flood(mgroupid, origin_subnet_address)


    def start_flood(self, mgroupid: str, origin_subnet_address: str):
        already_flooded_neighbours = []
        for destination_net_address, (next_hop, interface) in self.routing_table.items():
            local_subnet_address = "0.0.0.0"
            next_router_instance = self.router_center.get_router_instance(next_hop)
            if (next_hop != local_subnet_address) and (next_hop not in already_flooded_neighbours):
                this_router_address, mask = self.ips[int(interface)].split('/')
                flood_message = FloodMessage(origin_subnet_address, next_hop, this_router_address, mgroupid)
                already_flooded_neighbours.append(next_hop)
                next_router_instance.receive_from_router(flood_message)
    # not used methods

    def get_subnet(self, sid):
        return self.subnets[sid]

    def add_subnet_to_group(self, mgroupid: str, subnet_addr: str, subnet_id: str):
        self.logger.join_debug(subnet_id, self.rid, mgroupid)
        if mgroupid in self.groups:
            self.groups[mgroupid].append(subnet_addr)
            return
        self.groups[mgroupid] = [subnet_addr]

    def remove_subnet_from_group(self, mgroupid: str, subnet_addr: str, subnet_id: str):
        self.logger.leave_debug(self.rid, subnet_id, mgroupid)
        self.groups[mgroupid].remove(subnet_addr)
