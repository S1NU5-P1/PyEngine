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
        point_of_interest = self.player_one.get_location() + self.player_two.get_location() / 2

        camera_speed = 10.
        new_camera_location = lerp(self._engine.get_camera_location(), point_of_interest,
                                   delta_seconds * camera_speed)
        print()

        self._engine.set_camera_location(new_camera_location)
