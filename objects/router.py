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

  def receive_from_subnet(self, subnet_id, mgroupid, msg):
      print(f"{subnet_id} =>> {self.rid} : mping {mgroupid} {msg}")
      for sid, subnet in self.subnets.items():
          if sid != subnet_id: # Nao envia para a subnet que recebeu
            subnet.receive_from_router(self.rid, mgroupid, msg)
