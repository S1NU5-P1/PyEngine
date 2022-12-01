import numpy as np
import pygame

import Engine.Helpers as Helpers
from Engine.ImageActor import ImageActor
from Engine.MainEngine import MainEngine
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
        nearest_point = self.find_nearest_point(another_actor)

        if nearest_point[0] == self.location[0] and nearest_point[1] == self.location[1]:
            left = self.location[0] - another_actor.get_left() + self._radius
            right = another_actor.get_right() - self.location[0] + self._radius
            top = self.location[1] - another_actor.get_top() + self._radius
            bottom = another_actor.get_bottom() - self.location[1] + self._radius

            x = min([-left, right], key=abs)
            y = min([-top, bottom], key=abs)

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

    def find_nearest_point(self, another_actor):
        nearest_point = np.array([Helpers.clamp(self.location[0], another_actor.get_left(), another_actor.get_right()),
                                  Helpers.clamp(self.location[1], another_actor.get_top(), another_actor.get_bottom())])
        return nearest_point
