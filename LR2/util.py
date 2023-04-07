import numpy as np
import matplotlib.pyplot as plt

def draw(equation, a, b):
    x = np.linspace(a, b, 1000)
    y = np.vectorize(equation)(x)

    plt.plot(x, y)
    plt.grid()
    plt.show()

def draw_system(equation1, equation2, a, b):
    x = np.linspace(a, b, 100)
    y = np.linspace(a, b, 100)

    X, Y = np.meshgrid(x, y)

    plt.contour(X, Y, np.vectorize(equation1)(X,Y), levels=[0], colors=['blue'])
    plt.contour(X, Y, np.vectorize(equation2)(X,Y), levels=[0], colors=['red'])
    plt.grid()
    plt.show()

def save_to_file(name, content):
    with open(name, "w", encoding="utf-8") as file:
        for line in content:
            file.write(str(line[0]) + " " + str(line[1]) + "\n")