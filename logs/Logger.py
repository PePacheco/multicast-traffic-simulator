from data.SubnetCenter import SubnetCenter

class Logger:
    _instance = None
    subnet_center = SubnetCenter.get_instance()

    @staticmethod
    def get_instance():
        if Logger._instance is None:
            Logger._instance = Logger()
        return Logger._instance

    def join_debug(self, subnet_id: str, router_id: str, mgroupid: str) -> None:
        print(f'{subnet_id} => {router_id} : mjoin {mgroupid};')

    def leave_debug(self, router_id: str, subnet_id: str, mgroupid: str) -> None:
        print(f'{router_id} => {subnet_id} : mleave {mgroupid};')

    def flood_debug(self, sender_id: str, receiver_id: str, mgroupid: str) -> None:
        print(f'{sender_id} >> {receiver_id} : mflood {mgroupid};')

    def prune_debug(self, sender_id: str, receiver_id: str, mgroupid: str) -> None:
        print(f'{sender_id} >> {receiver_id} : mprune {mgroupid};')

    def ping_debug(self) -> None:
        pass

    def box_debug(self, msg: str, mgroupid: str, origin_subnet_address: str, receiver_subnet_id) -> None:
        subnet_id = self.subnet_center.get_subnet_id(origin_subnet_address).sid
        print(f"{receiver_subnet_id} box {receiver_subnet_id} : {mgroupid}#{msg} from {subnet_id};")
