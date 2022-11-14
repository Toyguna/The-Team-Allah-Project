import pygame

import util.settings as SETTINGS
import src.projectile as projectile

class EntityHandler:
    def __init__(self):
        self.proj_arr = []

    def create_projectile(self, proj):
        self.proj_arr.append(proj)

    def kill_projectile(self, proj):
        self.proj_arr.remove(proj)

    def clear_projectiles(self):
        self.proj_arr.clear()

    def get_projectiles(self):
        return self.proj_arr

    def update(self):
        for proj in self.proj_arr:
            proj.update()

            if isinstance(proj, projectile.AlertProjectile):
                if proj.counter >= proj.total_duration:
                    self.kill_projectile(proj)

    def draw(self):
        for proj in self.proj_arr:
            proj.draw()

    def out_of_bounds_check(self):
        for proj in self.proj_arr:
            if proj.rect.top <= -5 or proj.rect.top >= SETTINGS.PA_HEIGHT:
                self.kill_projectile(proj)

            if proj.rect.left <= -5 or proj.rect.left >= SETTINGS.PA_WIDTH + 5:
                self.kill_projectile(proj)