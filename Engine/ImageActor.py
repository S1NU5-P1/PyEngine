from abc import ABC

import numpy as np
import pygame

from Engine.MainEngine import Actor, MainEngine


class ImageActor(Actor, ABC):

    def __init__(self, engine: MainEngine, surface: pygame.surface):
        super().__init__(engine)
        self._surface = surface
        self._surface_rect = surface.get_rect()

    def Start(self):
        pass

    def Update(self, seconds: float, delta_seconds: float, events: list[pygame.event]):
        size_x = self._surface_rect.right - self._surface_rect.left
        size_y = self._surface_rect.bottom - self._surface_rect.top

        if self._surface_rect.right - size_x > self._engine.get_resolution()[0] or \
                self._surface_rect.bottom - size_y > self._engine.get_resolution()[1] or \
                self._surface_rect.left < -size_x or \
                self._surface_rect.top < -size_y:
            return

        width = self._surface_rect.right - self._surface_rect.left
        height = self._surface_rect.bottom - self._surface_rect.top

        scale_x = np.ceil(width * self._engine.get_camera_scale())
        scale_y = np.ceil(height * self._engine.get_camera_scale())

        scaled_surface = pygame.transform.scale(self._surface, (scale_x, scale_y))
        self._engine.screen.blit(scaled_surface, self._surface_rect)

    def get_location(self):
        return super().get_location()

    def set_location(self, new_location: np.ndarray):
        super().set_location(new_location)

        relative_to_camera_location: np.ndarray = self.get_location() - self._engine.get_camera_location() + np.array(
            self._engine.get_resolution()) / 2.

        relative_to_camera_location = relative_to_camera_location.transpose().dot(np.identity(2) * self._engine.get_camera_scale())

        self._surface_rect.center = relative_to_camera_location.tolist()

    def __deepcopy__(self, memodict={}):
        new_copy = ImageActor(self._engine, self._surface)
        new_copy._surface_rect = self._surface_rect.copy()
        new_copy._location = self.location.copy()
        return new_copy
