import argparse


def interpreter(binary_path, result_path, memory_range):
    # Инициализация памяти и регистров
    memory = [0] * 100  # Увеличим количество ячеек памяти до 100
    registers = [0] * 32  # 32 регистра

    # Чтение бинарного файла
    with open(binary_path, "rb") as binary_file:
        byte_code = binary_file.read()

    i = 0
    while i < len(byte_code):
        command = byte_code[i] & 0x7F  # Биты 0-6 для команды

        if command == 52:  # Загрузка константы
            B = (int.from_bytes(byte_code[i:i + 5], "little") >> 7) & 0x1F  # Регистр
            C = (int.from_bytes(byte_code[i:i + 5], "little") >> 12) & 0xFFF  # Константа
            if 0 <= B < len(registers):
                registers[B] = C

        elif command == 43:  # Чтение из памяти
            B = (int.from_bytes(byte_code[i:i + 5], "little") >> 7) & 0x1F  # Регистр для хранения
            C = (int.from_bytes(byte_code[i:i + 5], "little") >> 12) & 0x1F  # Регистр с адресом
            D = (int.from_bytes(byte_code[i:i + 5], "little") >> 17) & 0xFFFF  # Смещение

            if 0 <= C < len(registers):  # Проверка регистра
                if registers[C] == 0:
                    memory_address = D
                else:
                    memory_address = registers[C] + D
                if 0 <= memory_address < len(memory):
                    registers[B] = memory[memory_address]

        elif command == 25:  # Запись в память
            B = (int.from_bytes(byte_code[i:i + 5], "little") >> 7) & 0x1F
            C = (int.from_bytes(byte_code[i:i + 5], "little") >> 12) & 0x3F
            if 0 <= B < len(registers) and 0 <= C < len(memory):
                memory[C] = registers[B]
            else:
                print(f"Ошибка: Неверный индекс памяти или регистра B={B}, C={C}")



        elif command == 57:  # Побитовое "не"
            B = (int.from_bytes(byte_code[i:i + 5], "little") >> 7) & 0x1F
            C = (int.from_bytes(byte_code[i:i + 5], "little") >> 12) & 0x1F
            D = (int.from_bytes(byte_code[i:i + 5], "little") >> 17) & 0xFFFF
            if 0 <= B < len(registers) and 0 <= C < len(registers):
                source_address = registers[C] + D
                destination_address = registers[B] + D
                if 0 <= source_address < len(memory) and 0 <= destination_address < len(memory):
                    value = memory[source_address]
                    result = ~value & 0xFFFFFFFF
                    memory[destination_address] = result
                    print(f"Bitwise NOT: Mem[{destination_address}] = ~Mem[{source_address}]")
                else:
                    print(f"Ошибка: Адреса {source_address} или {destination_address} выходят за пределы памяти.")
            else:
                print(f"Ошибка: Неверный индекс регистра B={B} или C={C}")

        i += 5

    # Сохранение результата в файл
    with open(result_path, "w", encoding="utf-8") as result_file:
        result_file.write("Address,Value\n")
        for address in range(memory_range[0], memory_range[1] + 1):
            if 0 <= address < len(memory):
                result_file.write(f"{address},{memory[address]}\n")

    print("Интерпретатор завершил работу успешно.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Interpreting the bytes like instructions (from binary file) to the csv-table.")
    parser.add_argument("binary_path", help="Path to the binary file (bin)")
    parser.add_argument("result_path", help="Path to the result file (csv)")
    parser.add_argument("first_index", help="The first index of the displayed memory")
    parser.add_argument("last_index", help="The last index of the displayed memory")
    args = parser.parse_args()
    interpreter(args.binary_path, args.result_path, (int(args.first_index), int(args.last_index)))