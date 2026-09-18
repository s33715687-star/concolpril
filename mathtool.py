"""
mathtool.py --- консольное приложение для решения алгебраических уравнений
вида A*x^2 + B*x + C = 0.

Использование:
    python mathtool.py                        вывод справки
    python mathtool.py --help                 вывод справки
    python mathtool.py solve                  ввод коэффициентов с клавиатуры
    python mathtool.py solve -a 1 -b -3 -c 2  решение с заданными коэффициентами

Коэффициенты A, B, C --- целые числа, по модулю не превышающие MAX_VALUE.
При успешном завершении приложение возвращает код 0, при ошибке --- код 1.
"""

import sys
import math

# Предельное по модулю значение коэффициента
MAX_VALUE = 10000

HELP_TEXT = (
    "mathtool --- решение уравнений вида A*x^2 + B*x + C = 0\n"
    "\n"
    "Использование:\n"
    "    python mathtool.py                        вывод справки\n"
    "    python mathtool.py --help                 вывод справки\n"
    "    python mathtool.py solve                  ввод коэффициентов с клавиатуры\n"
    "    python mathtool.py solve -a 1 -b -3 -c 2  решение с заданными коэффициентами\n"
    "\n"
    f"Коэффициенты A, B, C --- целые числа, по модулю не превышающие {MAX_VALUE}."
)


def print_help():
    """Выводит краткую справку о назначении и способах запуска приложения."""
    print(HELP_TEXT)


def read_from_keyboard():
    """Запрашивает коэффициенты A, B, C с клавиатуры. Возвращает строки."""
    a_str = input("Введите A: ")
    b_str = input("Введите B: ")
    c_str = input("Введите C: ")
    return a_str, b_str, c_str


def parse_args(argv):
    """
    Разбирает параметры командной строки.

    Возвращает кортеж строковых значений коэффициентов (a_str, b_str, c_str).
    При выводе справки или обнаружении ошибки завершает работу приложения
    вызовом sys.exit() с соответствующим кодом возврата.
    """
    # Параметров нет либо запрошена справка
    if len(argv) == 0 or argv[0] == "--help":
        print_help()
        sys.exit(0)

    # Первым параметром должна быть команда solve
    if argv[0] != "solve":
        print(f'ОШИБКА: неизвестная команда "{argv[0]}"', file=sys.stderr)
        sys.exit(1)

    # solve без коэффициентов -> запросить их с клавиатуры
    if len(argv) == 1:
        return read_from_keyboard()

    # solve -a .. -b .. -c .. -> взять коэффициенты из параметров
    if len(argv) == 7:
        keys = (argv[1], argv[3], argv[5])
        if keys != ("-a", "-b", "-c"):
            print("ОШИБКА: неизвестный параметр", file=sys.stderr)
            sys.exit(1)
        return argv[2], argv[4], argv[6]

    # Любой другой набор параметров считается неверным
    print("ОШИБКА: неверный набор параметров", file=sys.stderr)
    sys.exit(1)


def parse_coefficients(a_str, b_str, c_str):
    """Преобразует строковые коэффициенты в целые числа."""
    try:
        a = int(a_str)
        b = int(b_str)
        c = int(c_str)
    except ValueError:
        print("ОШИБКА: коэффициент не является целым числом", file=sys.stderr)
        sys.exit(1)
    return a, b, c


def validate_coefficients(a, b, c):
    """Проверяет коэффициенты на соответствие допустимому диапазону."""
    if abs(a) > MAX_VALUE or abs(b) > MAX_VALUE or abs(c) > MAX_VALUE:
        print("ОШИБКА: значение вне допустимого диапазона", file=sys.stderr)
        sys.exit(1)


def solve_linear(b, c):
    """Решает уравнение вида B*x + C = 0 (случай A = 0)."""
    if b != 0:
        print("Уравнение линейное")
        x = -c / b
        print(f"x = {x:.3f}")
    else:
        # B = 0 и A = 0 -> неизвестное в записи отсутствует
        print("ОШИБКА: это не уравнение, неизвестное отсутствует", file=sys.stderr)
        sys.exit(1)


def solve_quadratic(a, b, c):
    """Решает квадратное уравнение A*x^2 + B*x + C = 0 (случай A != 0)."""
    print("Уравнение квадратное")

    d = b * b - 4 * a * c
    print(f"D = {d}")

    if d > 0:
        x1 = (-b + math.sqrt(d)) / (2 * a)
        x2 = (-b - math.sqrt(d)) / (2 * a)
        print(f"x1 = {x1:.3f}")
        print(f"x2 = {x2:.3f}")
    elif d == 0:
        x = -b / (2 * a)
        print(f"x = {x:.3f}")
    else:
        print("Действительных корней нет")


def main():
    argv = sys.argv[1:]

    # 1. Разбор параметров командной строки
    a_str, b_str, c_str = parse_args(argv)

    # 2. Получение и преобразование исходных данных в целые числа
    a, b, c = parse_coefficients(a_str, b_str, c_str)

    # 3. Проверка значений на соответствие ограничениям
    validate_coefficients(a, b, c)

    # 4. Определение вида уравнения, решение и вывод результата
    if a == 0:
        solve_linear(b, c)
    else:
        solve_quadratic(a, b, c)

    sys.exit(0)


if __name__ == "__main__":
    main()
