import pygame
import os

import util.gamestate as GAMESTATE
import util.settings as SETTINGS

class SoundHandler:
    def __init__(self) -> None:
        pygame.mixer.init()
        "  ∟ pygame.mixer √"

        self.music = {
            "bad_ending": os.path.join("assets/music", "bad_ending.ogg"),
            "dialogue_jolly": os.path.join("assets/music", "dialogue_jolly.ogg"),
            "dialogue_objection": os.path.join("assets/music", "dialogue_objection.ogg"),
            "main_menu": os.path.join("assets/music", "main_menu.ogg"),
            "1": os.path.join("assets/music", "stage1_mert.ogg"),
            "2": os.path.join("assets/music", "stage2_cagan.ogg"),
            "3": os.path.join("assets/music", "stage3_samet.ogg"),
            "4": os.path.join("assets/music", "stage4_ruzgar.ogg"),
            "5": os.path.join("assets/music", "stage5_ege.ogg"),
            "6": os.path.join("assets/music", "stage6_efe.ogg"),
            "0": os.path.join("assets/music", "stageExtra_can.ogg"),
        }

        self.loop = -1
        self.music_playing = None

        self.set_volume(SETTINGS.VOLUME)

    def play(self, key: str):
        self.stop()

        pygame.mixer.music.load(self.music[key])
        pygame.mixer.music.play(self.loop)

        self.music_playing = key

    def stop(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

        self.music_playing = None

    def set_volume(self, volume: float):
        pygame.mixer.music.set_volume(volume)