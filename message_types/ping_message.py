import base_message


#It shows interest in one group only
class PingMessage(base_message.BaseMessage):
    def __init__(self, origin_adress, destination_adress, last_adress, multicast_group, message):
        super().__init__(origin_adress, destination_adress, last_adress)
        self.multicast_group = multicast_group
        self.message = message