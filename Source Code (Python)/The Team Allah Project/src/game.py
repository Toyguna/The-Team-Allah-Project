import pygame
import math
import sys
import os

import util.settings as SETTINGS
import util.gamestate as GAMESTATE
import src.renderer as renderer
import src.player as player 
import src.boss as boss 
import src.projectile as projectile

import util.projectile_type as PROJECTILE_T
import util.entity_handler as entity_handler
import util.sound_handler as sound_handler

class Game:
    def __init__(self) -> None:
        print(">> Starting initialization...")

        self.display = pygame.display.set_mode((SETTINGS.RESOLUTION))
        pygame.display.set_caption("The Team Allah Project")

        self.game_state = GAMESTATE.MAIN_MENU

        self.renderer = renderer.MainRenderer(self.display)
        print(" ∟ MainRenderer √")

        self.entity_handler = entity_handler.EntityHandler()
        print(" ∟ EntityHandler √")

        self.sound_handler = sound_handler.SoundHandler()
        print(" ∟ SoundHandler √")

        self.button_arr = self.renderer.get_buttons()
        self.proj_arr = self.entity_handler.get_projectiles()

        self.bosses_defeated = 0

        self.player: player.Player = None
        self.boss: boss.Boss = None

        self.clock = pygame.time.Clock()

        print(">> Initialization successful.")
        
    def game_loop(self) -> None:
        keys_pressed = []
        mouse_pressed = []
        mouse_pos = []

        self.sound_handler.play("main_menu")

        while True:
            keys_pressed = pygame.key.get_pressed()
            mouse_pressed = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()

            # Debug logging
            #print(len(self.proj_arr))

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_app()

                if event.type == pygame.MOUSEBUTTONUP:
                    self.handle_buttons(mouse_pos)

                if event.type == pygame.KEYUP: 
                    if event.key == pygame.K_x:
                        self.player.spell_card(self.boss, self.entity_handler)

                    if event.key == pygame.K_k: # DEBUG
                        self.entity_handler.create_projectile(
                            projectile.AlertProjectile(
                                self.display, 
                                pygame.Rect(self.player.rect.topleft, PROJECTILE_T.ALERT_PROJ_SIZE)
                            )
                        )

            # Player
            if self.game_state == GAMESTATE.IN_GAME and self.player is not None:
                self.player.movement(keys_pressed)
                self.player.shoot(keys_pressed, self.entity_handler)

                self.player_damage()

            # Boss
            if self.game_state == GAMESTATE.IN_GAME and self.boss is not None:
                self.boss.update()

                self.boss_damage()
                self.boss_death()

                self.renderer.value_bossbar(self.boss.ai.hp)

            # Projectiles
            if self.game_state == GAMESTATE.IN_GAME and self.proj_arr is not None:
                self.entity_handler.update()
                self.entity_handler.out_of_bounds_check()

            # Other rendering in between
            self.renderer.repaint(self.game_state)

            #   Player /  Boss / Projectiles
            if self.game_state > GAMESTATE.START_GAME:
                if self.proj_arr is not None:
                    self.entity_handler.draw()
                if self.boss is not None:
                    self.boss.draw()
                if self.player is not None:
                    self.player.draw()

            try:
                self.renderer.handleUI(self.game_state, self.boss.type)
            except:
                self.renderer.handleUI(self.game_state)

            self.renderer.update(self.game_state)

            # Finalize
            self.clock.tick(SETTINGS.MAX_FPS)


    def handle_buttons(self, mouse_pos: list[int, int]):
        for button in self.button_arr:
            if button.rect.collidepoint(mouse_pos) and self.game_state == button.activation:
                self.game_state = button.destination

                if button.special_id is not None:
                    if button.special_id == 0:
                        self.player = player.Player(self.display, 1)
                        self.start_game()
                    elif button.special_id == 1:
                        self.player = player.Player(self.display, 2)
                        self.start_game()

    def start_game(self):
        if self.bosses_defeated >= 6:
            self.bosses_defeated = -1

        self.game_state = GAMESTATE.IN_GAME

        self.player.rect.topleft = (320 * SETTINGS.normalize_w, 800 * SETTINGS.normalize_h)
        self.boss = boss.Boss(self.display, self.bosses_defeated + 1)

        self.renderer.set_bossbar(self.boss.ai.hp, 0)

        self.sound_handler.play(f"{self.boss.type}")

    def quit_app(self):
        pygame.quit()
        sys.exit()

    def player_damage(self):
        for proj in self.proj_arr:
            if proj.rect.colliderect(self.player.rect) and not isinstance(proj, projectile.AllyProjectile):
                if hasattr(proj, "activated"):
                    if proj.activated:
                        self.entity_handler.clear_projectiles()
                        self.player.take_damage()

                        self.renderer.player_hp.value = self.player.health
                else:
                    self.entity_handler.clear_projectiles()
                    self.player.take_damage()

                    self.renderer.player_hp.value = self.player.health

    def boss_damage(self):
        for proj in self.proj_arr:
            if proj.rect.colliderect(self.boss.rect) and isinstance(proj, projectile.AllyProjectile):
                damage = SETTINGS.PLAYER_BASE_DAMAGE_T1 if self.player.type == 1 else SETTINGS.PLAYER_BASE_DAMAGE_T2
                damage /= 2 if proj.type < 0 else 1

                self.boss.ai.take_damage(damage)

                self.entity_handler.kill_projectile(proj)

    def boss_death(self):
        if self.boss.ai.hp <= 0:
            self.bosses_defeated += 1

            self.start_game()