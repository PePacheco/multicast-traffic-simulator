from dataclasses import dataclass


@dataclass
class BaseMessage:
    origin_adress: str
    destination_adress: str
    last_address: str

    def get_origin_adress(self):
        return self.origin_adress

    def get_destination_adress(self):
        return self.destination_adress

    def get_last_address(self):
        return self.last_address