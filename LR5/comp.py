import numpy as np


def finite_differences(y):
    n = len(y)
    f = np.copy(y)
    d = np.zeros((n, n))
    d[:, 0] = f
    for j in range(1, n):
        for i in range(n - j):
            d[i, j] = d[i + 1, j - 1] - d[i, j - 1]
    return d


def lagrange(x, y, z):
    n = len(x)
    p = 0
    for i in range(n):
        l = 1
        for j in range(n):
            if i != j:
                l *= (z - x[j]) / (x[i] - x[j])
        p += l * y[i]
    return p


def newton(x, z, d):
    n = len(x)
    p = d[0, 0]
    q = 1
    for i in range(1, n):
        q *= (z - x[i - 1]) / (x[i] - x[i - 1])

        p += q * d[0, i] / np.math.factorial(i)
    return p


def newton_eq_dist(x, y, z, d):
    if z > (x[0] + x[-1]) / 2:
        print("Используем 2ую интерполяционную формулу Ньютона")
        return newton_backward(x, y, z, d)
    else:
        print("Используем 1ую интерполяционную формулу Ньютона")
        return newton_forward(x, y, z, d)


def newton_forward(x, y, z, d):
    n = len(x)
    print("n: ", n)
    step = x[1] - x[0]
    t = (z - x[0]) / step
    N = y[0]
    q = t
    for i in range(1, n):
        N += q * d[0, i] / np.math.factorial(i)
        print("i=", i, "d=", d[0, i])
        q *= t - i
    return N


def newton_backward(x, y, z, d):
    n = len(x)
    step = x[1] - x[0]
    t = (z - x[n - 1]) / step
    N = y[n - 1]
    q = t
    for i in range(1, n):
        N += q * d[n - i - 1, i] / np.math.factorial(i)
        print("i=", i, "d=", d[n - i - 1, i])
        q *= t + i
    return N


def stirling(x, y, z, d):
    _2n = len(x) - 1
    ind = len(x) // 2
    step = x[1] - x[0]
    t = (z - x[ind]) / step
    print("t=", t)
    if not (np.abs(t) <= 0.5):
        print("Стирлинг лучше применять только в интервале t [-0.5, 0.5]")
    p = y[ind]
    q = 1
    for i in range(1, _2n + 1, 2):
        fd1 = d[ind, i]
        fd2 = d[ind - 1, i]
        fd3 = d[ind - 1, i + 1]
        print(
            f"d[{ind}, {i}]=",
            fd1,
            f"d[{ind - 1}, {i}]=",
            fd2,
            f"d[{ind - 1}, {i + 1}]=",
            fd3,
        )
        q *= t**2 - (i // 2) ** 2
        tt = 1 if t == 0 else t
        ls = q / tt / np.math.factorial(i) * (fd1 + fd2) / 2
        rs = q / np.math.factorial(i + 1) * fd3
        p += ls + rs
        ind -= 1
    return p


def bessel(x, y, z, d):
    _2n = len(x) - 1
    ind = len(x) // 2 - 1
    step = x[1] - x[0]
    t = (z - x[ind]) / step
    print("t=", t)
    if not (np.abs(t) <= 0.75 and np.abs(t) >= 0.25):
        print("Бессель лучше применять только в интервале |t| [0.25, 0.75]")

    t12 = t - 0.5
    p = (y[ind] + y[ind + 1]) / 2 + t12 * d[ind, 1]
    q = 1
    for i in range(2, _2n + 1, 2):
        q *= (t - i // 2) * (t + i // 2 - 1)
        ls = q / np.math.factorial(i) * (d[ind, i] + d[ind - 1, i]) / 2
        rs = t12 * q / np.math.factorial(i + 1) * d[ind - 1, i + 1]
        print(
            f"d[{ind}, {i}]",
            d[ind, i],
            f"d[{ind - 1}, {i}]",
            d[ind - 1, i],
            f"d[{ind - 1}, {i + 1}]",
            d[ind - 1, i + 1],
        )
        p += ls + rs
        ind -= 1
    return p
