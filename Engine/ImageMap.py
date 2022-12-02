import copy
import random
from abc import ABC

import numpy as np
import pygame

from Engine.MainEngine import Actor, MainEngine
from Engine.ImageActor import ImageActor
from Engine.SquareActor import SquareActor


class ImageMap(Actor, ABC):

    def __init__(self, engine: MainEngine):
        super().__init__(engine)
        self._tiles = []
        self.z = -100

    def LoadMap(self, path: str, tile_dict: dict[str, ImageActor], tile_x=32, tile_y=32):
        self.remove_tiles()

        with open(path) as map_file:
            for line_number, line in enumerate(map_file.readlines()):
                for character_number, character in enumerate(line):
                    if character == "\n":
                        continue

                    new_tile: SquareActor = copy.deepcopy(tile_dict[character])
                    new_tile.z = self.z
                    new_location = np.array([tile_x * character_number + tile_x / 2., tile_y * line_number + tile_y / 2.])
                    new_tile.set_location(new_location)
                    self._tiles.append(new_tile)
                    self._engine.RegisterActor(new_tile)

    def remove_tiles(self):
        for tile in self._tiles:
            try:
                self._engine.get_actor_list().remove(tile)
            except ValueError:
                continue

        self._tiles.clear()

    def Start(self):
        pass

    def Update(self, seconds: float, delta_seconds: float, events: list[pygame.event]):
        pass

    def set_location(self, new_location: np.ndarray):
        for tile in self._tiles:
            tile.set_location(tile.get_location())

    def find_tile(self, path: str, target_character=' '):
        found_tiles_locations = []

        with open(path) as map_file:
            for line_number, line in enumerate(map_file.readlines()):
                for character_number, character in enumerate(line):
                    if character == "\n":
                        continue

                    if character == target_character:
                        found_tiles_locations.append(np.array([character_number, line_number]))

        return random.choice(found_tiles_locations)
