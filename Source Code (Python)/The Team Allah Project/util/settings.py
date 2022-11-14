import pygame
pygame.font.init()

RESOLUTION = WIDTH, HEIGHT = 900, 900

normalize_w, normalize_h = 900 / WIDTH, 900 / HEIGHT

MAX_FPS = 144

PLAYABLE_AREA = PA_WIDTH, PA_HEIGHT = normalize_w * 600, normalize_h * 900
INFO_HUD_AREA = IHA_WIDTH, IHA_HEIGHT = normalize_w * 300, normalize_h * 900

# Player
PLAYER_WIDTH, PLAYER_HEIGHT = normalize_w * 40, normalize_h * 80

PLAYER_MAX_SPELLCARDS = 5
PLAYER_MAX_HEALTH = 5

PLAYER_SPEED = 2.5 * normalize_w
PLAYER_FOCUS_SPEED = PLAYER_SPEED / 2

PLAYER_SPELLCARD_DAMAGE = 50
PLAYER_BASE_DAMAGE_T1 = 5
PLAYER_BASE_DAMAGE_T2 = 3

# Boss
BOSS_WIDTH, BOSS_HEIGHT = normalize_w * 50, normalize_h * 100

# AllyProjectile
NALPROJ_WIDTH, NALPROJ_HEIGHT = normalize_w * 5, normalize_h * 20
FALPROJ_WIDTH, FALPROJ_HEIGHT = normalize_w * 15, normalize_h * 15

NALPROJ_SPEED = 5
FALPROJ_SPEED = 6

# UI
BUTTON_WIDTH, BUTTON_HEIGHT = normalize_w * 100, normalize_h * 40

BUTTON_FONT = pygame.font.SysFont("arial.ttf", int(24 * normalize_w), False, False)

# SOUND
VOLUME = 0.1

print(">> Settings loaded. \n")