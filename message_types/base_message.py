class BaseMessage:
    def __init__(self, origin_adress, destination_adress, last_adress):
        self.origin_adress = origin_adress
        self.destination_adress = destination_adress
        self.last_adress = last_adress

    def get_origin_adress(self):
        return self.origin_adress
    
    def get_destination_adress(self):
        return self.destination_adress
    
    def get_last_adress(self):
        return self.last_adress