import pygame

from Engine.ImageMap import ImageMap
from Engine.MainEngine import MainEngine, ImageActor
from Engine.Player import Player


def main():
    tile_dict = {
        "#": ImageActor(pygame.image.load("res/Images/Bricks.png")),
        "*": ImageActor(pygame.image.load("res/Images/Floor.png"))
    }

    engine = MainEngine()
    engine.RegisterActor(Player())

    image_map = ImageMap()
    image_map.LoadMap("res/map", tile_dict)

    engine.RegisterActor(image_map)

    engine.MainLoop()


if __name__ == "__main__":
    main()
