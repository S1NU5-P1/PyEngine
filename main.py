import numpy as np
import pygame

from Engine import Helpers
from Engine.ArrowActor import ArrowActor
from Engine.CircleActor import CircleActor
from Engine.CoinActor import CoinActor
from Engine.CoopCamera import CoopCamera
from Engine.ImageActor import ImageActor
from Engine.ImageMap import ImageMap
from Engine.MainEngine import MainEngine
from Engine.Player import Player
from Engine.PlayerTwo import CirclePlayer
from Engine.SceneManager import SceneManager
from Engine.SquareActor import SquareActor


def main():
    engine = MainEngine()
    tile_dict = {
        '#': SquareActor(engine, pygame.image.load("res/Images/Bricks.png")),
        ' ': ImageActor(engine, pygame.image.load("res/Images/Floor.png")),
    }

    tile_map = ImageMap(engine)
    engine.RegisterActor(tile_map)

    player_one = Player(engine)
    player_two = CirclePlayer(engine)
    camera = CoopCamera(player_one, player_two, engine)

    coin = CoinActor(engine)
    arrow = ArrowActor(engine, coin)

    scene_manager = SceneManager(engine, tile_map, player_one, player_two, coin)
    scene_manager.load_next_map()

    engine.RegisterActor(player_one)
    engine.RegisterActor(player_two)
    engine.RegisterActor(coin)
    engine.RegisterActor(camera)
    engine.RegisterActor(arrow)
    engine.RegisterActor(scene_manager)

    engine.MainLoop()


if __name__ == "__main__":
    main()
