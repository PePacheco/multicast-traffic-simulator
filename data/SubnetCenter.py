class SubnetCenter:
    _instance = None
    subnets = {}

    @staticmethod
    def get_instance():
        if SubnetCenter._instance is None:
            SubnetCenter._instance = SubnetCenter()
        return SubnetCenter._instance
    
    def add_subnet(self, subnet):
        self.subnets[subnet.netaddr] = subnet

    def get_subnet_id(self, subnet_address):
        subnet = self.subnets.get(subnet_address)
        if subnet is None:
            return None
        return subnet.sid