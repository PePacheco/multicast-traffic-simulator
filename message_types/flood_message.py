import base_message


class FloodMessage(base_message.BaseMessage):
    def __init__(self, origin_adress, destination_adress, last_adress, multicastg_group):
        super().__init__(origin_adress, destination_adress, last_adress)
        self.multicastg_group = multicastg_group