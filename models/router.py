from state.RouterCenter import RouterCenter
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


    def receive_from_router(self, package: BaseMessage):
        match package:
            case FloodMessage():
                print("FloodMessage")
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