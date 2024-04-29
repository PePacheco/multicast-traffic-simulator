from objects.multicastSimulator import MulticastSimulator
from sys import argv

simulator = MulticastSimulator()

if __name__ == "__main__":
  topology, commands = argv[1:3]
  print (topology, commands)
  simulator.process_topology(topology)
  simulator.execute_commands(commands)
