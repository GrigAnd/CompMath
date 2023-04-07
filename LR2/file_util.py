from equations import *
from util import *
from comp import *

def file_proc(file):
    equation_type = int(file.readline())

    match equation_type:
        case 1:
            equation = equations[int(file.readline()) - 1][1]
            draw(equation, -10, 10)

            method = int(file.readline())

            a = float(file.readline())
            b = float(file.readline())
            if a > b:
                a, b = b, a
            rn = count_roots(equation, a, b)
            print("Количество корней на интервале:", rn)
            if rn != 1:
                return None

            precision = float(file.readline())

            match method:
                case 1:
                    solution, n_iter = half_dividing(equation, a, b, eps=precision, max_iter=100)
                case 2:
                    solution, n_iter = newton(equation, a, b, eps=precision, max_iter=100000)
                case 3:
                    solution, n_iter = simple_iterations(equation, a, b, eps=precision, max_iter=100)
                case _:
                    print("Нет такого метода")
                    return None
                
            if solution is not None:
                print("Количество итераций: ", n_iter)
                print("f(x) =", equation(solution))
                print("Ответ:", solution)
            else:
                print("Не сходится")

        case 2:
            sys_eq_index = int(file.readline()) - 1
            sys_eq = sys_equations[sys_eq_index]
            
            precision = float(file.readline())

            x01, x02 = list(map(float, file.readline().split()))
            solution, n_iter, pogr = simple_iterations_system(sys_eq, x01, x02, eps=precision, max_iter=100)

            if solution is not None:
                print("Вектор неизвестных:", solution)
            else:
                print("Не сходится")

            print("Количество итераций: ", n_iter)
            print("Вектор погрешностей: |xᵢᵏ − xᵢᵏ⁻¹| ", pogr)

            print("Проверка ответа:")
            print("f1(x₁, x₂) =", sys_eq[0][1](solution[0], solution[1]))
            print("f2(x₁, x₂) =", sys_eq[1][1](solution[0], solution[1]))
        case _:
            return None