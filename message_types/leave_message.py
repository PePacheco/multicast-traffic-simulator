from message_types.base_message import BaseMessage
from dataclasses import dataclass

@dataclass
class LeaveMessage(BaseMessage):
    subgroup_adress: str
    multicast_group: str
