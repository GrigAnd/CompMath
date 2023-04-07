def half_dividing(equation, a, b, eps=1e-6, max_iter=100):
    f = equation

    print("Step\ta\t\tb\t\tx\t\tf(a)\t\tf(b)\t\tf(x)\t\t|a-b|")

    for i in range(max_iter):
        x = (a + b) / 2
        fa = f(a)
        fb = f(b)
        fx = f(x)
        error = abs(b - a)

        print(
            f"{i+1}\t{a:.6f}\t{b:.6f}\t{x:.6f}\t{fa:.6f}\t{fb:.6f}\t{fx:.6f}\t{error:.6f}")

        if abs(fx) < eps :
            return x, i + 1
        if fa * fx < 0:
            b = x
        else:
            a = x
    return None

def choose_initial_guess(f, a, b):
    f_a = f(a)
    f_b = f(b)
    f_double_prime_a = second_derivative(f, a)
    f_double_prime_b = second_derivative(f, b)

    print (f_a, f_double_prime_a, f_b, f_double_prime_b)
    

    if f_a * f_double_prime_a > 0:
        return a
    elif f_b * f_double_prime_b > 0:
        return b
    else:
        return (a + b) / 2
        # return b


def second_derivative(f, x, h=1e-6):
    return (f(x + h) - 2 * f(x) + f(x - h)) / (h ** 2)


def newton(equation, a, b, eps=1e-6, max_iter=100):
    x0 = choose_initial_guess(equation, a, b)
    f = equation
    def fprime(x): return (f(x + eps) - f(x)) / eps
    x = x0
    print("Step\t xₖ\t\t f(xₖ)\t\t f'(xₖ)\t\t xₖ₊₁\t\t |xₖ₊₁ - xₖ|")
    for i in range(max_iter):
        fx = f(x)
        
        fpx = fprime(x)
        if fpx == 0:
            return None
        x_next = x - fx / fpx
        print(
            f"{i+1}\t {x:.8f}\t {fx:.8f}\t {fpx:.8f}\t {x_next:.8f}\t {abs(x_next - x):.8f}")
        x = x_next
        if abs(fx) < eps:
            return x, i + 1
    return None


def simple_iterations(func, a, b, eps=1e-6, max_iter=100):
    def lyam():
        max_derivative = 0
        for i in range(int(1 / eps)):
            x = a + i * (b - a) / (int(1 / eps))
            current_derivative = abs((func(x + 1e-10) - func(x)) / 1e-10)
            if current_derivative > max_derivative:
                max_derivative = current_derivative
                break

        return -1 / max_derivative

    def find_x(xk):
        return xk + lyam() * func(xk)

    def derivative(x):
        return (find_x(x + eps) - find_x(x)) / eps

    print(derivative(a), derivative(b))
    
    for i in range(int(1 / eps)):
        x = a + i * (b - a) / (int(1 / eps))
        if abs(derivative(x)) >= 1:
            print("Не выполняется условие сходимости")
            break


    

    

    xk = choose_initial_guess(func, a, b)

    step = 0
    print("Step \t xₖ \t\t xₖ₊₁ \t\t f(xₖ₊₁) \t |xₖ₊₁ - xₖ|")

    new_xk = find_x(xk)
    print(f"{step} \t {xk:.8f} \t {new_xk:.8f} \t {func(new_xk):.8f} \t {abs(new_xk - xk):.8f}")
    while (abs(new_xk - xk) > eps or func(new_xk)>eps) and step < max_iter:
        step += 1
        xk = new_xk
        new_xk = find_x(xk)
        print(
            f"{step} \t {xk:.8f} \t {new_xk:.8f} \t {func(new_xk):.8f} \t {abs(new_xk - xk):.8f}")
    return new_xk, step


def simple_iterations_system(funcs, x01, x02, eps=1e-6, max_iter=100):
    def phi1(x1, x2):
        return - funcs[0][1](x1, x2) + x1
    
    def phi2(x1, x2):
        return - funcs[1][1](x1, x2) + x2
    
    if not check_convergence([phi1, phi2], x01, x02):
        print("Не сходится")
    
    print("Step \t x₁ \t\t x₂ \t\t |x₁ₖ₊₁ - x₁| \t |x₂ₖ₊₁ - x₂|")
    for i in range(max_iter):
        x1 = phi1(x01, x02)
        x2 = phi2(x01, x02)

        print(f"{i+1}\t{x1:.8f}\t{x2:.8f}\t{abs(x1 - x01):.8f}\t{abs(x2 - x02):.8f}")

        if abs(x1 - x01) < eps and abs(x2 - x02) < eps:
            return [x1, x2], i+1, [abs(x1 - x01), abs(x2 - x02)]
        x01 = x1
        x02 = x2

    return None

def check_convergence(phis, x1, x2):
    d_phi1_dx1 = partial_derivative(phis[0], 1, x1, x2)
    d_phi1_dx2 = partial_derivative(phis[0], 2, x1, x2)
    d_phi2_dx1 = partial_derivative(phis[1], 1, x1, x2)
    d_phi2_dx2 = partial_derivative(phis[1], 2, x1, x2)

    print(d_phi1_dx1 , d_phi1_dx2, d_phi2_dx1 , d_phi2_dx2)

    max_val = max(abs(d_phi1_dx1 + d_phi1_dx2), abs(d_phi2_dx1 - d_phi2_dx2))
    
    if max_val <= 1:
        return True
    else:
        return False
    
def partial_derivative(func, var, x1, x2):
    h = 1e-6
    if var == 1:
        return (func(x1+h, x2) - func(x1-h, x2)) / (2*h)
    elif var == 2:
        return (func(x1, x2+h) - func(x1, x2-h)) / (2*h)

def count_roots(func, a, b, step=1e-4):
    roots = 0
    pm = 0
    last = 0
    for i in range(int((b - a) / step)):
        x = a + i * step
        if func(x) * pm < 0:
            roots += 1
            print(f"Корень {roots} в [{last:.8f}, {x:.8f}]")
        last = x

        pm = func(x)
    return roots