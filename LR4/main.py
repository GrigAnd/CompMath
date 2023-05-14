import sys
from comp import *
import numpy as np
import matplotlib.pyplot as plt

def estimate_aproximation(func, par, points):
    if par == None:
        print("Апроксимация не найдена")
        return
    print("Параметры:", par)
    print("S: ", S(func, par, points))
    print("σ: ", mSqErr(func, par, points))

def plot_approximations(approximations, points):
    x = np.array([p[0] for p in points])
    x_new = np.linspace(min(x), max(x), 1000)
    y = np.array([p[1] for p in points])
    plt.scatter(x, y, color='black', label='Исходные данные')
    for name, (func, par) in approximations.items():
        try:
            y_pred = np.array([func(xi, par) for xi in x_new])
            plt.plot(x_new, y_pred, label=name)
        except (ValueError, TypeError):
            continue

    plt.legend()
    plt.grid()
    plt.axhline(y=0)
    plt.axvline(x=0)
    plt.show()

def read_points(file):
    points = []
    with open(file) as f:
        for line in f:
            try:
                x, y = line.split()
                points.append((float(x), float(y)))
            except ValueError:
                print("Неверный формат ввода")
                continue
    return points

def prompt_points():
    points = []
    print("Введите исходные точки (x, y) [8-12 точек]:")
    print("По окончанию ввода введите пустую строку")

    for i in range(12):
        line = input()

        if not line:
            if i < 8:
                print("Недостаточно точек")
                i -= 1
                continue
            break
        
        try:
            x, y = line.split()
            points.append((float(x), float(y)))
        except ValueError:
            print("Неверный формат ввода")
            i -= 1
            continue
    return points

def main():
    points = []
    
    if len(sys.argv) > 1:
        points = read_points(sys.argv[1])
    else:
        points = prompt_points()
        
    pol1_approx = mnk(points, 1)
    pol2_approx = mnk(points, 2)
    pol3_approx = mnk(points, 3)
    pow_approx = pow_wrap(points)
    exp_approx = exp_wrap(points)
    log_approx = log_wrap(points)

    print("Линейная:")
    estimate_aproximation(pol1, pol1_approx, points)
    print("Коэффициент корреляции: ", pearson(points))

    print("Полиномиальная 2 степени:")
    estimate_aproximation(pol2, pol2_approx, points)

    print("Полиномиальная 3 степени:")
    estimate_aproximation(pol3, pol3_approx, points)

    print("Степенная:")
    estimate_aproximation(pow, pow_approx, points)

    print("Экспоненциальная:")
    estimate_aproximation(exp, exp_approx, points)

    print("Логарифмическая:")
    estimate_aproximation(log, log_approx, points)

    approximations = {
        "линейная": (pol1, pol1_approx),
        "полиномиальная 2 степени": (pol2, pol2_approx),
        "полиномиальная 3 степени": (pol3, pol3_approx),
        "степенная": (pow, pow_approx),
        "экспоненциальная": (exp, exp_approx),
        "логарифмическая": (log, log_approx)
    }

    errors = {}
    for name, (func, par) in approximations.items():
        errors[name] = mSqErr(func, par, points)
    best_approximation = min(errors, key=errors.get)
    print("Лучшая апроксимация:", best_approximation)

    plot_approximations(approximations, points)

    print("Введите имя файла для сохранения результатов или пустую строку для выхода")
    filename = input()
    if filename:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Лучшая апроксимация: " + best_approximation + "\n")
            f.write("Параметры:\n")
            f.write(str(approximations[best_approximation][1]) + "\n")
            f.write("S: " + str(S(approximations[best_approximation][0], approximations[best_approximation][1], points)) + "\n")
            f.write("σ: " + str(mSqErr(approximations[best_approximation][0], approximations[best_approximation][1], points)) + "\n")
            f.write("Коэффициент корреляции: " + str(pearson(points)) + "\n")
            f.write("Исходные данные:\n")
            for point in points:
                f.write(str(point[0]) + " " + str(point[1]) + "\n")
            f.write("Апроксимация:\n")
            for point in points:
                f.write(str(point[0]) + " " + str(approximations[best_approximation][0](point[0], approximations[best_approximation][1])) + "\n")

if __name__ == "__main__":
    main()