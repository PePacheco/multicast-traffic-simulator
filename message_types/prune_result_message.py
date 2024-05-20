from message_types.base_message import BaseMessage
from dataclasses import dataclass


@dataclass
class PruneResultMessage(BaseMessage):
    multicast_group: set[str]