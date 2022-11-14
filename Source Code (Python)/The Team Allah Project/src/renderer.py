import pygame
import os

from src.boss import type_name_map

import ui.button as button
from ui.health_bar import HealthBar

from util.settings import HEIGHT, PLAYABLE_AREA, INFO_HUD_AREA, normalize_w, normalize_h, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_FONT, PLAYER_MAX_HEALTH, PLAYER_MAX_SPELLCARDS
import util.gamestate as GAMESTATE
import util.image as IMAGE

class MainRenderer:
    def __init__(self, display: pygame.Surface) -> None:
        self.display = display

        self.background_color = "black"

        # UI {
        self.hud_area = pygame.Rect(
            (PLAYABLE_AREA[0] + 5 * normalize_w, 0),
            INFO_HUD_AREA
        )

        self.area_border = pygame.Rect(
            (PLAYABLE_AREA[0], 0),
            (5 * normalize_w, HEIGHT)
        )

        self.boss_bar = HealthBar(self.display, pygame.Rect(
            (self.area_border.right + 10 * normalize_w, 10 * normalize_h),
            (self.hud_area.width - 25 * normalize_w, 40 * normalize_h)
        ), 100, 0)

        self.player_hp = HealthBar(self.display, 
            pygame.Rect(
                (self.area_border.right + 10 * normalize_w, HEIGHT - 50 * normalize_h),
                (self.hud_area.width - 25 * normalize_w, 40 * normalize_h)
            ), 5, 5)
        
        self.player_hp.fg_color = pygame.Color(0, 140, 40)

        self.buttons = self.create_buttons()
        # }

    def clear(self):
        self.display.fill(self.background_color)

    def repaint(self, game_state: int) -> None:
        self.clear()

        self.handleAreas(game_state)
        self.handleObjects(game_state)

    def handleAreas(self, game_state: int) -> None:
        pass

    def handleUI(self, game_state: int, boss_type: int = None) -> None:
        if game_state == GAMESTATE.IN_GAME:
            pygame.draw.rect(self.display, "black", self.hud_area)
            pygame.draw.rect(self.display, "gray", self.area_border)

            self.boss_bar.calc()
            self.boss_bar.draw()

            self.player_hp.calc()
            self.player_hp.draw()

            if boss_type is not None:
                boss_text = BUTTON_FONT.render(type_name_map[boss_type], False, "white")
                self.display.blit(
                    boss_text, 
                    (self.boss_bar.bg_rect.centerx - boss_text.get_width() / 2,
                    self.boss_bar.bg_rect.centery - boss_text.get_height() / 2)
                )

            self.player_hp.draw()

        for button in self.buttons:
            if (game_state == button.activation):
                button.draw()

    def handleImportant(self, game_state: int) -> None:
        pass

    def handleObjects(self, game_state: int) -> None:
        pass

    def update(self, game_state: int) -> None:
        pygame.display.update()
    
    def value_bossbar(self, value: int) -> None:
        self.boss_bar.value = value

    def set_bossbar(self, max: int, starter: int) -> None:
        self.boss_bar.max = max
        self.boss_bar.value = starter

    def get_buttons(self) -> list:
        return self.buttons

    def create_buttons(self) -> list[button.Button]:
        button_arr = [
            button.Button(self.display, pygame.Rect(
                100 * normalize_w, 100 * normalize_h,
                BUTTON_WIDTH, BUTTON_HEIGHT
                ), {
                "text": "START",
                "activation": GAMESTATE.MAIN_MENU,
                "destination": GAMESTATE.CHAR_SELECTION
            }),

            button.ImageButton(self.display, pygame.Rect(
                100 * normalize_w, 300 * normalize_h,
                100 * normalize_w, 300 * normalize_h
                ), {
                "image": pygame.image.load(
                    os.path.join("assets/textures", "alp.png")
                ).convert_alpha(),
                "image_conversion": (int(150 * normalize_w), int(300 * normalize_h)),
                "activation": GAMESTATE.CHAR_SELECTION,
                "destination": GAMESTATE.IN_GAME,
                "special_id": 0
            })
            
        ]

        return button_arr