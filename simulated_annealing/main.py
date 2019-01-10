import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.widgets import Slider, Button, TextBox

points = [(random.random() * 10, random.random() * 10) for i in range(10)]
def_order = [i for i in range(10)]
solution = []
history = []


def get_distance_for_route(order):
    distance = 0
    last_pos = points[order[0]]
    for n in order[1:]:
        distance += np.linalg.norm(np.array(points[n]) - np.array(last_pos))
        last_pos = points[n]
    return distance


def generate_new_configuration(order):
    new_order = order.copy()
    index = random.randint(0, len(new_order) - 2)
    new_order[index], new_order[index + 1] = new_order[index + 1], new_order[index]
    return new_order


def should_accept(old_cost, new_cost, temp):
    if old_cost > new_cost:
        return True
    else:
        return np.exp((old_cost - new_cost) / temp)


def simulated_annealing():
    global history, solution
    temp = 10
    min_temp = 0.0000001
    while temp > min_temp:
        new_solution = generate_new_configuration(solution)
        new_cost = get_distance_for_route(new_solution)
        old_cost = get_distance_for_route(solution)
        if should_accept(old_cost, new_cost, temp):
            solution = new_solution
        temp = 0.999 * temp
        history.append(get_distance_for_route(new_solution))


def update_plot(val):
    global points, history, solution
    points = [(x_sliders[i].val, y_sliders[i].val) for i in range(10)]
    history = []
    solution = def_order
    ax.clear()
    ax.set_title("simulated annealing")
    ax.set_xlabel("iterations")
    ax.set_ylabel("optimal route length")
    simulated_annealing()
    ax.plot(history, lw=0.5)
    solution_text.set_val(solution)


def update_map(val):
    global points
    ax.clear()
    points_ax.clear()
    solution_text.set_val("")
    points = [(x_sliders[i].val, y_sliders[i].val) for i in range(10)]
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    points_ax.scatter(xs, ys)
    for i in range(10):
        points_ax.annotate(i, (xs[i], ys[i]))


fig = plt.figure(figsize=(18, 13))
fig.canvas.set_window_title('Travelling salesman problem')
ax = fig.add_axes([0.10, 0.45, 0.8, 0.48])

x_axes = [fig.add_axes([0.03, step / 100.0, 0.27, 0.02]) for step in range(1, 40, 4)]
y_axes = [fig.add_axes([0.35, step / 100.0, 0.27, 0.02]) for step in range(1, 40, 4)]
points_ax = fig.add_axes([0.66, 0.04, 0.28, 0.28])
points_ax.set_xlim((0, 10))
points_ax.set_ylim((0, 10))
points_ax.set_aspect(1)

button_ax = fig.add_axes([0.66, 0.34, 0.06, 0.06])
button = Button(button_ax, "Count")
button.on_clicked(update_plot)

solution_ax = fig.add_axes([0.79, 0.34, 0.20, 0.06])
solution_text = TextBox(solution_ax, 'Best path')

x_sliders = [Slider(x_axes[i], 'x{}'.format(i), 0., 10., valinit=points[i][0]) for i in range(10)]
y_sliders = [Slider(y_axes[i], 'y{}'.format(i), 0., 10., valinit=points[i][1]) for i in range(10)]
for slider in x_sliders + y_sliders:
    slider.on_changed(update_map)

update_map(None)
plt.show()
