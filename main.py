from objects.multicastSimulator import MulticastSimulator

simulator = MulticastSimulator()

if __name__ == "__main__":
  simulator.process_topology('topology.txt')
  #simulator.execute_commands('commands.txt')
