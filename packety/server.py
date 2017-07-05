import struct

import gevent
from gevent import socket
from gevent.pool import Pool
from gevent.queue import Queue
from gevent.server import StreamServer

from . import packets, client


def block_read_packet(sck):
    dat = sck.recv(3)
    idx = struct.unpack("!Hx", dat)[0]
    pack = packets.find_packet_by_id(idx)(sck.makefile("rb"))
    return pack


class PacketReader:
    def __init__(self, outgoing_packets, sock, parent):
        self.buf = outgoing_packets
        self.sock = sock
        self.parent = parent

    def run(self):
        while True:
            try:
                pack = block_read_packet(self.sock)
            except (struct.error, ConnectionResetError):
                self.parent.kill() # socket was closed or something of that nature.
            else:
                self.buf.put(pack)


class PacketWriter:
    def __init__(self, incoming_packets, sock):
        self.buf = incoming_packets
        self.sock = sock.makefile("wb")

    def run(self):
        while True:
            outgoing = self.buf.get() # type: packets.Packet
            self.sock.write(outgoing.write_out())


class BaseConnection:
    def __init__(self, sock):
        self.sock = sock
        self.outgoing = Queue()
        self.incoming = Queue()

        self.packet_reader = PacketReader(self.incoming, self.sock, self)
        self.packet_writer = PacketWriter(self.outgoing, self.sock)
        self.greenlets = []

    def on_start(self):
        pass

    def run(self):
        pass

    def on_close(self):
        pass

    def kill(self):
        for let in self.greenlets:
            let.kill()
        self.on_close()

    def start(self):
        self.on_start()
        me, write, read = gevent.spawn(self.run), gevent.spawn(self.packet_reader.run), gevent.spawn(self.packet_writer.run)
        self.greenlets = [me, write, read]
        gevent.joinall([me, write, read])


class Server:
    def __init__(self, host="localhost", port=0, conn_type=BaseConnection, on_new_conn=lambda x: None, max_clients=None):
        self.host = host
        self.port = port
        self.server = StreamServer((host, port), self.new_conn, spawn=Pool(max_clients))
        self.outgoing_events = Queue()
        self.conn_type = conn_type

        self.connections = []
        self.on_new_conn = on_new_conn

    def new_conn(self, socket_, client_addr):
        connection = self.conn_type(socket_)
        self.connections.append(connection)
        self.on_new_conn(connection)
        connection.start()

    def run_blocking(self):
        self.server.serve_forever()

    def run(self):
        self.server.start()
        self.port = self.server.server_port
        self.host = self.server.server_host

    def stop(self):
        self.server.stop()


class SimpleServer:
    def __init__(self, host="localhost", port=12355, backlog=5):
        self.sock = gevent.socket.socket()
        self.sock.bind((host, port))
        self.sock.listen(backlog)

    def accept(self):
        sock, addr = self.sock.accept()
        return client.SimpleClient(sock), addr

    def close(self):
        self.sock.close()