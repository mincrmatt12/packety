import unittest

from io import BytesIO
from packety import packets


class SimplePacketTestCase(unittest.TestCase):
    def setUp(self):
        class TestPacket(packets.Packet):
            packet_id = 1

            m_byte = packets.schema.Byte()
        self.p_type = TestPacket
        TestPacket.register()

    def tearDown(self):
        self.p_type.unregister()

    def test_creation(self):
        my_packet = self.p_type()
        my_packet.m_byte = 4
        self.assertEqual(my_packet.m_byte, 4)

    def test_serialize(self):
        good = b'\x00\x01\x00\x04\x00\x00\x00'
        my_packet = self.p_type()
        my_packet.m_byte = 4
        self.assertEqual(my_packet.write_out(), good)

    def test_deserialize(self):
        good = BytesIO(b'\x04\x00\x00\x00')
        n_packet = packets.find_packet_by_id(1)(good)
        self.assertEqual(n_packet.m_byte, 4)


if __name__ == '__main__':
    unittest.main()
