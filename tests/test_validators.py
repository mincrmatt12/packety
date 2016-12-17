from io import BytesIO
from unittest import TestCase

from packety import packets
from packety.packets.validate import Longer, LengthInRange, Greater, Smaller, Not, IsOneOf, All


class TestPacketValidator(TestCase):
    def test_validator_length(self):
        class PacketLongth(packets.Packet):
            packet_id = 1

            str_test = packets.schema.String(validators=[Longer(2)])
            str_test_2 = packets.schema.String(validators=[LengthInRange(1, 8)])

        PacketLongth.register()

        m = PacketLongth()
        m.str_test = "a"
        m.str_test_2 = "ccccccccccc"
        failed = False
        try:
            out = m.write_out()
            failed = True
        except ValueError:
            m.str_test = "bbb"
            m.str_test_2 = "baba"
            try:
                out = m.write_out()
            except ValueError:
                failed = True
        PacketLongth.unregister()
        if failed:
            self.fail()

    def test_validator_numerical(self):
        class PacketLongth(packets.Packet):
            packet_id = 1

            byte_test = packets.schema.UnsignedByte(validators=[Greater(122, or_equal=True)])
            int_test = packets.schema.SignedInt(validators=[Smaller(24328)])

        PacketLongth.register()

        m = PacketLongth()
        m.byte_test = 100
        m.int_test = 250000
        failed = False
        try:
            out = m.write_out()
            failed = True
        except ValueError:
            m.byte_test = 234
            m.int_test = -25
            try:
                out = m.write_out()
            except ValueError:
                failed = True
        PacketLongth.unregister()
        if failed:
            self.fail()


class TestIsolated(TestCase):
    def test_not(self):
        my_validator = Not(Greater(234))
        my_other_validator = Not(Longer(4))

        self.assertFalse(my_validator.valid(555))
        self.assertFalse(my_other_validator.valid("abcdefg"))
        self.assertTrue(my_validator.valid(111))
        self.assertTrue(my_other_validator.valid("abc"))

    def test_all(self):
        my_validator = All(Not(IsOneOf([1, 5, 8, 9])), Smaller(40))

        self.assertTrue(my_validator.valid(4))
        self.assertTrue(my_validator.valid(12))
        self.assertFalse(my_validator.valid(5))
        self.assertFalse(my_validator.valid(8))
        self.assertFalse(my_validator.valid(42))
