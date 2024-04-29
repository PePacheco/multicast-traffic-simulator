class Router:
  def __init__(self, rid, numifs, ips):
      self.rid = rid
      self.numifs = numifs
      self.ips = ips
      self.routing_table = {}  # Tabela de roteamento

  def add_route(self, netaddr, nexthop, ifnum):
      self.routing_table[netaddr] = (nexthop, ifnum)