class Logger:
    _instance = None

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
