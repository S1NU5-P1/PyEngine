import copy
import math

import numpy as np
import pygame

from Engine import Helpers
from Engine.CoinActor import CoinActor
from Engine.ImageActor import ImageActor
from Engine.MainEngine import MainEngine


class ArrowActor(ImageActor):
    def __init__(self, engine: MainEngine, coin: CoinActor):
        super().__init__(engine, pygame.image.load("res/Images/Arrow.png"))
        self._default_surface = self._surface
        self._coin = coin

    def Start(self):
        super().Start()

    def Update(self, seconds: float, delta_seconds: float, events: list[pygame.event]):
        super().Update(seconds, delta_seconds, events)
        self._surface = pygame.transform.rotate(self._default_surface, 90)
        target_location = copy.copy(self._engine.get_camera_location())
        # target_location -= np.array([640 * (self._engine.get_camera_scale() - 1),
        #                              480 * (self._engine.get_camera_scale() - 1)])
        self.set_location(target_location)

        target_angle = np.dot(Helpers.normalize(self.get_location() - self._coin.get_location()), np.array([1, 0]))

        if self.get_location()[1] < self._coin.get_location()[1]:
            target_angle = math.degrees(np.arccos(target_angle)) + 180
            self._surface = pygame.transform.rotate(self._default_surface, target_angle)
        else:
            target_angle = math.degrees(np.arccos(target_angle))
            self._surface = pygame.transform.rotate(self._default_surface, target_angle)
            self._surface = pygame.transform.flip(self._surface, True, False)


