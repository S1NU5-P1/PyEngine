import copy

import numpy as np
import pygame

from Engine.ImageActor import ImageActor
from Engine.MainEngine import MainEngine


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

        collided_actors = []
        for another_actor in self._engine.get_actor_list():
            if isinstance(another_actor, SquareActor) and another_actor is not self:
                if self.get_right() > another_actor.get_left() and another_actor.get_right() > self.get_left() and \
                        self.get_bottom() > another_actor.get_top() and another_actor.get_bottom() > self.get_top():
                    collided_actors.append(another_actor)

        return collided_actors

    def apply_separation(self, another_actor):
        separation_vector = self.calculate_separation_vector(another_actor)
        new_position = self.get_location() + separation_vector
        self.set_location(new_position)

    def calculate_separation_vector(self, another_actor):
        left = self.get_right() - another_actor.get_left()
        right = another_actor.get_right() - self.get_left()
        top = self.get_bottom() - another_actor.get_top()
        bottom = another_actor.get_bottom() - self.get_top()

        x = min([-left, right], key=abs)
        y = min([-top, bottom], key=abs)

        if abs(x) > abs(y):
            x = 0
        else:
            y = 0

        return np.array([x, y])

    def __deepcopy__(self, memodict={}):
        new_copy = SquareActor(self._engine, self._surface)
        new_copy._surface_rect = self._surface_rect.copy()
        new_copy._location = copy.deepcopy(self.location)
        new_copy.is_static = self.is_static
        return new_copy

    def get_width(self) -> float:
        return self._surface_rect.right - self._surface_rect.left

    def get_height(self) -> float:
        return self._surface_rect.bottom - self._surface_rect.top

    def get_left(self) -> float:
        return self.get_location()[0] - self.get_width() / 2

    def get_right(self) -> float:
        return self.get_location()[0] + self.get_width() / 2

    def get_top(self) -> float:
        return self.get_location()[1] - self.get_height() / 2

    def get_bottom(self) -> float:
        return self.get_location()[1] + self.get_height() / 2
