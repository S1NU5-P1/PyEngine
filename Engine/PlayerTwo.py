import pygame.event

from Engine.Player import Player


class PlayerTwo(Player):
    def HandleInput(self, events: list[pygame.event]):
        analog = [self._engine.gamepad.get_axis(0), self._engine.gamepad.get_axis(1)]
        if abs(analog[0]) > 0.4:
            if analog[0] > 0:
                self._control_dict["right"] = analog[0]
                self._control_dict["left"] = 0
            elif analog[0] < 0:
                self._control_dict["left"] = -analog[0]
                self._control_dict["right"] = 0
        else:
            self._control_dict["left"] = 0
            self._control_dict["right"] = 0

        if abs(analog[1]) > 0.4:
            if analog[1] > 0:
                self._control_dict["down"] = analog[1]
                self._control_dict["up"] = 0
            elif analog[1] < 0:
                self._control_dict["up"] = -analog[1]
                self._control_dict["down"] = 0
        else:
            self._control_dict["up"] = 0
            self._control_dict["down"] = 0
