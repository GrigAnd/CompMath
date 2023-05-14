import math

equations = [
    ["x³ - 2•x - 5", lambda x: x**3 - 2*x - 5, [-5, 5]],
    ["eˣ - 5•x²", lambda x: math.exp(x) - 5*x**2, [-5, 5]],
    ["sin(x) - cos(x)", lambda x: math.sin(x) - math.cos(x), [-5, 5]],
    ["1/sqrt(x)", lambda x: 1/math.sqrt(x), [-5, 5]],
    ["1/x", lambda x: 1/x, [-5, 5]],
    ["x/|x|", lambda x: x/abs(x), [-5, 5]],
    ["1/(1-x)", lambda x: 1/(1-x), [-5, 5]],
    ]