import numpy as np
import pygame

from Engine.Helpers import lerp
from Engine.MainEngine import Actor, MainEngine
from Engine.Player import Player


class CoopCamera(Actor):
    def __init__(self, player_one: Player, player_two: Player, engine: MainEngine):
        super().__init__(engine)
        self.player_one = player_one
        self.player_two = player_two

    def Start(self):
        pass

    def Update(self, seconds: float, delta_seconds: float, events: list[pygame.event]):
        point_of_interest = (self.player_one.get_location() + self.player_two.get_location()) / 2

        camera_speed = 10.
        camera_resolution = self._engine.get_resolution()
        point_of_interest += np.array([camera_resolution[0] * (self._engine.get_camera_scale() - 1),
                                       camera_resolution[1] * (self._engine.get_camera_scale() - 1)])

        new_camera_location = lerp(self._engine.get_camera_location(), point_of_interest, delta_seconds * camera_speed)
        target_camera_scale = np.linalg.norm(self.player_one.get_location() - self.player_two.get_location()) / 300
        target_camera_scale = max(1, target_camera_scale)
        target_camera_scale = 1 / target_camera_scale

        new_camera_scale = lerp(self._engine.get_camera_scale(), target_camera_scale, delta_seconds * camera_speed)

        self._engine.set_camera_location(new_camera_location)
        self._engine.set_camera_scale(new_camera_scale)
