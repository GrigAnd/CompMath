import math
import sys

def wrapper(method, equation, a, b, eps, n_div=4):
    while True:
        try:
            f1 = method(equation, a, b, n_div)
            f2 = method(equation, a, b, n_div * 2)
        except (ZeroDivisionError, ValueError):
            print("Деление на 0")
            sys.exit()

        print("f1:", f1[0], "f2:", f2[0], "f1-f2", f1[0] - f2[0], "n_div:", n_div )
        if abs(f1[0] - f2[0]) < eps:
            if math.isinf(f1[0]):
                print("Расходящийся интеграл")
                sys.exit()
            else:
                return f2
        if n_div > 1e4*(1/eps):
            print("Слишком большое количество разбиений")
            sys.exit()
        n_div *= 2

def equation_wrapper(equation, x):
    try:
        return equation(x)
    except (ZeroDivisionError, ValueError):
        try:
            ret = equation(x+1e-8)
            if not abs(ret) > 1e8:
                return ret
        except (ZeroDivisionError, ValueError):
            ret = equation(x-1e-10)
            if not abs(ret) > 1e8:
                return ret
    
    raise ValueError
    

def rectangle_left(equation, a, b, n_div=4):
    h = (b - a) / n_div
    f1 = 0
    for i in range(n_div):
        f1 += equation_wrapper(equation, a + i * h)
    f1 *= h
    return f1, n_div
    

def rectangle_middle(equation, a, b, n_div=4):
    h = (b - a) / n_div
    f1 = 0
    for i in range(n_div):
        f1 += equation_wrapper(equation, a + (i + 0.5) * h)
    f1 *= h
    return f1, n_div

def rectangle_right(equation, a, b, n_div=4):
    h = (b - a) / n_div
    f1 = 0
    for i in range(n_div):
        f1 += equation_wrapper(equation, a + (i + 1) * h)
    f1 *= h
    return f1, n_div

def trapezoid(equation, a, b, n_div=4):
    h = (b - a) / n_div
    f1 = equation_wrapper(equation, a) + equation_wrapper(equation, b)
    for i in range(1, n_div):
        f1 += 2 * equation_wrapper(equation, a + i * h)
    f1 *= h / 2
    return f1, n_div

def simpson(equation, a, b, n_div=4):
    h = (b - a) / n_div

    f1 = equation_wrapper(equation, a)

    for i in range(1, n_div, 2):
        f1 += 4 * equation_wrapper(equation, a + i * h)

    for i in range(2, n_div - 1, 2):
        f1 += 2 * equation_wrapper(equation, a + i * h)

    f1 += equation_wrapper(equation, b)

    f1 *= h / 3
    return f1, n_div
