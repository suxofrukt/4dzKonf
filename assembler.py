import argparse
import struct
import yaml


# Логирование операций в формате YAML
def log_operation(log_path, operation_code, *args):
    if log_path is not None:
        log_data = {
            'operation_code': operation_code,
            'args': args
        }
        # Добавляем новую операцию в лог
        with open(log_path, "a", encoding="utf-8") as log_file:
            yaml.dump([log_data], log_file, default_flow_style=False, allow_unicode=True)


# Сериализация инструкции в байты
def serializer(cmd, fields, size):
    # Создаем начальные биты с помощью команды
    bits = cmd
    # Добавляем остальные поля с учетом смещения
    for value, offset in fields:
        bits |= (value << offset)
    # Возвращаем байты в нужном формате (little-endian)
    return bits.to_bytes(size, "little")


# Внутри функции assembler
def assembler(instructions, log_path=None):
    byte_code = []
    for operation, *args in instructions:
        if operation == "load":
            B, C = args
            if B < 0 or B >= 32:  # Проверка допустимого индекса
                raise ValueError(f"Invalid register index: {B}. Valid range is 0-31.")
            print(f"Operation: load, B: {B}, C: {C}")  # Вывод для отладки
            byte_code += list(serializer(52, ((B, 7), (C, 12)), 5))
            log_operation(log_path, 52, B, C)
        elif operation == "read":
            B, C, D = args
            if B < 0 or B >= 32 or C < 0 or C >= 32:  # Проверка допустимого индекса
                raise ValueError(f"Invalid register index: B={B}, C={C}. Valid range is 0-31.")
            print(f"Operation: read, B: {B}, C: {C}, D: {D}")  # Вывод для отладки
            byte_code += list(serializer(43, ((B, 7), (C, 12), (D, 17)), 5))
            log_operation(log_path, 43, B, C, D)
        elif operation == "write":
            B, C = args
            if B < 0 or B >= 32:  # Проверка допустимого индекса
                raise ValueError(f"Invalid register index: {B}. Valid range is 0-31.")
            print(f"Operation: write, B: {B}, C: {C}")  # Вывод для отладки
            byte_code += list(serializer(25, ((B, 7), (C, 12)), 5))
            log_operation(log_path, 25, B, C)
        elif operation == "not":
            B, C, D = args
            if B < 0 or B >= 32 or C < 0 or C >= 32:  # Проверка допустимого индекса
                raise ValueError(f"Invalid register index: B={B}, C={C}. Valid range is 0-31.")
            print(f"Operation: not, B: {B}, C: {C}, D: {D}")  # Вывод для отладки
            byte_code += list(serializer(57, ((B, 7), (C, 12), (D, 17)), 5))
            log_operation(log_path, 57, B, C, D)
    return byte_code


# Обработка входного файла с инструкциями
def assemble(instructions_path: str, log_path=None):
    with open(instructions_path, "r", encoding="utf-8") as f:
        instructions = []
        for line in f.readlines():
            # Преобразуем строку в список, где цифры остаются числами, а слова - строками
            instructions.append([int(x) if x.isdigit() else x for x in line.split()])
    return assembler(instructions, log_path)


# Сохранение ассемблированных инструкций в бинарный файл
def save_to_bin(assembled_instructions, binary_path):
    with open(binary_path, "wb") as binary_file:
        binary_file.write(bytes(assembled_instructions))


# Главная функция
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assembling the instructions file to the byte-code.")
    parser.add_argument("instructions_path", help="Path to the instructions file (txt)")
    parser.add_argument("binary_path", help="Path to the binary file (bin)")
    parser.add_argument("log_path", help="Path to the log file (yaml)")
    args = parser.parse_args()

    # Инициализация лог-файла
    with open(args.log_path, "w", encoding="utf-8") as log_file:
        yaml.dump([], log_file, default_flow_style=False, allow_unicode=True)

    # Ассемблирование инструкций
    result = assemble(args.instructions_path, args.log_path)

    # Сохранение в бинарный файл
    save_to_bin(result, args.binary_path)