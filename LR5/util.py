import numpy as np
from funcs import *


def print_fin_def(d):
    print("Таблица конечных разностей:")
    n = len(d)
    print("{:14s}".format("xi"), end=" ")
    for i in range(n):
        print("{:14s}".format("Δ{}y".format(i)), end=" ")
    print()
    for i in range(n):
        print("x{} {:14.6f}".format(i, d[i][0]), end=" ")
        for j in range(1, n):
            if j < n - i:
                print("{:14.6f}".format(d[i][j]), end=" ")
            else:
                print("{:14s}".format("    -"), end=" ")
        print()


def read_data(filename):
    data = np.loadtxt(filename)
    x = data[:, 0]
    y = data[:, 1]
    return x, y


def input_data():
    n = int(input("Введите количество точек данных: "))
    x = np.zeros(n)
    y = np.zeros(n)
    for i in range(n):
        x[i] = float(input(f"Введите x[{i}]: "))
        y[i] = float(input(f"Введите y[{i}]: "))
    return x, y


def generate_data(func):
    a = float(input("Введите нижнюю границу интервала: "))
    b = float(input("Введите верхнюю границу интервала: "))
    n = int(input("Введите количество точек данных: "))
    x = np.linspace(a, b, n)
    y = [func(x) for x in x]
    return x, y


def prompt():
    x, y = [], []
    func = None
    print("Выберите способ ввода данных:")
    print("1. Ввести с клавиатуры")
    print("2. Прочитать из файла")
    print("3. Сгенерировать из функции")
    choice = int(input("Введите ваш выбор (1/2/3): "))

    if choice == 1:
        x, y = input_data()
    elif choice == 2:
        filename = input("Введите имя файла: ")
        x, y = read_data(filename)
    elif choice == 3:
        print("Выберите функцию:")
        for i, f in enumerate(funcs):
            print(f"{i+1}) {f[0]}")

        choice = input("Введите номер функции: ")
        try:
            index = int(choice) - 1
            func = funcs[index][1]
        except (IndexError, ValueError):
            print("Неверный номер функции")
        x, y = generate_data(func)
    else:
        print("Неверный выбор")
        return prompt()

    return x, y, func


def is_eq_dist(x, eps=1e-6):
    n = len(x)
    for i in range(1, n):
        if (x[i] - x[i - 1]) - (x[1] - x[0]) > eps:
            return False
    return True
