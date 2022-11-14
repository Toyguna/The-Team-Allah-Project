import pygame
import random

import src.attacks as attacks

class BossAI:
    def __init__(self, hp: int, attack_delay: int, phase_amount: int, attack_patterns: dict) -> None:
        """
            ``phrases`` must be more than 0. \n
            ``attack_patters`` appicable format:
                attack_patterns = {
                    1: {    // phase indicator //
                        20: ... ,   // key value -> attack weight in rng //  \n
                        5: ... ,    // attack weight : attack object // \n
                        35: ... , \n
                        . . .
                    },

                    2: {...}
                }
        """
        
        self.max_hp = hp
        self.hp = hp
        self.phase_amount = phase_amount

        self.attack_delay = attack_delay
        self.delay_counter = 100

        self.current_phase = 1
        self.phase_spread =  self.hp / self.phase_amount

        self.attack_patterns = attack_patterns

        self.attack_chances = []

        self.locked = False

        for key in self.attack_patterns:
            atkc_arr = []
            for weight in self.attack_patterns[key]:
                atkc_arr.append(weight)

            self.attack_chances.append(atkc_arr) 

    def update(self):
        if self.delay_counter > 0:
            self.delay_counter -= 1
        else:
            self.delay_counter = self.attack_delay
            self.try_rng()

    def take_damage(self, amt: int):
        if not self.locked:
            self.hp -= amt

            if self.hp < 0:
                self.death()

    def death(self):
        self.locked = True

    def try_rng(self):
        attack = random.choices(self.attack_patterns[self.current_phase], self.attack_chances[self.current_phase-1])

        attack.commence()