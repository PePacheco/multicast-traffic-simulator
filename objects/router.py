class Router:
  def __init__(self, rid, numifs, ips, subnets):
      self.rid = rid
      self.numifs = numifs
      self.ips = ips
      self.subnets = subnets
      self.routing_table = {}  # Tabela de roteamento

  def add_route(self, netaddr, nexthop, ifnum):
      self.routing_table[netaddr] = (nexthop, ifnum)

  def get_subnet(self, sid):
      return self.subnets[sid]