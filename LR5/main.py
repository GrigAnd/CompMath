import matplotlib.pyplot as plt
from comp import *
from util import *

x, y, func = prompt()
d = finite_differences(y)
print_fin_def(d)

z = float(input("Введите значение z для интерполяции: "))
p_lagrange = lagrange(x, y, z)
p_newton_general = newton(x, z, d)


print(f"Значение многочлена Лагранжа в точке {z} равно {p_lagrange}")
print(f"Значение многочлена Ньютона в точке {z} равно {p_newton_general}")

xx = np.linspace(min(x), max(x), 1000)
if func is not None:
    yy = [func(xx) for xx in xx]
    plt.plot(xx, yy, 'r-', label='Функция')
pp_n = [newton(x, xx, d) for xx in xx]
pp_l = [lagrange(x, y, xx) for xx in xx]

plt.plot(x, y, 'bo', label='Точки данных')
plt.plot(xx, pp_n, 'g-', label='Многочлен Ньютона')
plt.plot(xx, pp_l, 'm-', label='Многочлен Лагранжа')


if is_eq_dist(x):
    p_newton_eq_dist = newton_eq_dist(x, y, z, d)
    print( f"Значение многочлена Ньютона для для равноотстоящих {z} равно {p_newton_eq_dist}")
    pp_ne = [newton_eq_dist(x, y, xx, d) for xx in xx]
    plt.plot(xx, pp_ne, 'c-', label='Многочлен Ньютона для равноотстоящих')

    if len(x) % 2 == 1:
        print( f"Нечётное количество узлов - считаем только Стирлига, без Бесселя")
        p_stirling = stirling(x, y, z, d)
        print(f"Значение многочлена Стирлинга в точке {z} равно {p_stirling}")
        pp_s = [stirling(x, y, xx, d) for xx in xx]
        plt.plot(xx, pp_s, 'y-', label='Многочлен Стирлинга')
    else:
        print( f"Чётное количество узлов - считаем только Бесселя, без Стирлинга")
        p_bessel = bessel(x, y, z, d)
        print(f"Значение многочлена Бесселя в точке {z} равно {p_bessel}")
        pp_b = [bessel(x, y, xx, d) for xx in xx]
        plt.plot(xx, pp_b, 'k-', label='Многочлен Бесселя')

plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid()
plt.show()