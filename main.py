import numpy as np

from Engine.MainEngine import MainEngine
from Engine.Player import Player


def main():
    engine = MainEngine()
    engine.RegisterActor(Player())

    engine.MainLoop()


if __name__ == "__main__":
    main()