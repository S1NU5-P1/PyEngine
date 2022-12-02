import pygame

from Engine.CircleActor import CircleActor
from Engine.MainEngine import MainEngine
from Engine.Player import Player
from Engine.PlayerTwo import CirclePlayer
from Engine.SceneManager import SceneManager


class CoinActor(CircleActor):
    def __init__(self, engine: MainEngine):
        super().__init__(engine, pygame.image.load("res/Images/Coin.png"), 8)

    def Start(self):
        super().Start()

    def Update(self, seconds: float, delta_seconds: float, events: list[pygame.event]):
        super().Update(seconds, delta_seconds, events)

        for another_actor in self.collided_actors_this_frame:
            if isinstance(another_actor, Player) or isinstance(another_actor, CirclePlayer):
                for actor in self._engine.get_actor_list():
                    if isinstance(actor, SceneManager):
                        actor.load_next_map()
                        self.collided_actors_this_frame.clear()
                        break
