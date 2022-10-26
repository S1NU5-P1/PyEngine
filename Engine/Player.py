import numpy as np
import pygame.image

from Engine.Helpers import lerp, normalize
from Engine.MainEngine import MainEngine, ImageActor


class Player(ImageActor):
    def __init__(self):
        super().__init__(pygame.image.load("res/Images/Circle.png"))
        self.velocity = np.array([0., 0.])

        self._control_dict = {
            "up": 0.,
            "down": 0.,
            "left": 0.,
            "right": 0.,
        }

    def Start(self):
        pass

    def Update(self, seconds: float, delta_seconds: float, engine: MainEngine, events: list[pygame.event]):
        super(Player, self).Update(seconds, delta_seconds, engine, events)
        
        self.HandleInput(events)
        move_vector = np.array([self._control_dict["right"] - self._control_dict["left"],
                                self._control_dict["down"] - self._control_dict["up"]])
        move_vector = normalize(move_vector)

        acceleration = 10.
        speed = 300.

        self.velocity = lerp(self.velocity, speed * move_vector, delta_seconds * acceleration)

        self.set_location(self.location + self.velocity * delta_seconds)

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
