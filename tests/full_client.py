from gevent.socket import create_connection

from packety.client import SimpleClient
from packety.packets import Packet

from packety.packets.schema import UnsignedByte


class TestP(Packet):
    packet_id = 1

    a = UnsignedByte()
TestP.register()

c = SimpleClient(create_connection(("localhost", 12342)))
c.send(TestP(a=5))
print(c.read().a)