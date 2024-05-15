from message_types.base_message import BaseMessage
from dataclasses import dataclass

@dataclass
class PruneMessage(BaseMessage):
    multicast_group: str
