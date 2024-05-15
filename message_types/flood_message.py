from message_types.base_message import BaseMessage
from dataclasses import dataclass

@dataclass
class FloodMessage(BaseMessage):
    multicast_group: str
