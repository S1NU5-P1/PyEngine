import numpy as np
import pygame

from Engine.ArrowActor import ArrowActor
from Engine.CircleActor import CircleActor
from Engine.CoinActor import CoinActor
from Engine.CoopCamera import CoopCamera
from Engine.ImageActor import ImageActor
from Engine.ImageMap import ImageMap
from Engine.MainEngine import MainEngine
from Engine.Player import Player
from Engine.PlayerTwo import CirclePlayer
from Engine.SquareActor import SquareActor


def main():
    engine = MainEngine()
    tile_dict = {
        '#': SquareActor(engine, pygame.image.load("res/Images/Bricks.png")),
        ' ': ImageActor(engine, pygame.image.load("res/Images/Floor.png")),
    }

    tile_map = ImageMap(engine)
    tile_map.LoadMap("res/map1", tile_dict)
    engine.RegisterActor(tile_map)

    player_one = Player(engine)
    player_two = CirclePlayer(engine)
    camera = CoopCamera(player_one, player_two, engine)

    engine.RegisterActor(player_one)
    engine.RegisterActor(player_two)
    engine.RegisterActor(camera)

    location = 32 * tile_map.find_tile("res/map1") + np.array([16, 16])
    player_one.set_location(np.array(location))

    location = 32 * tile_map.find_tile("res/map1") + np.array([16, 16])
    player_two.set_location(location)

    location = 32 * tile_map.find_tile("res/map1") + np.array([16, 16])
    coin = CoinActor(engine)
    coin.set_location(location)
    engine.RegisterActor(coin)

    arrow = ArrowActor(engine, coin)
    engine.RegisterActor(arrow)

    engine.MainLoop()


if __name__ == "__main__":
    main()
