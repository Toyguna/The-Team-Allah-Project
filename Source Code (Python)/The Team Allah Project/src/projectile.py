import pygame
import math
import numpy as np

import util.settings as SETTINGS

class AllyProjectile:
    def __init__(self, display: pygame.Surface, origin: tuple[int, int], type: int) -> None:
        """
        ``type``: positive -> focusing, negative -> non-focusing
        """
        
        self.display = display
        self.rect = pygame.Rect(origin, (0, 0))
 
        self.type = type
        self.speed = 0

        self.image = None

        if self.type == 1:
            self.rect.size = SETTINGS.FALPROJ_WIDTH, SETTINGS.FALPROJ_HEIGHT
            self.speed = SETTINGS.FALPROJ_SPEED
        elif self.type == -1:
            self.rect.size = SETTINGS.NALPROJ_WIDTH, SETTINGS.NALPROJ_HEIGHT
            self.speed = SETTINGS.NALPROJ_SPEED
        elif self.type == 2:
            pass
        elif self.type == -2:
            pass
        else:
            KeyError(f"``self.type`` cannot be {self.type}")

    def update(self):
        if self.type in [2, 1, -1]:
            self.rect.y -= self.speed

    def draw(self):
        #self.display.blit(self.image)
        pygame.draw.rect(self.display, "red", self.rect)


class EnemyProjectile:
    def __init__(self, display: pygame.Surface, rect: pygame.Rect, image: pygame.Surface = None,
            attr: dict = None) -> None:
        self.display = display
        self.rect = rect
        self.attr = attr

        if attr is not None:
            self.speed = attr["speed"] if "speed" in attr else 1.5
        else:
            self.speed = 1.5

        self.image = image

    def update(self):
        pass

    def draw(self):
        if self.image is None:
            pygame.draw.rect(self.display, "red", self.rect)
        else:
            self.display.blit(self.image, self.rect.topleft)


class CurveProjectile(EnemyProjectile):
    def __init__(self, display: pygame.Surface, rect: pygame.Rect, image: pygame.Surface = None,
            attr: dict = None) -> None:
        super().__init__(display, rect, image, attr)


        self.angle = 0

    def update(self):
        self.angle += 1

        angle2 = self.angle * math.pi / 180
        print(angle2)

        self.rect.x += np.ceil(math.sin(angle2))
        self.rect.y += -math.cos(angle2)
        
        if self.angle > 360:
            self.angle = 0


class ForwardProjectile(EnemyProjectile):
    def __init__(self, display: pygame.Surface, rect: pygame.Rect, image: pygame.Surface = None,
            attr: dict = None) -> None:
        super().__init__(display, rect, image, attr)

    def update(self):
        pass


class AlertProjectile(EnemyProjectile):
    def __init__(self, display: pygame.Surface, rect: pygame.Rect, image: pygame.Surface = None,
            attr: dict = None) -> None:
        super().__init__(display, rect, image, attr)

        if attr is not None:
            self.activation_delay = attr["activation_delay"] if "activation_delay" in attr else 300
            self.duration = attr["duration"] if "duration" in attr else 150

        else:
            self.activation_delay = 300
            self.duration = 150

        self.total_duration = self.activation_delay + self.duration

        self.counter = 0

        self.activated = False

    def update(self):
        if self.total_duration > self.counter:
            self.counter += 1

            if self.activation_delay == self.counter:
                self.fire()

    def fire(self):
        self.activated = True

    def draw(self):
        if self.activated:
            pygame.draw.rect(self.display, "red", self.rect)
        else:
            pygame.draw.rect(self.display, "yellow", self.rect)