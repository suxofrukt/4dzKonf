import unittest
from assembler import assembler

class TestAssembler(unittest.TestCase):

    def test_load_constant(self):
        # Ожидаемая команда: (A=52, B=25, C=791)
        byte_code = assembler([["load", 25, 791]])
        expected_bytes = bytes([0xB4, 0x7C, 0x31, 0x00, 0x00])  # 5 байт
        self.assertEqual(byte_code, list(expected_bytes))

    def test_read_memory(self):
        # Ожидаемая команда: (A=43, B=6, C=30, D=217)
        byte_code = assembler([["read", 6, 30, 217]])
        expected_bytes = bytes([0x2B, 0xE3, 0xB3, 0x01, 0x00])  # 5 байт
        self.assertEqual(byte_code, list(expected_bytes))

    def test_write_memory(self):
        # Ожидаемая команда: (A=25, B=5, C=11)
        byte_code = assembler([["write", 5, 11]])
        expected_bytes = bytes([0x99, 0xB2, 0x00, 0x00, 0x00])  # 5 байт
        self.assertEqual(byte_code, list(expected_bytes))

    def test_popcnt(self):
        # Ожидаемая команда: (A=57, B=23, C=11, D=70)
        byte_code = assembler([["not", 23, 11, 70]])
        expected_bytes = bytes([0xB9, 0xBB, 0x8C, 0x00, 0x00])  # 5 байт
        self.assertEqual(byte_code, list(expected_bytes))

if __name__ == "__main__":
    unittest.main()