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

  def read_file(self, filename):
    dados = []
    with open(filename, 'r') as arquivo:
        for linha in arquivo:
          dados.append(linha.strip())

    return dados

  def process_topology(self, filename):
    dados = self.read_file(filename)

    index = 0
    print("PROCESSANDO DADOS")
    if dados[0] == '#SUBNET':
      print(dados[index])
      index += 1
      while dados[index] != '#ROUTER':
        sid, netaddr = dados[index].split(',')
        print(sid, netaddr)
        self.subnets[sid] = Subnet(sid, netaddr)
        index += 1
  
    if dados[index] == '#ROUTER':
      print(dados[index])
      index += 1
      while dados[index] != '#ROUTERTABLE':
        parts = dados[index].strip().split(',')
        rid, numifs = parts[0:2]
        print(rid, numifs)
        ips = parts[2:]
        self.routers[rid] = Router(rid, numifs, ips)
        index += 1
  
    if dados[index] == '#ROUTERTABLE':
      print(dados[index])
      index += 1
      while index < len(dados):
        rid, netaddr, nexthop, ifnum = dados[index].strip().split(',')
        print(rid, netaddr, nexthop, ifnum)
        self.routers[rid].add_route(netaddr, nexthop, ifnum)
        index += 1

  def execute_commands(self, filename):
    with open(filename, 'r') as file:
      for line in file:
        command, params = line.strip().split(' ', 1)
        if command == 'mjoin':
          sid, mgroupid = params.split()
          self.MJOIN.run()
        elif command == 'mleave':
          sid, mgroupid = params.split()
          self.MLEAVE.run()
        elif command == 'mping':
          sid, mgroupid, msg = params.split()
          self.MPING.run()
