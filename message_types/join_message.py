import base_message

class JoinMessage(base_message.BaseMessage):
    def __init__(self, origin_adress, destination_adress, last_adress, subgroup_adress, multicastg_group):
        super().__init__(origin_adress, destination_adress, last_adress)
        self.subgroup_adress = subgroup_adress
        self.multicastg_group = multicastg_group
