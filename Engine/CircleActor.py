import math

import numpy as np
import pygame

import Engine.Helpers as Helpers
from Engine.MainEngine import MainEngine, Actor
from Engine.ImageActor import ImageActor
from Engine.SquareActor import SquareActor


class CircleActor(ImageActor):
    def __init__(self, engine: MainEngine, sprite, radius):
        super().__init__(engine, sprite)
        self.collided_actors_this_frame = []
        self._radius = radius

    def Start(self):
        super().Start()

    def Update(self, seconds: float, delta_seconds: float, events: list[pygame.event]):
        super().Update(seconds, delta_seconds, events)

        self.collided_actors_this_frame = self.detect_collisions()

    def detect_collisions(self):
        collided_actors = []
        for another_actor in self._engine.get_actor_list():
            if isinstance(another_actor, CircleActor) and another_actor is not self:
                self.detect_circle_collision(another_actor, collided_actors)
            if isinstance(another_actor, SquareActor) and another_actor is not self:
                self.detect_square_collision(another_actor, collided_actors)

        return collided_actors

    def detect_circle_collision(self, another_actor, collided_actors):
        distance = Helpers.distance(self.get_location() - another_actor.get_location())
        if distance < self._radius + another_actor._radius:
            collided_actors.append(another_actor)

    def detect_square_collision(self, another_actor, collided_actors):
        another_width = another_actor._surface_rect.right - another_actor._surface_rect.left
        another_height = another_actor._surface_rect.bottom - another_actor._surface_rect.top

        left = another_actor.get_location()[0] - another_width / 2
        right = another_actor.get_location()[0] + another_width / 2
        top = another_actor.get_location()[1] - another_height / 2
        bottom = another_actor.get_location()[1] + another_height / 2

        nearest_point = np.array([Helpers.clamp(self.location[0], left, right),
                                 Helpers.clamp(self.location[1], top, bottom)])

        if Helpers.distance(self.location - nearest_point) < self._radius:
            collided_actors.append(another_actor)

    def apply_separation(self, another_actor):
        separation_vector = self.calculate_circle_separation_vector(another_actor)
        new_position = self.get_location() + separation_vector
        self.set_location(new_position)

    def set_velocity(self, new_velocity: np.ndarray):
        self._velocity = new_velocity

    def calculate_circle_separation_vector(self, another_actor):
        if isinstance(another_actor, CircleActor):
            return self.calculate_separation_vector_for_circle(another_actor)
        elif isinstance(another_actor, SquareActor):
            return self.calculate_separation_vector_for_square(another_actor)

    def calculate_separation_vector_for_circle(self, another_actor):
        result = self.get_location() - another_actor.get_location()
        circle_distance = Helpers.distance(result)
        if circle_distance == 0:
            return np.array([0, 0])
        result /= circle_distance
        return result * (self._radius + another_actor._radius - circle_distance)

    def calculate_separation_vector_for_square(self, another_actor):
        another_width = another_actor._surface_rect.right - another_actor._surface_rect.left
        another_height = another_actor._surface_rect.bottom - another_actor._surface_rect.top

        left2 = another_actor.get_location()[0] - another_width / 2
        right2 = another_actor.get_location()[0] + another_width / 2
        top2 = another_actor.get_location()[1] - another_height / 2
        bottom2 = another_actor.get_location()[1] + another_height / 2

        nearest_point = np.array([Helpers.clamp(self.location[0], left2, right2),
                                 Helpers.clamp(self.location[1], top2, bottom2)])

        if nearest_point[0] == self.location[0] and nearest_point[1] == self.location[1] :
            another_width = another_actor._surface_rect.right - another_actor._surface_rect.left
            another_height = another_actor._surface_rect.bottom - another_actor._surface_rect.top

            left2 = another_actor.get_location()[0] - another_width / 2
            right2 = another_actor.get_location()[0] + another_width / 2
            top2 = another_actor.get_location()[1] - another_height / 2
            bottom2 = another_actor.get_location()[1] + another_height / 2

            left = self.location[0] - left2 + self._radius
            right = right2 - self.location[0] + self._radius
            top = self.location[1] - top2 + self._radius
            bottom = bottom2 - self.location[1] + self._radius

            x = 0
            if left < right:
                x = -left
            else:
                x = right

            y = 0
            if top < bottom:
                y = -top
            else:
                y = bottom

            if abs(x) > abs(y):
                x = 0
            else:
                y = 0

            return np.array([x, y])
        else:
            result = self.get_location() - nearest_point
            circle_distance = Helpers.distance(result)
            if circle_distance == 0:
                return np.array([0, 0])
            result /= circle_distance
            return result * (self._radius - circle_distance)

    def bounce(self, collided_actor):
        separation_vector = Helpers.normalize(self.calculate_circle_separation_vector(collided_actor))

        self._velocity = self._velocity - 2 * np.dot(separation_vector, self._velocity) * separation_vector
        collided_actor._velocity = collided_actor._velocity - 2 * np.dot(-separation_vector,
                                                                         collided_actor._velocity) * -separation_vector
