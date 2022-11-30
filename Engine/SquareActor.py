import copy
import math

import numpy as np
import pygame

import Engine.Helpers as Helpers
from Engine.MainEngine import MainEngine, Actor
from Engine.ImageActor import ImageActor


class SquareActor(ImageActor):
    def __init__(self, engine: MainEngine, sprite):
        super().__init__(engine, sprite)
        self.collided_actors_this_frame = []
        self.is_static = True

    def Start(self):
        super().Start()

    def Update(self, seconds: float, delta_seconds: float, events: list[pygame.event]):
        super().Update(seconds, delta_seconds, events)

        self.collided_actors_this_frame = self.detect_collisions()

    def detect_collisions(self):
        if self.is_static:
            return

        self_width = self._surface_rect.right - self._surface_rect.left
        self_height = self._surface_rect.bottom - self._surface_rect.top

        left1 = self.get_location()[0] - self_width / 2
        right1 = self.get_location()[0] + self_width / 2
        top1 = self.get_location()[1] - self_height / 2
        bottom1 = self.get_location()[1] + self_height / 2

        collided_actors = []
        for another_actor in self._engine.get_actor_list():
            if isinstance(another_actor, SquareActor) and another_actor is not self:
                another_width = another_actor._surface_rect.right - another_actor._surface_rect.left
                another_height = another_actor._surface_rect.bottom - another_actor._surface_rect.top

                left2 = another_actor.get_location()[0] - another_width / 2
                right2 = another_actor.get_location()[0] + another_width / 2
                top2 = another_actor.get_location()[1] - another_height / 2
                bottom2 = another_actor.get_location()[1] + another_height / 2

                if right1 > left2 and right2 > left1 and \
                        bottom1 > top2 and bottom2 > top1:
                    collided_actors.append(another_actor)

        return collided_actors

    def apply_separation(self, another_actor):
        separation_vector = self.calculate_separation_vector(another_actor)
        new_position = self.get_location() + separation_vector
        self.set_location(new_position)

    def calculate_separation_vector(self, another_actor):
        self_width = self._surface_rect.right - self._surface_rect.left
        self_height = self._surface_rect.bottom - self._surface_rect.top

        another_width = another_actor._surface_rect.right - another_actor._surface_rect.left
        another_height = another_actor._surface_rect.bottom - another_actor._surface_rect.top

        left1 = self.get_location()[0] - self_width / 2
        right1 = self.get_location()[0] + self_width / 2
        top1 = self.get_location()[1] - self_height / 2
        bottom1 = self.get_location()[1] + self_height / 2

        left2 = another_actor.get_location()[0] - another_width / 2
        right2 = another_actor.get_location()[0] + another_width / 2
        top2 = another_actor.get_location()[1] - another_height / 2
        bottom2 = another_actor.get_location()[1] + another_height / 2

        left = right1 - left2
        right = right2 - left1
        top = bottom1 - top2
        bottom = bottom2 - top1

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

    def bounce(self, collided_actor):
        separation_vector = Helpers.normalize(self.calculate_circle_separation_vector(collided_actor))

        self._velocity = self._velocity - 2 * np.dot(separation_vector, self._velocity) * separation_vector
        collided_actor._velocity = collided_actor._velocity - 2 * np.dot(-separation_vector,
                                                                         collided_actor._velocity) * -separation_vector

    def __deepcopy__(self, memodict={}):
        new_copy = SquareActor(self._engine, self._surface)
        new_copy._surface_rect = self._surface_rect.copy()
        new_copy._location = copy.deepcopy(self.location)
        new_copy.is_static = self.is_static
        return new_copy
