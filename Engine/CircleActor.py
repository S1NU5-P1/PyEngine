import math

import numpy as np
import pygame

import Engine.Helpers as Helpers
from Engine.MainEngine import MainEngine, Actor
from Engine.ImageActor import ImageActor


class CircleActor(ImageActor):
    def __init__(self, engine: MainEngine):
        super().__init__(engine, pygame.image.load("res/Images/Circle.png"))
        self._radius = 16.
        self._velocity = np.array([0., 0.])

    def Start(self):
        super().Start()

    def Update(self, seconds: float, delta_seconds: float, events: list[pygame.event]):
        super().Update(seconds, delta_seconds, events)
        self.collide_with_screen_borders()

        new_location = self.get_location() + self._velocity * delta_seconds
        self.set_location(new_location)

        collided_actors = self.detect_collisions()
        for collided_actor in collided_actors:
            self.apply_separation(collided_actor)

    def detect_collisions(self):
        collided_actors = []
        for another_actor in self._engine.get_actor_list():
            if isinstance(another_actor, CircleActor) and another_actor is not self:
                distance = Helpers.distance(self.get_location() - another_actor.get_location())
                if distance < self._radius + another_actor._radius:
                    collided_actors.append(another_actor)

        return collided_actors

    def apply_separation(self, another_actor):
        separation_vector = self.calculate_circle_separation_vector(another_actor)
        new_position = self.get_location() +  separation_vector
        self.set_location(new_position)

    def set_velocity(self, new_velocity: np.ndarray):
        self._velocity = new_velocity

    def calculate_circle_separation_vector(self, another_actor):
        result = self.get_location() - another_actor.get_location()
        circle_distance = Helpers.distance(result)

        if circle_distance == 0:
            return np.array([0, 0])

        result /= circle_distance
        return result * (self._radius + another_actor._radius - circle_distance)

    def collide_with_screen_borders(self):
        if self.get_location()[0] + self._radius >= self._engine.get_resolution()[0]:
            if self._velocity[0] > 0:
                self._velocity[0] = -self._velocity[0]

        elif self.get_location()[0] - self._radius < 0:
            if self._velocity[0] < 0:
                self._velocity[0] = -self._velocity[0]

        if self.get_location()[1] + self._radius >= self._engine.get_resolution()[1]:
            if self._velocity[1] > 0:
                self._velocity[1] = -self._velocity[1]

        elif self.get_location()[1] - self._radius < 0:
            if self._velocity[1] < 1:
                self._velocity[1] = -self._velocity[1]
