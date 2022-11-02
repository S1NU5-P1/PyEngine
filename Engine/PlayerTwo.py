import pygame.event

from Engine.Player import Player


class PlayerTwo(Player):
    def HandleInput(self, events: list[pygame.event]):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self._control_dict["up"] = 1.
                if event.key == pygame.K_s:
                    self._control_dict["down"] = 1.
                if event.key == pygame.K_a:
                    self._control_dict["left"] = 1.
                if event.key == pygame.K_d:
                    self._control_dict["right"] = 1.

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self._control_dict["up"] = 0.
                if event.key == pygame.K_s:
                    self._control_dict["down"] = 0.
                if event.key == pygame.K_a:
                    self._control_dict["left"] = 0.
                if event.key == pygame.K_d:
                    self._control_dict["right"] = 0.
