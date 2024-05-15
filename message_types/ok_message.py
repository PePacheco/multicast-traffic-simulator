from message_types.base_message import BaseMessage
from dataclasses import dataclass

#It shows interest in one group only
@dataclass
class OkMessage(BaseMessage):
    multicast_group: str