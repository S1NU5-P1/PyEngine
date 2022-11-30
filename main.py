import math
import random

import numpy as np
import pygame
from Engine.ImageMap import ImageMap
from Engine.MainEngine import MainEngine
from Engine.ImageActor import ImageActor
from Engine.Player import Player
from Engine.PlayerTwo import PlayerTwo
from Engine.CoopCamera import CoopCamera


def main():
    engine = MainEngine()
    tile_dict = {
        '#': ImageActor(engine, pygame.image.load("res/Images/Bricks.png")),
        ' ': ImageActor(engine, pygame.image.load("res/Images/Floor.png")),
    }

    tile_map = ImageMap(engine)
    tile_map.LoadMap("res/map", tile_dict)

    engine.RegisterActor(tile_map)

    player_one = Player(engine)
    player_two = PlayerTwo(engine)
    camera = CoopCamera(player_one, player_two, engine)

    engine.RegisterActor(player_one)
    engine.RegisterActor(player_two)
    engine.RegisterActor(camera)

    engine.MainLoop()


if __name__ == "__main__":
    main()
