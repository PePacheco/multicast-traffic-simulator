from objects.router import Router
from objects.subnet import Subnet
from commands import mjoin, mleave, mping


class MulticastSimulator:

  def __init__(self):
    self.subnets = {}
    self.routers = {}
    self.MJOIN = mjoin.M_JOIN()
    self.MPING = mping.M_PING()
    self.MLEAVE = mleave.M_LEAVE()

  def verify_subnet(self, endereco_ip, subnet):
    # Separando o endereço IP e a máscara de sub-rede
      ip, mascara = subnet.split('/')

      # Verificando se os primeiros octetos são iguais
      ip_octetos = endereco_ip.split('.')
      subnet_octetos = ip.split('.')

      for i in range(0,3):
          if ip_octetos[i] != subnet_octetos[i]:
              return False
      return True

  def define_router_subnets(self, ips):
    subnets = {}

    for ip in ips:
      for sid, subnet in self.subnets.items():
        if self.verify_subnet(subnet.netaddr, ip):
          subnets[sid] = subnet

    return subnets

  def get_router_by_subnet(self, sid):
    for rid, router in self.routers.items():
      if router.subnets[sid]:
        return router
    return False

  def read_file(self, filename):
    dados = []
    with open(filename, 'r') as arquivo:
        for linha in arquivo:
          dados.append(linha.strip())

    return dados

  def process_subnets(self, index, data):
    if data[0] == '#SUBNET':
      index += 1
      while data[index] != '#ROUTER':
        sid, netaddr = data[index].split(',')
        self.subnets[sid] = Subnet(sid, netaddr)
        index += 1
    return index

  def process_routers(self, index, data):
    if data[index] == '#ROUTER':
      index += 1
      while data[index] != '#ROUTERTABLE':
        parts = data[index].strip().split(',')
        rid, numifs = parts[0:2]
        ips = parts[2:]
        subnets = self.define_router_subnets(ips)
        self.routers[rid] = Router(rid, numifs, ips, subnets)
        index += 1
    return index

  def process_routers_table(self, index, data):
    if data[index] == '#ROUTERTABLE':
      index += 1
      while index < len(data):
        rid, netaddr, nexthop, ifnum = data[index].strip().split(',')
        self.routers[rid].add_route(netaddr, nexthop, ifnum)
        index += 1

  def process_topology(self, filename):
    data = self.read_file(filename)

    index = self.process_subnets(0, data)
    index = self.process_routers(index, data)
    self.process_routers_table(index, data)

  def execute_commands(self, filename):
    with open(filename, 'r') as file:
      for line in file:
        command, params = line.strip().split(' ', 1)

        # Executando o comando mjoin
        if command == 'mjoin':
          sid, mgroupid = params.split()
          router = self.get_router_by_subnet(sid)
          if router:
            self.MJOIN.run(sid, mgroupid, router)

        elif command == 'mleave':
          sid, mgroupid = params.split()
          router = self.get_router_by_subnet(sid)
          if router:
            self.MLEAVE.run(sid, mgroupid, router)
        elif command == 'mping':
          sid, mgroupid, msg = params.split()
          self.MPING.run()
