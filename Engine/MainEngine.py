import time
from abc import ABC, abstractmethod

import numpy as np
import pygame


class MainEngine:
    pass


class Actor(ABC):
    def __init__(self):
        self._location = np.array([0, 0])
        self._z = 0

    @abstractmethod
    def Start(self):
        pass

    @abstractmethod
    def Update(self, seconds: float, delta_seconds: float, engine: MainEngine, events: list[pygame.event]):
        pass

    def get_location(self):
        return self._location

    def set_location(self, new_location: np.ndarray):
        self._location = new_location

    location = property(get_location, set_location)

    def get_z(self):
        return self._z

    def set_z(self, z):
        self._z = z

    z = property(get_z, set_z)

    def __lt__(self, other):
        return self._z < other.z


class MainEngine:

    def __init__(self):
        pygame.init()
        self._resolution = [640, 480]
        self.screen = pygame.display.set_mode(self._resolution)
        pygame.display.set_caption("PyEngine")
        self._ActorList = []

    def MainLoop(self):
        should_exit = False

        start = time.perf_counter()
        seconds = 0.
        last_frame_seconds = 0.
        delta_seconds = 0.

        while not should_exit:

            seconds = time.perf_counter() - start
            delta_seconds = seconds - last_frame_seconds
            last_frame_seconds = seconds

            this_frame_events = pygame.event.get()

            for event in this_frame_events:
                if event.type == pygame.QUIT:
                    should_exit = True

            self.screen.fill((0, 0, 0))
            for actor in self._ActorList:
                actor.Update(seconds, delta_seconds, self, this_frame_events)

            fps_font = pygame.font.SysFont(None, 24)
            fps_image = fps_font.render(f"fps: {round(1 / delta_seconds)}", True, (0., 255., 0.))
            self.screen.blit(fps_image, (5, 5))

            pygame.display.update()

    def RegisterActor(self, actor: Actor):
        self._ActorList.append(actor)
        self._ActorList.sort()


class ImageActor(Actor, ABC):

    def __init__(self, surface: pygame.surface):
        super().__init__()
        self._surface = surface
        self._surface_rect = surface.get_rect()

    def Start(self):
        pass

    def Update(self, seconds: float, delta_seconds: float, engine: MainEngine, events: list[pygame.event]):
        engine.screen.blit(self._surface, self._surface_rect)

    def get_location(self):
        return super().get_location()

    def set_location(self, new_location: np.ndarray):
        super().set_location(new_location)

        self._surface_rect.center = self.get_location().tolist()

    def copy(self):
        new_copy = ImageActor(self._surface)
        new_copy._surface_rect = self._surface_rect.copy()
        new_copy._location = self.location.copy()
        return new_copy

