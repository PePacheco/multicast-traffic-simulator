from data.SubnetCenter import SubnetCenter

class Logger:
    _instance = None
    subnet_center = SubnetCenter.get_instance()

    origin_subnet_id = ""

    order_of_floods_by_rid = []
    sent_floods_by_rid = {}
    mgroupid_from_floods = ""

    pruned_returns = []

    order_of_pings_by_rid = []
    sent_pings_by_rid = {}
    mgroupid_from_pings = ""

    order_of_pings_to_subnets_by_rid = []
    sent_pings_to_subnets_by_rid = {}
    message = ""

    @staticmethod
    def get_instance():
        if Logger._instance is None:
            Logger._instance = Logger()
        return Logger._instance


    def set_origin_subnet_id(self, origin_subnet_id):
        self.origin_subnet_id = origin_subnet_id

    def print_floods_pings_and_boxes(self):
        self.print_floods()
        self.print_pings()

        self._reset_flood_structure()
        self._reset_prune_structure()
        self._reset_ping_structure()

# join and leave
    

    def join_debug(self, subnet_id: str, router_id: str, mgroupid: str) -> None:
        self.print_floods_pings_and_boxes()
        print(f'{subnet_id} => {router_id} : mjoin {mgroupid};')

    def leave_debug(self, router_id: str, subnet_id: str, mgroupid: str) -> None:
        self.print_floods_pings_and_boxes()
        print(f'{router_id} => {subnet_id} : mleave {mgroupid};')

# prune and flood methods

    def prune_debug(self, sender_id: str, receiver_id: str, mgroupid: str) -> None:
        print(f'{sender_id} >> {receiver_id} : mprune {mgroupid};')

    def append_pruned_return(self, pruned_return: dict) -> None:
        self.pruned_returns.append(pruned_return)

    def _reset_prune_structure(self):
        self.pruned_returns = []

    def _reset_flood_structure(self):
        self.order_of_floods_by_rid = []
        self.sent_floods_by_rid = {}
        self.mgroupid_from_floods = ""

    def router_received_flood_from(self, recipient_rid, sender_ip, mgroupid):
        self.mgroupid_from_floods = mgroupid
        from data.RouterCenter import RouterCenter
        router_center = RouterCenter.get_instance()
        sender_instance = router_center.get_router_instance(sender_ip)
        sender_rid = sender_instance.rid

        if self.sent_floods_by_rid.get(sender_rid) == None:
           self.sent_floods_by_rid[sender_rid] = [recipient_rid]
        else:
            self.sent_floods_by_rid[sender_rid].append(recipient_rid)

        if sender_rid not in self.order_of_floods_by_rid:
            self.order_of_floods_by_rid.append(sender_rid)

    def print_floods(self):
        for sender_rid in self.order_of_floods_by_rid:
            reduced_flood_message = ""
            origin_router = self.order_of_floods_by_rid[0]
            recipient_rids = self.sent_floods_by_rid.get(sender_rid)
            for recipient_rid in recipient_rids:
                if recipient_rid != origin_router:
                    reduced_flood_message += f'{sender_rid} >> {recipient_rid}, '
            if reduced_flood_message != "":
                flooded_group_id_msg = reduced_flood_message.removesuffix(", ")
                group_id_msg = f" : mflood {self.mgroupid_from_floods}"
                print(flooded_group_id_msg + group_id_msg + ";")

        if len(self.pruned_returns) > 0:
            for prune_answer in self.pruned_returns:
                self.prune_debug(prune_answer['pruned_answer'].sender_id, prune_answer['self.rid'], prune_answer['mgroupid'])


# Ping and Box methods

    def box_debug(self, msg: str, mgroupid: str, receiver_subnet_id) -> None:
        origin_router_subnet_id = self.origin_subnet_id
        print(f"{receiver_subnet_id} box {receiver_subnet_id} : {mgroupid}#{msg} from {origin_router_subnet_id};")

    def _reset_ping_structure(self):
        self.order_of_pings_by_rid = []
        self.sent_pings_by_rid = {}
        self.mgroupid_from_pings = ""

        self.order_of_pings_to_subnets_by_rid = []
        self.sent_pings_to_subnets_by_rid = {}
    

    def router_sent_ping_to(self, sender_rid, receiver_rid, mgroupid):
        self.mgroupid_from_pings = mgroupid

        if self.sent_pings_by_rid.get(sender_rid) == None:
            self.sent_pings_by_rid[sender_rid] = [receiver_rid]
        else:
            self.sent_pings_by_rid[sender_rid].append(receiver_rid)

        if sender_rid not in self.order_of_pings_by_rid:
            self.order_of_pings_by_rid.append(sender_rid)

    def received_ping_from_router(self, sender_rid, receiver_sid, message):
        self.message = message

        if self.sent_pings_to_subnets_by_rid.get(sender_rid) == None:
            self.sent_pings_to_subnets_by_rid[sender_rid] = [receiver_sid]
        else:
            self.sent_pings_to_subnets_by_rid[sender_rid].append(receiver_sid)

        if sender_rid not in self.order_of_pings_to_subnets_by_rid:
            self.order_of_pings_to_subnets_by_rid.append(sender_rid)


    def print_pings(self):

        for sender_rid in self.order_of_floods_by_rid:
            reduced_ping_message = ""
            origin_router = self.order_of_floods_by_rid[0]
            recipient_rids = self.sent_pings_by_rid.get(sender_rid)
            if recipient_rids == None:
                self.printRelatedBoxes(sender_rid)
                continue
            for recipient_rid in recipient_rids:
                if recipient_rid != origin_router:
                    reduced_ping_message += f'{sender_rid} =>> {recipient_rid}, '
            if reduced_ping_message != "":
                ping_group_id_msg = reduced_ping_message.removesuffix(", ")
                group_id_msg = f" : mping {self.mgroupid_from_pings}"
                print(ping_group_id_msg + group_id_msg + ";")
                self.printRelatedBoxes(sender_rid)


    def printRelatedBoxes(self, sender_rid):
        if self.sent_pings_to_subnets_by_rid.get(sender_rid) == None:
            return
        
        subnets = self.sent_pings_to_subnets_by_rid[sender_rid]
        for receiver_sid in subnets:
            self.box_debug(self.message, self.mgroupid_from_pings, receiver_sid)