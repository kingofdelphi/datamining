#PYTHON 2.7

import matplotlib.pyplot as plt
from math import sqrt

def covar(a, b):
    return sum([x * y for x, y in zip(a, b)]) / float(len(a))

def pca(Dx, Dy):
    xm, ym = sum(Dx) / float(len(Dx)), sum(Dy) / float(len(Dy))
    x, y = [i - xm for i in Dx], [i - ym for i in Dy]
    cxx, cxy, cyy, var, ev = covar(x, x), covar(x, y), covar(y, y), -1, [1, 1]
    plt.gca().set_aspect("equal")
    for i in range(1000):
        ev = [cxx * ev[0] + cxy * ev[1], cxy * ev[0] + cyy * ev[1]]
        var = max(abs(ev[0]), abs(ev[1]))
        ev = [i / var for i in ev]
    m = sqrt(ev[0] ** 2 + ev[1] ** 2)
    ev = map(lambda x : x / m, ev)
    print([[cxx, cxy], [cxy, cyy]])
    print("variance", var)
    print("eigen value check", ev[0] ** 2 * cxx + 2 * ev[0] * ev[1] * cxy + ev[1] ** 2 * cyy)
    print("eigen vector", ev)
    new_points, nx, ny = [], [], [] #xXx
    plt.plot([-20 * ev[0], 20 * ev[0]], [-20 * ev[1], 20 * ev[1]])
    for i in range(len(x)):
        r = ev[0] * x[i] + ev[1] * y[i]
        new_points.append(r)
        nx += r * ev[0],
        ny += r * ev[1],
        plt.plot([x[i], r * ev[0]], [y[i], r * ev[1]], 'g')
    print("1d points", new_points)
    plt.plot(x, y, 'ro')
    plt.plot(nx, ny, 'bo')
    plt.show()

def main():
    x = [8, 9, 12, -3, 15, 3, 4, 13]
    y = [-3, 4, 15, -8, 7, 9, 20, 17]
    pca(x, y)

if __name__ == "__main__":
    main()
