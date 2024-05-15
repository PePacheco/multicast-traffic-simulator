from dataclasses import dataclass


@dataclass
class BaseMessage:
    origin_adress: str
    destination_adress: str
    last_adress: str

    def get_origin_adress(self):
        return self.origin_adress

    def get_destination_adress(self):
        return self.destination_adress

    def get_last_adress(self):
        return self.last_adress