import math
import numpy as np


def pol1(x, par):
    return par[0] + par[1] * x


def pol2(x, par):
    return par[0] + par[1] * x + par[2] * x**2


def pol3(x, par):
    return par[0] + par[1] * x + par[2] * x**2 + par[3] * x**3


def exp(x, par):
    return par[0] * math.exp(par[1] * x)


def log(x, par):
    if x <= 0:
        raise ValueError("x must be positive")
    return par[0] * math.log(x) + par[1]


def pow(x, par):
    if x <= 0:
        raise ValueError("x must be positive")
    return par[0] * x ** par[1]

funcs = {
    "Линейная": pol1,
    "Полиномиальная 2 степени": pol2,
    "Полиномиальная 3 степени": pol3,
    "Степенная": pow,
    "Экспоненциальная": exp,
    "Логарифмическая": log
}


def S(func, par, points):
    s = 0
    for p in points:
        try:
            s += (func(p[0], par) - p[1])**2
        except ValueError:
            return float("inf")

    return s


def mSqErr(func, par, points):
    if par == None:
        return float("inf")

    return (S(func, par, points) / (len(points)))**0.5


def mnk(points, pow):
    A = []
    for i in range(pow + 1):
        A.append([])
        for j in range(pow + 1):
            s = 0
            for p in points:
                s += p[0]**(i + j)
            A[i].append(s)

    B = []
    for i in range(pow + 1):
        s = 0
        for p in points:
            # print(p)
            s += p[1] * p[0]**i
        B.append(s)

    return list(np.linalg.solve(A, B))


def pow_wrap(points):
    converted_points = []
    try:
        for p in points:
            converted_points.append((math.log(p[0]), math.log(p[1])))
    except ValueError:
        print("Логарифм от отрицательного значения")
        return

    param = mnk(converted_points, 1)
    a = math.exp(param[1])
    b = param[0]

    return (a, b)


def exp_wrap(points):
    converted_points = []

    try:
        for p in points:
            converted_points.append((p[0], math.log(p[1])))
    except ValueError:
        print("Логарифм от отрицательного значения")
        return

    param = mnk(converted_points, 1)
    a = math.exp(param[0])
    b = param[1]

    return (a, b)


def log_wrap(points):
    converted_points = []

    try:
        for p in points:
            converted_points.append((math.log(p[0]), p[1]))
    except ValueError:
        print("Неверный формат ввода")
        return

    param = mnk(converted_points, 1)
    a = param[0]
    b = param[1]

    return (a, b)


def pearson(points):
    x_mean = 0
    y_mean = 0
    for p in points:
        x_mean += p[0]
        y_mean += p[1]
    x_mean /= len(points)
    y_mean /= len(points)

    x_disp = 0
    y_disp = 0
    for p in points:
        x_disp += (p[0] - x_mean)**2
        y_disp += (p[1] - y_mean)**2
    x_disp /= len(points)
    y_disp /= len(points)

    xy_cov = 0
    for p in points:
        xy_cov += (p[0] - x_mean) * (p[1] - y_mean)
    xy_cov /= len(points)

    return xy_cov / (x_disp * y_disp)**0.5
