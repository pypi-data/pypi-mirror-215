from numpy import arange, pi, sin, cos, arccos
import matplotlib.pyplot as plt


def add_one(number):
    return number + 1


def fibo_sphere(n):
    if type(n) != int:
        raise TypeError("n must be an integer")
    if n == 0:
        return [], [], []
    goldenRatio = (1 + 5**0.5) / 2
    i = arange(0, n)
    theta = 2 * pi * i / goldenRatio
    phi = arccos(1 - 2 * (i + 0.5) / n)
    x, y, z = cos(theta) * sin(phi), sin(theta) * sin(phi), cos(phi)
    return x, y, z


def plot_fibo_sphere(n):
    x, y, z = fibo_sphere(n)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(x, y, z)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.show()
