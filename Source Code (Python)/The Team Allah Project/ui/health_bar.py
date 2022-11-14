import pygame

class HealthBar:
    def __init__(self, display: pygame.Surface, rect: pygame.Rect, max: int, value: int = 0) -> None:
        self.display = display

        self.bg_rect = rect
        self.fg_rect = pygame.Rect((self.bg_rect.topleft), (self.bg_rect.size))

        self.bg_color = pygame.Color(50, 50, 50)
        self.fg_color = pygame.Color(140, 36, 36)

        self.value = value
        self.max = max

        self.calc()

    def calc(self) -> None:
        tick_size = self.bg_rect.width / self.max
        self.fg_rect.width = tick_size * self.value

    def draw(self) -> None:
        pygame.draw.rect(self.display, self.bg_color, self.bg_rect)
        pygame.draw.rect(self.display, self.fg_color, self.fg_rect)