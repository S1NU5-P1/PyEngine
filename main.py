import math
import random

import numpy as np
import pygame
from Engine.MainEngine import MainEngine
from Engine.CircleActor import CircleActor


def main():
    engine = MainEngine()

    for i in range(50):
        circle = CircleActor(engine)
        circle.set_location(np.array([random.randrange(50, 600), random.randrange(50, 420)]))
        direction_vector = np.array([math.sin(random.uniform(-math.pi, math.pi)),
                                     math.cos(random.uniform(-math.pi, math.pi))]) * 150
        circle.set_velocity(direction_vector)
        engine.RegisterActor(circle)

    engine.MainLoop()


if __name__ == "__main__":
    main()
