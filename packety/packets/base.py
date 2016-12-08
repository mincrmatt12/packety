import inspect
import struct

from packety.packets.meta_schema import SchemaType

all_packets = {}


class Packet(object):
    packet_id = -1

    def __new__(cls, *args, **kwargs):
        obj = super(Packet, cls).__new__(cls)

        if type(obj) == Packet:
            raise RuntimeError('''You cannot make a raw packets object, you must use a subclass''')

        attribs = inspect.getmembers(obj, lambda a: not inspect.isroutine(a))
        attribs = [x for x in attribs if not (x[0].startswith("__") and x[0].endswith("__"))]
        attribs = [x for x in attribs if isinstance(x[1], SchemaType)]
        schema = []
        schema_names = []
        for i in attribs:
            name, schem = i
            schem.name = name
            schema.append(schem)
            schema_names.append(name)

        for i in schema:
            setattr(obj, i.name, i.default)

        obj.__schema__ = schema
        obj.__schema_names__ = schema_names

        if cls.packet_id < 0:
            raise ValueError('''Packet does not have id or invalid id, cannot create new packets''')

        return obj

    @classmethod
    def register(cls):
        all_packets[cls.packet_id] = cls

    @classmethod
    def unregister(cls):
        del all_packets[cls.packet_id]

    def _read_into_self(self, file_like_object):
        # the packets id and 2 null bytes have already been read by other code

        for value in self.__schema__:
            name = value.name
            returned = value.read_from(file_like_object)
            if value.value_valid(returned) is False:
                raise ValueError('''Invalid data''')
            setattr(self, name, returned)
            file_like_object.read(1)  # discard separator null
        file_like_object.read(2)  # discard end 3 nulls

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            # this means read from a buffer in the first argument
            self._read_into_self(args[0])
        else:
            for kwarg in kwargs:
                if kwarg in self.__schema_names__:
                    setattr(self, kwarg, kwargs[kwarg])

    def write_out(self):
        buf = struct.pack("!Hx", self.packet_id)
        for value in self.__schema__:
            value_data = getattr(self, value.name)
            if not value.value_valid(value.py_type(value_data)):
                raise ValueError("""Invalid value for {}: {}""".format(value.name, value_data))
            buf += value.write_to(value.py_type(value_data))
            buf += bytes("\x00", encoding="ascii")
        buf += bytes("\x00\x00", encoding="ascii")
        return buf


def find_packet_by_id(idx):
    return all_packets[idx]