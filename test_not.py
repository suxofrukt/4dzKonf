import unittest
import os
from assembler import assemble, save_to_bin
from interpreter import interpreter

class TestNotOperation(unittest.TestCase):
    def setUp(self):
        self.instructions_path = "test_instructions.txt"
        self.binary_path = "test_program.bin"
        self.result_path = "test_result.csv"
        self.log_path = "test_log.yaml"

        # Инструкции для теста
        instructions = [
            ["load", 0, 10],   # R0 = 10 (адрес начала исходного вектора)
            ["load", 1, 20],   # R1 = 20 (адрес начала результирующего вектора)
            # Инициализация исходного вектора в памяти по адресам 10-14
            ["load", 2, 0b0001],
            ["write", 2, 10],
            ["load", 2, 0b0010],
            ["write", 2, 11],
            ["load", 2, 0b0011],
            ["write", 2, 12],
            ["load", 2, 0b0100],
            ["write", 2, 13],
            ["load", 2, 0b0101],
            ["write", 2, 14],
            # Выполнение операции not для каждого элемента
            ["not", 1, 0, 0],  # Mem[R1 + 0] = ~Mem[R0]
            ["not", 1, 0, 1],  # Mem[R1 + 1] = ~Mem[R0 + 1]
            ["not", 1, 0, 2],  # Mem[R1 + 2] = ~Mem[R0 + 2]
            ["not", 1, 0, 3],  # Mem[R1 + 3] = ~Mem[R0 + 3]
            ["not", 1, 0, 4],  # Mem[R1 + 4] = ~Mem[R0 + 4]
        ]

        # Запись инструкций в файл
        with open(self.instructions_path, "w", encoding="utf-8") as f:
            for instr in instructions:
                f.write(" ".join(map(str, instr)) + "\n")

        # Ассемблирование инструкций
        assembled_code = assemble(self.instructions_path, self.log_path)
        save_to_bin(assembled_code, self.binary_path)

    def test_not_operation(self):
        # Выполнение интерпретатора
        interpreter(self.binary_path, self.result_path, (20, 24))  # Проверяем память с 20 по 24

        # Чтение результатов из файла
        with open(self.result_path, "r", encoding="utf-8") as result_file:
            lines = result_file.readlines()
            results = {int(line.split(",")[0]): int(line.split(",")[1]) for line in lines[1:]}

        # Ожидаемые результаты (побитовое "не" от исходных значений)
        expected_values = {
            20: ~0b0001 & 0xFFFFFFFF,
            21: ~0b0010 & 0xFFFFFFFF,
            22: ~0b0011 & 0xFFFFFFFF,
            23: ~0b0100 & 0xFFFFFFFF,
            24: ~0b0101 & 0xFFFFFFFF,
        }

        for address, expected_value in expected_values.items():
            self.assertEqual(results.get(address, None), expected_value, f"Ошибка на адресе {address}")

    def tearDown(self):
        # Удаление временных файлов
        os.remove(self.instructions_path)
        os.remove(self.binary_path)
        os.remove(self.result_path)
        os.remove(self.log_path)

if __name__ == "__main__":
    unittest.main()
