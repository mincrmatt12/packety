from .meta_schema import SchemaType
import struct


class UnsignedInt(SchemaType):
    py_type = int

    def read_from(self, file_like):
        return struct.unpack("!I", file_like.read(4))[0]

    def write_to(self, val):
        return struct.pack("!I", val)

    def value_valid(self, val):
        return 0 <= val < 4294967296


class SignedInt(SchemaType):
    py_type = int

    def read_from(self, file_like):
        return struct.unpack("!i", file_like.read(4))[0]

    def write_to(self, val):
        return struct.pack("!i", val)

    def value_valid(self, val):
        return -2147483648 <= val < 2147483648


class String(SchemaType):
    py_type = str

    def __init__(self, default=None, validators=None, max_len=-1):
        super().__init__(default=default, validators=validators)
        self.max_len = min(max_len, 32768)
        if self.max_len != -1 and self.max_len <= 0:
            raise ValueError('''max_len cannot be less than or equal to zero 0''')

    def read_from(self, file_like):
        str_length = struct.unpack("!H", file_like.read(2))[0]
        data = file_like.read(str_length).decode("utf-8")
        return data

    def write_to(self, val):
        raw = val.encode("utf-8")
        length = len(raw)
        base = struct.pack("!H", length)
        base += raw
        return base

    def value_valid(self, val):
        return len(val) < 32768 if self.max_len == -1 else self.max_len


class Boolean(SchemaType):
    py_type = bool

    def read_from(self, file_like):
        return file_like.read(1) == b"\x01"

    def write_to(self, val):
        return b"\x01" if val else b"\x00"

    def value_valid(self, val):
        return True


class UnsignedByte(SchemaType):
    py_type = int

    def read_from(self, file_like):
        return ord(file_like.read(1))

    def write_to(self, val):
        return struct.pack("!B", val)

    def value_valid(self, val):
        return 0 <= val < 256


class Byte(SchemaType):
    py_type = int

    def read_from(self, file_like):
        return struct.unpack("!b", file_like.read(1))[0]

    def write_to(self, val):
        return struct.pack("!b", val)

    def value_valid(self, val):
        return -128 <= val < 128
