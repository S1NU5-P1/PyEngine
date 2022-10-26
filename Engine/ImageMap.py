from abc import ABC
from copy import copy, deepcopy

import numpy as np
import pygame

from Engine.MainEngine import Actor, MainEngine, ImageActor


class ImageMap(Actor, ABC):

    def __init__(self):
        super().__init__()
        self._tiles = []
        self.z = -100;

    def LoadMap(self, path: str, tile_dict: dict[str, ImageActor], tile_x=32, tile_y=32):
        with open(path) as map_file:
            for line_number, line in enumerate(map_file.readlines()):
                for character_number, character in enumerate(line):
                    if character == "\n":
                        continue

                    new_tile: ImageActor = tile_dict[character].copy()
                    new_tile.z = self.z
                    new_tile.set_location(np.array([tile_x * character_number + tile_x / 2,
                                                    tile_y * line_number + tile_y / 2]))
                    self._tiles.append(new_tile)

    def Start(self):
        for tile in self._tiles:
            tile.Start()

    def Update(self, seconds: float, delta_seconds: float, engine: MainEngine, events: list[pygame.event]):
        for tile in self._tiles:
            tile.Update(seconds, delta_seconds, engine, events)
