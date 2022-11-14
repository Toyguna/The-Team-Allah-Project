import pygame

import util.settings as SETTINGS
import util.image as IMAGE

class Button:
    def  __init__(self, display: pygame.Surface, rect: pygame.Rect,
            attr: dict) -> None:
        self.display = display
        self.rect = rect

        self.text = attr["text"] if "text" in attr else None
        self.activation = attr["activation"] if "activation" in attr else None 
        self.destination = attr["destination"] if "destination" in attr else None
        self.special_id = attr["special_id"] if "special_id" in attr else None

        if self.text is not None:
            self.font_text = SETTINGS.BUTTON_FONT.render(self.text, True, "black")

    def draw(self):
        pygame.draw.rect(self.display, "orange", self.rect)

        if self.text is not None:
            text_rect = self.font_text.get_rect()

            self.display.blit(self.font_text, (
                self.rect.left + text_rect.width / 2,
                self.rect.top + text_rect.height / 2
            ))

class ImageButton:
    def  __init__(self, display: pygame.Surface, rect: pygame.Rect,
            attr: dict) -> None:
        self.display = display
        self.rect = rect

        self.image = attr["image"] if "image" in attr else None
        self.image_conversion = attr["image_conversion"] if "image_conversion" in attr else None
        self.activation = attr["activation"] if "activation" in attr else None 
        self.destination = attr["destination"] if "destination" in attr else None
        self.special_id = attr["special_id"] if "special_id" in attr else None

        if self.image is not None and self.image_conversion is not None:
            if self.image_conversion == IMAGE.FIT:
                self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
            elif isinstance(self.image_conversion, tuple):
                self.image = pygame.transform.scale(self.image, self.image_conversion)

    def draw(self):
        self.display.blit(self.image, self.rect.topleft)
        #pygame.draw.rect(self.display, "green", self.rect)

CHAR_ALP = 0
CHAR_TOYGUN = 1