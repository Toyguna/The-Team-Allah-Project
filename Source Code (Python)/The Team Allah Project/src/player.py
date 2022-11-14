import pygame
import numpy as np

from src.projectile import *
from util.entity_handler import EntityHandler
import util.settings as SETTINGS

class Player:
    def __init__(self, display: pygame.Surface, type: int = 0) -> None:
        """ ``type``: 1 -> ALP, 2 -> TOYGUN """

        self.display = display
        
        # Starts out of bounds
        self.rect = pygame.Rect(-1000, -1000, SETTINGS.PLAYER_WIDTH, SETTINGS.PLAYER_HEIGHT)
        self.hitbox = pygame.Rect(-1000, -1000, self.rect.width/3, self.rect.width/3)

        self.health = 5
        self.spell_cards = 5

        self.type = type
        self.focusing = False
        self.speed = SETTINGS.PLAYER_SPEED

        self.iframe = 0

        self.shoot_cd = 0

    def movement(self, keys_pressed: list[int]):
        self.focusing = keys_pressed[pygame.K_LSHIFT]
        self.speed = SETTINGS.PLAYER_FOCUS_SPEED if self.focusing else SETTINGS.PLAYER_SPEED

        if keys_pressed[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys_pressed[pygame.K_DOWN]:
            self.rect.y += np.ceil(self.speed)
        if keys_pressed[pygame.K_RIGHT]:
            self.rect.x += np.ceil(self.speed)
        if keys_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed

        self.collision()
        self.update_hitbox()

        if self.shoot_cd > 1:
            self.shoot_cd -= 0.1
        elif self.shoot_cd != 0:
            self.shoot_cd = 0

    def collision(self):
        hb_rect_diff = abs(self.hitbox.bottom - self.rect.bottom )

        if self.rect.right > SETTINGS.PA_WIDTH + self.hitbox.width:
            self.rect.right = SETTINGS.PA_WIDTH + self.hitbox.width
        if self.rect.left < -self.hitbox.width:
            self.rect.left = -self.hitbox.width
        if self.rect.top < -hb_rect_diff:
            self.rect.top = -hb_rect_diff
        if self.rect.bottom > SETTINGS.PA_HEIGHT + hb_rect_diff:
            self.rect.bottom = SETTINGS.PA_HEIGHT + hb_rect_diff

    def update_hitbox(self):
        self.hitbox.topleft = (self.rect.centerx - self.hitbox.width / 2), (self.rect.centery - self.hitbox.height / 2)

    def shoot(self, keys_pressed: list[int], entity_handler: EntityHandler):
        if keys_pressed[pygame.K_z] and self.shoot_cd == 0:
            self.shoot_cd = 1.5

            find_type = self.type
            find_type *= 1 if self.focusing else -1

            if self.type == 1:
                entity_handler.create_projectile(
                    AllyProjectile(
                    self.display, (self.rect.left, self.rect.top - 10), find_type)) 
                entity_handler.create_projectile(
                    AllyProjectile(
                    self.display, (self.rect.right - SETTINGS.NALPROJ_WIDTH, self.rect.top - 10), find_type))
            
    def draw(self):
        pygame.draw.rect(self.display, "yellow", self.rect)

        if self.focusing:
            pygame.draw.rect(self.display, "red", self.hitbox)

        if self.type == 1: # ALP
            pass
        elif self.type == 2: # TOYGUN
            pass

    def take_damage(self):
        #print(self.health)

        if self.iframe <= 0:
            self.iframe = 60
            self.health -= 1

            if self.health < 1:
                self.death()
            else:
                self.rect.topleft = (320 * SETTINGS.normalize_w, 800 * SETTINGS.normalize_h)

    def spell_card(self, boss, entity_handler):
        if self.spell_cards > 0:
            self.spell_cards -= 1

            entity_handler.clear_projectiles()

            harm_amt = boss.ai.max_hp / 5

            boss.ai.take_damage(harm_amt)

    def death(self):
        pass

    def handle_iframe(self):
        if self.iframe > 0:
            self.iframe -= 1
        elif self.iframe < 0:
            self.iframe = 0