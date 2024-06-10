import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from coef_f import *

def fern(num_points, coef, method):
    x = np.zeros(num_points)
    y = np.zeros(num_points)

    funcs = []
    probabilities = []

    for coeffs in coef:
        a, b, c, d, e, f, p = coeffs
        if method == 1:
            func = lambda x, y, a=a, b=b, c=c, d=d, e=e, f=f: (a * x + b * y + e, c * x + d * y + f)
        else:
            func = lambda x, y, a=a, b=b, c=c, d=d, e=e, f=f: (
            a * np.cos(c) * x - b * np.sin(d) * y + e, a * np.sin(c) * x + b * np.cos(d) * y + f)
        funcs.append(func)
        probabilities.append(p)

    probabilities = np.array(probabilities)
    p_cumulative = np.cumsum(probabilities)

    for i in range(1, num_points):
        r = np.random.random()
        func_index = np.searchsorted(p_cumulative, r)
        func = funcs[func_index]
        x[i], y[i] = func(x[i - 1], y[i - 1])

    return x, y


def update(frame, x, y, scatter):
    scatter.set_offsets(np.c_[x[:frame], y[:frame]])
    return scatter,


def create_animation(num_points, coef_data, method, iterations, output_filename):
    x, y = fern(num_points, coef_data, method)

    fig, ax = plt.subplots(figsize=(10, 10))
    scatter = ax.scatter([], [], s=0.1, color='green')
    ax.set_xlim(min(x), max(x))
    ax.set_ylim(min(y), max(y))
    ax.set_title("Fractal Fern")

    animation = FuncAnimation(fig, update, frames=np.arange(0, num_points, num_points // iterations),
                              fargs=(x, y, scatter), interval=400, blit=True)

    animation.save(output_filename, writer=PillowWriter(fps=30))
    plt.show()


# Параметри
num_points = 100000
iterations = 10
method = 1
coeff_data = [
    [0.1400, 0.0100, 0.0000, 0.5100, -0.0800, -1.3100, 0.25],
    [0.4300, 0.5200, -0.4500, 0.5000, 1.4900, -0.7500, 0.25],
    [0.4500, -0.4900, 0.4700, 0.4700, -1.6200, -0.7400, 0.25],
    [0.4900, 0.0000, 0.0000, 0.5100, 0.0200, 1.6200, 0.25]
]

output_filenames = {
    'Кленовий_лист.gif': f_1_4_1,
    'Спіраль.gif': f_1_4_2,
    'Mandelbrot_like.gif': f_1_4_3,
    'Фрактальне_дерево.gif': f_1_4_4,
    'III_фрактального_дерева.gif': f_1_4_6,
    'IIII_фрактального_дерева.gif': f_1_4_7,
    'Фрактальний_лист.gif': f_1_4_8,
    'Пісочний_долар_сніжинка.gif': f_1_4_9,
    'Фрактал_папороті.gif': f_1_4_10,
    'інший.gif': f_1_5,
    'IFS_Chaos_Text.gif': f_1_5_1,
    'IFS_Dragon.gif': f_1_5_2,
    'IFS_Гілка.gif': f_1_5_3,
    'IFS_Ялинка.gif': f_1_5_4,
    'MY_F1.gif': f_1,
    'MY_F2.gif': f_2,
    'MY_F3.gif': f_3
}

# Створення анімації
for key, value in output_filenames.items():
    create_animation(num_points, value, method, iterations, key)
else:
    create_animation(num_points, f_1_4_5, method, iterations, 'II_фрактального_дерева.gif')
