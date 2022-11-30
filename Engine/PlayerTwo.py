import pygame.event

from Engine.MainEngine import MainEngine
from Engine.Player import Player


class PlayerTwo(Player):

    def __init__(self, engine: MainEngine):
        super().__init__(engine)
        self._surface = pygame.image.load("res/Images/Circle.png")
        self._surface_rect = self._surface.get_rect()

    def HandleInput(self, events: list[pygame.event]):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self._control_dict["up"] = 1.
                if event.key == pygame.K_DOWN:
                    self._control_dict["down"] = 1.
                if event.key == pygame.K_LEFT:
                    self._control_dict["left"] = 1.
                if event.key == pygame.K_RIGHT:
                    self._control_dict["right"] = 1.

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self._control_dict["up"] = 0.
                if event.key == pygame.K_DOWN:
                    self._control_dict["down"] = 0.
                if event.key == pygame.K_LEFT:
                    self._control_dict["left"] = 0.
                if event.key == pygame.K_RIGHT:
                    self._control_dict["right"] = 0.
