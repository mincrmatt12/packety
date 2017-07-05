from packety.packets.schema import UnsignedByte

from packety.packets import Packet
from packety.server import BaseConnection, Server


class TestP(Packet):
    packet_id = 1

    a = UnsignedByte()
TestP.register()

class BC(BaseConnection):
    def run(self):
        a = self.incoming.get()
        if a.a == 5:
            print("yay")
            self.outgoing.put(TestP(a=3))
        else:
            self.sock.close()
            self.kill()

s = Server(port=12342, conn_type=BC)
s.run_blocking()