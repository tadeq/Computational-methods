import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider


def lorenz_attractor(x0=0, y0=1., z0=1.05, a=10, b=2.667, c=28):
    rk4 = True

    h = 0.01
    step_cnt = 10000

    xs = np.empty((step_cnt + 1,))
    ys = np.empty((step_cnt + 1,))
    zs = np.empty((step_cnt + 1,))

    xs[0], ys[0], zs[0] = (x0, y0, z0)

    if not rk4:
        for i in range(step_cnt):
            der_x = a * (ys[i] - xs[i])
            der_y = c * xs[i] - ys[i] - xs[i] * zs[i]
            der_z = xs[i] * ys[i] - b * zs[i]
            xs[i + 1] = xs[i] + (der_x * h)
            ys[i + 1] = ys[i] + (der_y * h)
            zs[i + 1] = zs[i] + (der_z * h)
        return xs, ys, zs

    else:
        def f1(x, y):
            return a * (y - x)

        def f2(x, y, z):
            return c * x - y - x * z

        def f3(x, y, z):
            return x * y - b * z

        for i in range(step_cnt):
            k1 = f1(xs[i], ys[i])
            l1 = f2(xs[i], ys[i], zs[i])
            m1 = f3(xs[i], ys[i], zs[i])
            k2 = f1(xs[i] + 0.5 * k1 * h, ys[i] + 0.5 * l1 * h)
            l2 = f2(xs[i] + 0.5 * k1 * h, ys[i] + 0.5 * l1 * h, zs[i] + 0.5 * m1 * h)
            m2 = f3(xs[i] + 0.5 * k1 * h, ys[i] + 0.5 * l1 * h, zs[i] + 0.5 * m1 * h)
            k3 = f1(xs[i] + 0.5 * k2 * h, ys[i] + 0.5 * l2 * h)
            l3 = f2(xs[i] + 0.5 * k2 * h, ys[i] + 0.5 * l2 * h, zs[i] + 0.5 * m2 * h)
            m3 = f3(xs[i] + 0.5 * k2 * h, ys[i] + 0.5 * l2 * h, zs[i] + 0.5 * m2 * h)
            k4 = f1(xs[i] + k3 * h, ys[i] + l3 * h)
            l4 = f2(xs[i] + k3 * h, ys[i] + l3 * h, zs[i] + m3 * h)
            m4 = f3(xs[i] + k3 * h, ys[i] + l3 * h, zs[i] + m3 * h)
            xs[i + 1] = xs[i] + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
            ys[i + 1] = ys[i] + h * (l1 + 2 * l2 + 2 * l3 + l4) / 6
            zs[i + 1] = zs[i] + h * (m1 + 2 * m2 + 2 * m3 + m4) / 6

        return xs, ys, zs


xs, ys, zs = lorenz_attractor()
fig = plt.figure("Lorenz attractor")
ax = fig.add_axes([0.10, 0.35, 0.8, 0.6], projection='3d')

ax.plot(xs, ys, zs, lw=0.7)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.set_title("Lorenz Attractor")

a = fig.add_axes([0.05, 0.11, 0.65, 0.03])
b = fig.add_axes([0.05, 0.06, 0.65, 0.03])
c = fig.add_axes([0.05, 0.01, 0.65, 0.03])
x0 = fig.add_axes([0.05, 0.29, 0.65, 0.03])
y0 = fig.add_axes([0.05, 0.24, 0.65, 0.03])
z0 = fig.add_axes([0.05, 0.19, 0.65, 0.03])

a_sl = Slider(a, 'a', 0.0, 25.0, valinit=10.)
b_sl = Slider(b, 'b', 0.0, 10.0, valinit=2.667)
c_sl = Slider(c, 'c', 0.0, 40.0, valinit=28.)
x0_sl = Slider(x0, 'x0', 0., 2., valinit=0.)
y0_sl = Slider(y0, 'y0', 0., 2., valinit=1.)
z0_sl = Slider(z0, 'z0', 0., 2., valinit=1.05)


def update(val):
    ax.clear()
    xs, ys, zs = lorenz_attractor(x0_sl.val, y0_sl.val, z0_sl.val, a_sl.val, b_sl.val, c_sl.val)
    ax.plot(xs, ys, zs, lw=0.7)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_title("Lorenz Attractor")


sliders = [a_sl, b_sl, c_sl, x0_sl, y0_sl, z0_sl]
for slider in sliders:
    slider.on_changed(update)

plt.show()
