import numpy as np
import pygame.image

from Engine.Helpers import lerp, normalize, smooth_step
from Engine.MainEngine import MainEngine
from Engine.ImageActor import ImageActor


class Player(ImageActor):
    def __init__(self, engine: MainEngine):
        super().__init__(engine, pygame.image.load("res/Images/Circle.png"))
        self.velocity = np.array([0., 0.])

        self._control_dict = {
            "up": 0.,
            "down": 0.,
            "left": 0.,
            "right": 0.,
        }

    def Start(self):
        pass

    def Update(self, seconds: float, delta_seconds: float, events: list[pygame.event]):
        super(Player, self).Update(seconds, delta_seconds, events)
        
        self.HandleInput(events)
        move_vector = np.array([self._control_dict["right"] - self._control_dict["left"],
                                self._control_dict["down"] - self._control_dict["up"]])
        move_vector = normalize(move_vector)

        acceleration = 10.
        speed = 300.

        self.velocity = lerp(self.velocity, speed * move_vector, delta_seconds * acceleration)
        print(smooth_step(0, 1, delta_seconds / 2))

        self.set_location(self.location + self.velocity * delta_seconds)

        distance_to_camera = np.linalg.norm(self.get_location() - self._engine.get_camera_location())

        camera_speed = 0.
        if distance_to_camera > 50.:
            camera_speed = 20.
        else:
            camera_speed = 8.

        new_camera_location = lerp(self._engine.get_camera_location(), self.get_location(), delta_seconds * camera_speed)

        self._engine.set_camera_location(new_camera_location)

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
