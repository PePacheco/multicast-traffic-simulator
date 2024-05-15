from message_types.base_message import BaseMessage
from dataclasses import dataclass

@dataclass
class PingMessage(BaseMessage):
    multicast_group: str
    message: str
