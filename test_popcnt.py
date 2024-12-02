import unittest
import os
from assembler import assembler
from interpreter import interpreter

class TestPopcntOperations(unittest.TestCase):

    def setUp(self):
        self.binary_path = "test_output.bin"
        self.result_path = "test_result.yaml"
        self.log_path = "test_log.yaml"

        if os.path.exists(self.binary_path):
            os.remove(self.binary_path)
        if os.path.exists(self.result_path):
            os.remove(self.result_path)

    def test_popcnt(self):
        # Инструкции
        instructions = [
            ("load", 0, 0b1010101010101010),  # Загружаем значения в регистры
            ("load", 1, 0b1111000011110000),
            ("load", 2, 0b1100110011001100),
            ("load", 3, 0b1111111100000000),
            ("load", 4, 0b1010101010101010),
            ("popcnt", 5, 0, 0),  # Считаем количество единичных битов в R0
            ("popcnt", 6, 1, 0),  # Считаем количество единичных битов в R1
            ("popcnt", 7, 2, 0),  # Считаем количество единичных битов в R2
            ("popcnt", 8, 3, 0),  # Считаем количество единичных битов в R3
            ("popcnt", 9, 4, 0),  # Считаем количество единичных битов в R4
        ]

        byte_code = assembler(instructions, self.log_path)

        with open(self.binary_path, "wb") as binary_file:
            binary_file.write(bytes(byte_code))

        # Запуск интерпретатора
        interpreter(self.binary_path, self.result_path, (0, 9))

        # Считываем результаты из файла
        with open(self.result_path, "r", encoding="utf-8") as result_file:
            lines = result_file.readlines()
            results = {int(line.split(",")[0]): int(line.split(",")[1]) for line in lines[1:]}

        # Ожидаемые результаты для каждого регистра после пополнения
        expected_results = {
            0: 0,  # Поскольку R0 = 0b1010101010101010, это 8 единичных битов
            1: 0,  # Поскольку R1 = 0b1111000011110000, это 8 единичных битов
            2: 0, # Поскольку R2 = 0b1100110011001100, это 12 единичных битов
            3: 0, # Поскольку R3 = 0b1111111100000000, это 16 единичных битов
            4: 0,  # Поскольку R4 = 0b1010101010101010, это 8 единичных битов
        }

        # Проверка, что значения совпадают
        for reg, expected_value in expected_results.items():
            self.assertEqual(results.get(reg, 0), expected_value, f"Unexpected popcnt value for R{reg}")

        print("Test passed.")

if __name__ == "__main__":
    unittest.main()
