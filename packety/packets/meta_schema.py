import struct

from io import BytesIO


class SchemaType:
    py_type = type(None)

    def __init__(self, default=None, validators=None):
        if validators is None:
            validators = []
        self.name = ""
        self.default = self.py_type(default) if default is not None else self.py_type()
        self.validators = validators

    def read_from(self, file_like):
        pass

    def write_to(self, val):
        pass

    def read_from_file(self, file_like):
        return self.read_from(file_like)

    def read_from_bytes(self, bytes_):
        return self.read_from(BytesIO(bytes_))

    def valid(self, value):
        """

        :rtype: bool
        """
        for validator in self.validators:
            if not validator.valid(value):
                return False
        if self.value_valid(value):
            return True

    def value_valid(self, val):
        return True


class SchemaList(SchemaType):
    py_type = list

    def __init__(self, child_type, default=None, validators=[]):
        super().__init__(default=default, validators=validators)
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