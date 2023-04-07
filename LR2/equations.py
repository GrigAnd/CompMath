import math

equations = [
    ["x³ - 2•x - 5 = 0", lambda x: x**3 - 2*x - 5, [-5, 5]],
    ["eˣ - 5•x² = 0", lambda x: math.exp(x) - 5*x**2, [-5, 5]],
    ["sin(x) - cos(x) = 0", lambda x: math.sin(x) - math.cos(x), [-5, 5]]
    ]

sys_equations = [
    [
        ["0,1x₁² + x₁ + 0,2x₂² - 0,3 = 0", lambda x1, x2: 0.1*x1**2 + x1 + 0.2*x2**2 - 0.3, [-5, 5]],
        ["0,2x₁² + x₂ + 0,1x₁x₂ - 0,7 = 0", lambda x1, x2: 0.2*x1**2 + x2 + 0.1*x1*x2 - 0.7, [-5, 5]]
    ], [
        ["sin(x₁) + cos(x₂) - 1 = 0", lambda x1, x2: math.sin(x1) + math.cos(x2) - 1, [-5, 5]],
        ["x₁ + x₂ = 0", lambda x1, x2: x1 + x2, [-5, 5]]
    ]
]