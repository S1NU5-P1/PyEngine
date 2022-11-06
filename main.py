import pygame

from Engine.CoopCamera import CoopCamera
from Engine.ImageActor import ImageActor
from Engine.ImageMap import ImageMap
from Engine.MainEngine import MainEngine
from Engine.Player import Player
from Engine.PlayerTwo import PlayerTwo


def main():
    engine = MainEngine()

    tile_dict = {
        "#": ImageActor(engine, pygame.image.load("res/Images/Bricks.png")),
        "*": ImageActor(engine, pygame.image.load("res/Images/Floor.png"))
    }

    player_one = Player(engine)
    player_two = PlayerTwo(engine)
    camera = CoopCamera(player_one, player_two, engine)

    engine.RegisterActor(player_one)
    engine.RegisterActor(player_two)
    engine.RegisterActor(camera)

    image_map = ImageMap(engine)
    image_map.LoadMap("res/map", tile_dict)

    engine.RegisterActor(image_map)

    engine.set_camera_location([100, 100])
    engine.MainLoop()


if __name__ == "__main__":
    main()
