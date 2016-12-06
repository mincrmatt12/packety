import struct

from packety import packets


class SimpleClient:
    def __init__(self, sock):
        self.sock = sock
        self.sock_file = sock.makefile("rb")

    def read(self):
        from_file = self.sock_file
        try:
            idx = struct.unpack("!Hx", from_file.read(3))[0]
            pack = packets.find_packet_by_id(idx)(from_file)
            return pack
        except struct.error:
            return None

    def send(self, pack):
        self.sock.send(pack.write_out())

    def close(self):
        self.sock.close()
