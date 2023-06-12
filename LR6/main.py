from comp import *
import numpy as np
import sympy
import matplotlib.pyplot as plt

funcs = [
    [
        "y' = sin(x) + y",
        lambda x, y: np.sin(x) + y,
        lambda x, C: -np.sin(x) / 2 - np.cos(x) / 2 + C * np.e**x,
    ],
    [
        "y' = xy",
        lambda x, y: x*y,
        lambda x, C: C * np.e ** (x**2 / 2),
    ],
    [
        "y' = y + (1+x)y^2",
        lambda x, y: y+(1+x)*y**2,
        lambda x, C: -(np.e**x)/(x*np.e**x+C)
    ]
]

print("Доступные функции:")
for i, func in enumerate(funcs):
    print(f"{i+1}. {func[0]}")

functionNumber = int(input("Введите номер функции: ")) - 1

if functionNumber < 0 or functionNumber >= len(funcs):
    print("Неверный номер функции.")
    exit()

func = funcs[functionNumber][1]
ex_sol = funcs[functionNumber][2]

y0 = float(input("Введите y0: "))
a = float(input("Введите начало интервала a: "))
b = float(input("Введите конец интервала b: "))

if a >= b:
    print("Неверный интервал.")
    exit()

h = float(input("Введите шаг h: "))

if h <= 0:
    print("Неверный шаг.")
    exit()

b_init = b

if (b - a) % h != 0:
    krat = (b - a) // h + 1
    b = a + krat * h

eps = float(input("Введите допуск eps: ").replace(",", "."))

if eps <= 0:
    print("Неверный допуск")
    exit()

if eps <= 1e-8:
    print("Слишком малый допуск, возможно слишком долгое решение")

C = sympy.symbols("С")
try:
    C = sympy.solve(ex_sol(a, C) - y0, C)[0]
except IndexError:
    print("Не имеет решений")
    exit()

print(f"C = {C}")

t = np.linspace(a, b, 100)
print("Результаты:")
print("      \t\tx\t\ty")

try:
    result_euler, pogr, h = euler(a, b, y0, h, func, eps)
    print("Эйлер")
    for row in result_euler[:20]:
        print(f"\t\t{row[0]:.3f}\t\t{row[1]:.3f}\t\t{row[2]:.5f}")
    print(f"Погрешность: {pogr}, h={h}")
    result_euler = np.array(result_euler)
    plt.plot(result_euler[:, 0], result_euler[:, 1], label="Эйлер")

except ValueError as e:
    print("Невозможно решить модифицированным методом Эйлера")
except OverflowError as e:
    print("Во время подсчёта модифицированным методом Эйлера произошло переполнение")


try:
    result_rungkutt_4, pogr, h = rungkutt_4(a, b, y0, h, func, eps)
    print("Рунге-Кутта 4")
    for row in result_rungkutt_4[:20]:
        print(f"\t\t{row[0]:.3f}\t\t{row[1]:.3f}\t\t{row[2]:.5f}")
    print(f"Погрешность: {pogr}, h={h}")
    result_rungkutt_4 = np.array(result_rungkutt_4)
    plt.plot(result_rungkutt_4[:, 0], result_rungkutt_4[:, 1], label="Рунге-Кутта 4")

except ValueError as e:
    print("Невозможно решить методом Рунге-Кутты 4")
except OverflowError as e:
    print("Во время подсчёта методом Рунге-Кутты 4 произошло переполнение")


try:
    result_adams = adams_4(a, b, y0, h, func, eps)
    h_half = h / 2
    max_eps = 0
    pogr = []
    for row in result_adams:
        # print(f"\t\t{row[0]:.3f}\t\t{row[1]:.3f}")
        max_eps = max(max_eps, abs(row[1] - ex_sol(row[0], C)))
        pogr.append(abs(row[1] - ex_sol(row[0], C)))

    steps = 0
    max_steps = 10
    while max_eps > eps and steps < max_steps:
        pogr = []
        max_eps = 0
        result_adams = adams_4(a, b, y0, h_half, func, eps)
        for row in result_adams:
            # print(f"\t\t{row[0]:.3f}\t\t{row[1]:.3f}")
            max_eps = max(max_eps, abs(row[1] - ex_sol(row[0], C)))
            pogr.append(abs(row[1] - ex_sol(row[0], C)))
        h_half = h_half / 2
        steps += 1

    
    print("Адамс")
    result_adams = [[x, y, 0] for x, y in result_adams]
    for i in range(len(pogr)):
        result_adams[i][2] = pogr[i]

    for row in result_adams[:20]:
        print(f"\t\t{row[0]:.3f}\t\t{row[1]:.3f}\t\t{row[2]:.6f}")
    print(f"Погрешность: {max_eps}, h={h_half*2}")

    # for row in pogr[:20]:
    #     print(f"Погрешность: {row}")

    result_adams = np.array(result_adams)
    plt.plot(result_adams[:, 0], result_adams[:, 1], label="Адамс")
    
# except ValueError as e:
#     print("Невозможно решить методом Адамса")
except OverflowError as e:
    print("Во время подсчёта методом Адамса произошло переполнение")

plt.plot(t, [ex_sol(t, C) for t in t], label="Точный")
plt.xlabel("t")
plt.ylabel("y")
plt.xlim(a-(b_init-a)/20, b_init+(b_init-a)/20)
plt.legend()
plt.grid()
plt.show()
