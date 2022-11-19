import math

import numpy as np


def clamp(x, minimum, maximum):
    if x > maximum:
        return maximum
    elif x < minimum:
        return minimum
    else:
        return x


def lerp(a, b, t):
    t = clamp(t, 0., 1.)
    return a + (b - a) * t


def smooth_step(a, b, t):
    t = clamp(t, 0., 1.)
    t1 = t ** 2
    t2 = 1. - (1.0 - t) * (1.0 - t)
    return lerp(a, b, lerp(t1, t2, t))


def distance(v: np.ndarray):
    return math.sqrt(v[0] ** 2 + v[1] ** 2)


def normalize(v: np.ndarray):
    norm = distance(v)
    if norm == 0:
        return v
    return v / norm
