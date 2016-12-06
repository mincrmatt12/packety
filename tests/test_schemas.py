import unittest
from io import BytesIO

from packety.packets.meta_schema import SchemaList
from packety.packets.schema import Boolean, String, UnsignedInt, SignedInt, UnsignedByte, Byte


class BaseSchemaTestCase(object):
    py_obj = None
    in_data = b''
    invalid_obj = None
    invalid_objs = None

    def create_schema(self):
        return None

    @classmethod
    def setUpClass(cls):
        if cls is not BaseSchemaTestCase and cls.setUp is not BaseSchemaTestCase.setUp:
            cls.setUp = BaseSchemaTestCase.setUp

    def setUp(self):
        self.schema = self.create_schema()

    def test_encode(self):
        self.assertEqual(self.in_data, self.schema.write_to(self.py_obj))
        self.assertTrue(self.schema.value_valid(self.py_obj))

    def test_decode(self):
        self.assertEqual(self.schema.read_from(BytesIO(self.in_data)), self.py_obj)

    def test_invalid(self):
        if self.invalid_obj is None and self.invalid_objs is None:
            pass
        elif self.invalid_obj is None:
            for i in self.invalid_objs:
                self.assertFalse(self.schema.value_valid(i), '''error in {}'''.format(repr(i)))
        else:
            self.assertFalse(self.schema.value_valid(self.invalid_obj))


class TestSchemaBool(BaseSchemaTestCase, unittest.TestCase):
    py_obj = True
    in_data = b'\x01'
    invalid_obj = None

    def create_schema(self):
        return Boolean()


class TestSchemaString(BaseSchemaTestCase, unittest.TestCase):
    py_obj = "test"
    in_data = b'\x00\x04test'
    invalid_obj = ("B" * 32790)  # can only use strings with len() < 32768

    def create_schema(self):
        return String()


class TestSchemaUInt(BaseSchemaTestCase, unittest.TestCase):
    py_obj = 2146483680
    in_data = b'\x7f\xf0\xbd\xe0'
    invalid_obj = 4294967296

    def create_schema(self):
        return UnsignedInt()


class TestSchemaSignedInt(BaseSchemaTestCase, unittest.TestCase):
    py_obj = 12345
    in_data = b'\x00\x0009'
    invalid_obj = 2147483649

    def create_schema(self):
        return SignedInt()


class TestSchemaUByte(BaseSchemaTestCase, unittest.TestCase):
    py_obj = 253
    in_data = b'\xfd'
    invalid_obj = 256

    def create_schema(self):
        return UnsignedByte()


class TestSchemaByte(BaseSchemaTestCase, unittest.TestCase):
    py_obj = 122
    in_data = b'z'
    invalid_obj = 256

    def create_schema(self):
        return Byte()


class TestSchemaListString(BaseSchemaTestCase, unittest.TestCase):
    py_obj = ["abcde", "fgh", "defg", "bcda", "bobo", "bablabl123", "YAY"]
    in_data = b'\x00\x07\x00\x05abcde\x00\x00\x03fgh\x00\x00\x04defg\x00\x00\x04bcda\x00\x00\x04bobo\x00\x00\nbablabl123\x00\x00\x03YAY\x00'
    invalid_obj = [123, 456]

    def create_schema(self):
        return SchemaList(String())


class TestSchemaListInt(BaseSchemaTestCase, unittest.TestCase):
    py_obj = [123, 456]
    in_data = b'\x00\x02\x00\x00\x00{\x00\x00\x00\x01\xc8\x00'
    invalid_objs = ["abcde", "fgh", "defg", "bcda", "bobo", "bablabl123", "YAY"], [0.4], ["m"]*32769

    def create_schema(self):
        return SchemaList(SignedInt())


if __name__ == '__main__':
    unittest.main()
