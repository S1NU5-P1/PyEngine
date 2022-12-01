import pygame

from Engine.PlayerTwo import CirclePlayer
from Engine.CircleActor import CircleActor
from Engine.MainEngine import MainEngine
from Engine.Player import Player


class CoinActor(CircleActor):
    def __init__(self, engine: MainEngine):
        super().__init__(engine, pygame.image.load("res/Images/Coin.png"), 8)

    def Start(self):
        super().Start()

    def Update(self, seconds: float, delta_seconds: float, events: list[pygame.event]):
        super().Update(seconds, delta_seconds, events)

        for another_actor in self.collided_actors_this_frame:
            if isinstance(another_actor, Player) or isinstance(another_actor, CirclePlayer):
                print("Win!!!")


