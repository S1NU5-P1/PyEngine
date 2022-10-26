import numpy as np


def lerp(a, b, t):
    return a + (b - a) * t


def normalize(v: np.ndarray):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm
