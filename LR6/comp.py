import numpy as np

def adams_4(a, b, y0, h, func, eps):
    rk, _, _ = rungkutt_4(a, a + 4 * h, y0, h, func, eps)
    if rk is None:
        print("Ошибка при попытке нахождения 4 первых точек")
    rk = [[row[0], row[1]] for row in rk]
    return adams(b, rk, h, func)

def adams(b, start, h, func):
    n = int((b - start[-1][0]) / h)
    result = start 
    for i in range(n):
        f = [func(x, y) for x, y in result[i:i + 4]]
        df1 = f[-1] - f[-2]
        df2 = f[-1] - 2*f[-2] + f[-3]
        df3 = f[-1] - 3*f[-2] + 3 * f[-3] - f[-4]
        x = result[-1][0]
        y = result[-1][1]
        result.append((x + h, y + h * f[-1] +1 / 2 * h ** 2 * df1 + 5 / 12 * h ** 3 * df2 + 3 / 8 * h ** 4 * df3))
    return result

def runge(result, b, h, func, formula, eps, p):
    result = [[x, y, 0] for x, y in result]
    result_2 = result.copy()
    h_2 = h / 2
    while result[-1][0] < b + 0.0001:
        xy = formula(result, h, func)
        result_2.append(formula(result_2, h_2, func))
        xy_2 = formula(result_2, h_2, func)
        pogr = abs(xy[1] - xy_2[1]) / (2**p - 1)
        if pogr > eps:
            h /= 2
            h_2 /= 2
            result = result[:1]
            result_2 = result_2[:1]
        else:
            result.append([xy[0], xy[1], pogr])
            result_2.append(xy_2)
    return result, pogr, h

def euler(a, b, y0, h, func, eps):
    result = [(a, y0)]

    def formula(result, h, func):
        x = result[-1][0]
        y = result[-1][1]
        x_new = x + h
        y_new = y + h / 2 * (
            func(x, y)
            + func(
                x + h,
                y + h * func(x, y),
            )
        )
        return x_new, y_new
        
    return runge(result, b, h, func, formula, eps, 2)


def rungkutt_4(a, b, y0, h, func, eps):
    result = [[a, y0]]

    def formula(result, h, func):
        x = result[-1][0]
        y = result[-1][1]
        x_new = x + h

        k1 = h * func(x, y)
        k2 = h * func(x + h / 2, y + k1 / 2)
        k3 = h * func(x + h / 2, y + k2 / 2)
        k4 = h * func(x + h, y + k3)

        y_new = (
            y
            + (
                k1
                + 2 * k2
                + 2 * k3
                + k4
            )
            / 6
        )

        return x_new, y_new

    return runge(result, b, h, func, formula, eps, 4)
