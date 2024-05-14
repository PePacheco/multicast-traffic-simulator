import base_message

class JoinMessage(base_message.BaseMessage):
    def __init__(self, origin_adress, destination_adress, last_adress, subgroup_adress, multicast_group):
        super().__init__(origin_adress, destination_adress, last_adress)
        self.subgroup_adress = subgroup_adress
        self.multicast_group = multicast_group
