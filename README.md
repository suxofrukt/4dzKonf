# 4dzKonf
Задание №4
Разработать ассемблер и интерпретатор для учебной виртуальной машины
(УВМ). Система команд УВМ представлена далее.
Для ассемблера необходимо разработать читаемое представление команд
УВМ. Ассемблер принимает на вход файл с текстом исходной программы, путь к
которой задается из командной строки. Результатом работы ассемблера является
бинарный файл в виде последовательности байт, путь к которому задается из
командной строки. Дополнительный ключ командной строки задает путь к файлу-
46
логу, в котором хранятся ассемблированные инструкции в духе списков
“ключ=значение”, как в приведенных далее тестах.
Интерпретатор принимает на вход бинарный файл, выполняет команды УВМ
и сохраняет в файле-результате значения из диапазона памяти УВМ. Диапазон
также указывается из командной строки.
Форматом для файла-лога и файла-результата является yaml.
Необходимо реализовать приведенные тесты для всех команд, а также
написать и отладить тестовую программу.
Загрузка константы
A B C
Биты 0—6 Биты 7—11 Биты 12—25
52 Адрес Константа
Размер команды: 5 байт. Операнд: поле C. Результат: регистр по адресу,
которым является поле B.
Тест (A=52, B=25, C=791):
0xB4, 0x7C, 0x31, 0x00, 0x00
Чтение значения из памяти
A B C D
Биты 0—6 Биты 7—11 Биты 12—16 Биты 17—32
43 Адрес Адрес Смещение
Размер команды: 5 байт. Операнд: значение в памяти по адресу, которым
является сумма адреса (регистр по адресу, которым является поле C) и смещения
(поле D). Результат: регистр по адресу, которым является поле B.
Тест (A=43, B=6, C=30, D=217):
0x2B, 0xE3, 0xB3, 0x01, 0x00
Запись значения в память
A B C
47
A B C
Биты 0—6 Биты 7—11 Биты 12—21
25 Адрес Адрес
Размер команды: 5 байт. Операнд: регистр по адресу, которым является поле
B. Результат: значение в памяти по адресу, которым является поле C.
Тест (A=25, B=5, C=11):
0x99, 0xB2, 0x00, 0x00, 0x00
Унарная операция: побитовое "не"
A B C D
Биты 0—6 Биты 7—11 Биты 17—32
57 Адрес Смещение
Биты 12—16 Адрес Размер команды: 5 байт. Операнд: значение в памяти по адресу, которым
является регистр по адресу, которым является поле C. Результат: значение в
памяти по адресу, которым является сумма адреса (регистр по адресу, которым
является поле B) и смещения (поле D).
Тест (A=57, B=23, C=11, D=70):
0xB9, 0xBB, 0x8C, 0x00, 0x00
Тестовая программа
Выполнить поэлементно операцию побитовое "не" над вектором длины 5.
Результат записать в новый вектор.
