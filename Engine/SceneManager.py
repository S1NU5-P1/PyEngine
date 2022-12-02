import numpy as np
import pygame

from Engine import Helpers
from Engine.ImageActor import ImageActor
from Engine.MainEngine import Actor, MainEngine
from Engine.SquareActor import SquareActor


class SceneManager(Actor):
    def __init__(self, engine: MainEngine, image_map, player_one, player_two, coin_actor):
        super().__init__(engine)
        self._image_map = image_map

        self.tile_dict = {
            '#': SquareActor(engine, pygame.image.load("res/Images/Bricks.png")),
            ' ': ImageActor(engine, pygame.image.load("res/Images/Floor.png")),
        }
        self.map_list = ["res/map", "res/map1", "res/map2", "res/map2"]

        self.map_index = 0
        self._player_one = player_one
        self._player_two = player_two
        self._coin_actor = coin_actor

    def Start(self):
        pass

    def Update(self, seconds: float, delta_seconds: float, events: list[pygame.event]):
        pass

    def load_next_map(self):
        map_path = self.map_list[self.map_index]
        self._image_map.LoadMap(map_path, self.tile_dict)

        location_one = 32 * self._image_map.find_tile(map_path) + np.array([16, 16])
        self._player_one.set_location(location_one)

        location_two = 32 * self._image_map.find_tile(map_path) + np.array([16, 16])
        while Helpers.distance(location_two - location_one) > 300:
            location_two = 32 * self._image_map.find_tile(map_path) + np.array([16, 16])

        self._player_two.set_location(location_two)

        coin_location = 32 * self._image_map.find_tile(map_path) + np.array([16, 16])
        while Helpers.distance(coin_location - location_two) < 100 or Helpers.distance(coin_location - location_one) < 100:
            coin_location = 32 * self._image_map.find_tile(map_path) + np.array([16, 16])

        self._coin_actor.set_location(coin_location)

        if self.map_index + 1 < len(self.map_list):
            self.map_index += 1
        else:
            self.map_index = 0

        self._engine.is_map_loaded_this_frame = True
