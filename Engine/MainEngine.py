import time
from abc import ABC, abstractmethod

import numpy as np
import pygame


class Actor:
    pass


class MainEngine:

    def __init__(self):
        pygame.init()
        self._resolution = [640, 480]
        self.screen = pygame.display.set_mode(self._resolution)
        self._ActorList: list[Actor] = []
        self._camera_location = np.array(self._resolution) / 2.
        self._camera_scale = 1.

        self.is_separation_active = True
        self.is_bouncing_active = True

        pygame.display.set_caption("PyEngine")

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
                actor.Update(seconds, delta_seconds, this_frame_events)

            fps_font = pygame.font.SysFont("", 24)
            fps_image = fps_font.render(f"fps: {round(1 / delta_seconds)}", True, (0., 255., 0.))
            self.screen.blit(fps_image, (5, 5))

            hud_image = fps_font.render(f"Bounce: {self.is_bouncing_active}", True, (0., 255., 0.))
            self.screen.blit(hud_image, (5, 28))

            hud_image = fps_font.render(f"Separation: {self.is_separation_active}", True, (0., 255., 0.))
            self.screen.blit(hud_image, (5, 50))

            for event in this_frame_events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.is_bouncing_active = not self.is_bouncing_active
                    if event.key == pygame.K_2:
                        self.is_separation_active = not self.is_separation_active

            pygame.display.update()

    def RegisterActor(self, actor: Actor):
        self._ActorList.append(actor)
        self._ActorList.sort()

    def get_resolution(self):
        return self._resolution

    def get_camera_location(self):
        return self._camera_location

    def set_camera_location(self, camera):
        self._camera_location = camera

        for actor in self._ActorList:
            actor.set_location(actor.get_location())

    def get_camera_scale(self):
        return self._camera_scale

    def set_camera_scale(self, scale):
        self._camera_scale = scale

        for actor in self._ActorList:
            actor.set_location(actor.get_location())

    def get_actor_list(self):
        return self._ActorList


class Actor(ABC):
    def __init__(self, engine: MainEngine):
        self._location = np.array([0, 0])
        self._z = 0
        self._engine = engine

    @abstractmethod
    def Start(self):
        pass

    @abstractmethod
    def Update(self, seconds: float, delta_seconds: float, events: list[pygame.event]):
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
