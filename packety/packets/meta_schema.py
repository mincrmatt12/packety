import struct


class SchemaType:
    py_type = type(None)

    def __init__(self, default=None):
        self.name = ""
        self.default = self.py_type(default) if default is not None else self.py_type()

    def read_from(self, file_like):
        pass

    def write_to(self, val):
        pass

    def value_valid(self, val):
        return True


class SchemaList(SchemaType):
    py_type = list

    def __init__(self, child_type, default=None):
        super().__init__(default=default)
        self.child_type = child_type

    def read_from(self, file_like):
        length = struct.unpack("!H", file_like.read(2))[0]
        my_value = []
        for index in range(length):
            my_value.append(self.child_type.read_from(file_like))
            file_like.read(1)
        return my_value

    def write_to(self, val):
        buf = struct.pack("!H", len(val))
        for value in val:
            buf += self.child_type.write_to(value)
            buf += b'\x00'
        return buf

    def value_valid(self, val):
        return len(val) < 32768 and all((type(x) == self.child_type.py_type for x in val)) and \
            all((self.child_type.value_valid(x) for x in val))