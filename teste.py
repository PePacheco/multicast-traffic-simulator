from models.router import Router
from message_types.flood_message import FloodMessage
from message_types.ok_message import OkMessage

r1 = Router("1", "idk",["123"], ["123"])

m1 = OkMessage("123", "234", "234", "g1")

r1.receive_from_router(m1)