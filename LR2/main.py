import sys

from comp import *
from equations import *
from file_util import *
from util import *

def enter_with_segment(equation):
    try:
        a = float(input("Введите левую границу интервала: "))
        b = float(input("Введите правую границу интервала: "))
    except ValueError:
        print("Не число")
        input()
        enter_with_segment(equation)
        
    if a > b:
        a, b = b, a
    rn = count_roots(equation, a, b)
    print("Количество корней на этом интервале:", rn)
    if rn == 0:
        print("Нет корней на этом интервале")
        return enter_with_segment(equation)
    elif rn > 1:
        print("Больше одного корня")
        return enter_with_segment(equation)
    
    draw(equation, a - 1, b + 1)
    return a, b

def enter_for_equation(equation):
    a, b = enter_with_segment(equation)
    precision = float(input("Введите точность: "))
    return a, b, precision

def choose_method(equation):
    print("Выберите метод решения:")
    print("1) половинного деления")
    print("2) Ньютона")
    print("3) простых итераций")
    try:
        method = int(input())  
    except ValueError:
        print("Не число")
        input()
        choose_method(equation) 

    a, b, precision = enter_for_equation(equation)


    try:
        match method:
            case 1:
                solution, n_iter = half_dividing(equation, a, b, eps=precision, max_iter=100)
            case 2:
                solution, n_iter = newton(equation, a, b, eps=precision, max_iter=100)
            case 3:
                solution, n_iter = simple_iterations(equation, a, b, eps=precision, max_iter=100)
            case _:
                print("Нет такого метода")
                choose_method(equation)
    except OverflowError:
        print("Переполнение (а значит расходится)")
        sys.exit()
        
    if solution is not None:
        print("Количество итераций: ", n_iter)
        print("f(x) =", equation(solution))
        print("Ответ:", solution)
        name = input("Введите имя файла для сохранения/n для отмены: ")
        if name != "n":
            save_to_file(name, [["Количество итераций: ", n_iter], ["f(x) =", equation(solution)], ["Ответ:", solution]])
    else:
        print("Не сходится")

def choose_equation_system():
    print("Выберите систему уранвений:")
    for i, sys_eq in enumerate(sys_equations):
        print(f"{i + 1}) {sys_eq[0][0]}")
        print(sys_eq[1][0])

    try:
        sys_eq_index = int(input()) - 1
        sys_eq = sys_equations[sys_eq_index]
    except IndexError:
        print("Нет такой системы уравнений")
        choose_equation_system()
    except ValueError:
        print("Не число")
        input()
        choose_equation_system()

    draw_system(sys_eq[0][1], sys_eq[1][1], max(sys_eq[0][2][0], sys_eq[1][2][0]), min(sys_eq[0][2][1], sys_eq[1][2][1]))

    precision = float(input("Введите точность решения: "))

    x01, x02 = list(map(float, input("Введите начальное приближение (x₀₁, x₀₂): ").split()))
    solution, n_iter, pogr = simple_iterations_system(
        sys_eq, x01, x02, eps=precision, max_iter=100)

    if solution is not None:
        print("Вектор неизвестных:", solution)
        print("Количество итераций: ", n_iter)
        print("Вектор погрешностей: |xᵢᵏ − xᵢᵏ⁻¹|", pogr)

        # check answer
        print("Проверка ответа:")
        print("f1(x₁, x₂) =", sys_eq[0][1](solution[0], solution[1]))
        print("f2(x₁, x₂) =", sys_eq[1][1](solution[0], solution[1]))

        name = input("Введите имя файла для сохранения/n для отмены: ")
        if name != "n":
            save_to_file(name, [["Вектор неизвестных:", solution], ["Количество итераций: ", n_iter], ["Вектор погрешностей: |xᵢᵏ − xᵢᵏ⁻¹|", pogr]])
    else:
        print("Не сходится")

    

def choose_equation():
    print("Выберите уравнение:")
    for i, equation in enumerate(equations):
        print(f"{i + 1}) {equation[0]}")

    try:
        equation_index = int(input()) - 1
        equation = equations[equation_index][1]
    except IndexError:
        print("Нет такого уравнения")
        choose_equation()
    except ValueError:
        print("Не число")
        input()
        choose_equation()

    return equation, equations[equation_index][2]


def enter_type():
    print("Выберите тип:")
    print("1) Уравнение")
    print("2) Система уравнений")

    try:
        equation_type = int(input())
    except ValueError:
        print("Не число")
        input()
        enter_type()

    match equation_type:
        case 1:
            equation, interval = choose_equation()

            draw(equation, interval[0], interval[1])

            choose_method(equation)

        case 2:
            choose_equation_system()

        case _:
            print("Нет такого типа")
            enter_type()


if len(sys.argv) > 1:
    try:
        file = open(sys.argv[1], "r")
        file_proc(file)
    except FileNotFoundError:
        print("Файл не найден")
        enter_type()  
else:
    enter_type()  

