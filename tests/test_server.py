import unittest
from packety import packets
from packety import server
from packety import client
from gevent.socket import create_connection
from gevent.lock import Semaphore


class SimpleServerTestCase(unittest.TestCase):
    def setUp(self):
        class TestPacket(packets.Packet):
            packet_id = 1

            m_byte = packets.schema.UnsignedByte()
        self.p_type = TestPacket
        TestPacket.register()

    def tearDown(self):
        self.p_type.unregister()

    def test_connect_disconnect(self):
        my_server = server.Server(host="0.0.0.0")
        my_server.run()
        a = client.SimpleClient(create_connection(("localhost", my_server.port)))

        a.close()
        my_server.stop()

    def test_connect_send(self):
        p = None

        class Conn(server.BaseConnection):
            def __init__(self, sock):
                super().__init__(sock)

            def run(self):
                nonlocal p
                pack = self.incoming.get()
                t.release()
                p = pack
                self.kill()

        my_server = server.Server(host="0.0.0.0", conn_type=Conn)
        my_server.run()
        t = Semaphore(value=0)
        a = client.SimpleClient(create_connection(("localhost", my_server.port)))
        a.send(self.p_type(m_byte=232))
        a.close()
        t.acquire()
        self.assertEqual(p.__class__, self.p_type)
        self.assertEqual(p.m_byte, 232)
        my_server.stop()

if __name__ == '__main__':
    unittest.main()
