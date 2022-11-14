import pygame

import util.settings as SETTINGS
from src.boss_ai import BossAI
from src.attacks import Attack

ai_map = {
    0: BossAI( # Can
        9000, 600, 6,
        {
            1: {

            },

            2: {

            },

            3: {

            },

            4: {

            },

            5: {

            },

            6: {
                
            }
        }
    ),

    1: BossAI( # Mert
        1500, 500, 2, 
        {
            1: {
                20: Attack([])
            },

            2: {

            }
        }
    ),

    2: BossAI( # Çağan
        1500, 700, 2,
        {
            1: {

            },

            2: {

            }
        }
    ),

    3: BossAI( # Samet
        1500, 600, 3,
        {
            1: {

            },

            2: {

            },

            3: {

            }
        }
    ),

    4: BossAI( # Rüzgar
        1500, 600, 3,
        {
            1: {

            },

            2: {

            },

            3: {

            }
        }
    ),

    5: BossAI( # Ege
        1500, 600, 4,
        {
            1: {

            },

            2: {

            },

            3: {

            },

            4: {

            }
        }
    ),

    6: BossAI( # Efe
        1500, 600, 5,
        {
            1: {

            },

            2: {

            },

            3: {

            },

            4: {

            },

            5: {
                
            }
        }
    )
}

type_name_map = {
    0: "Can",
    1: "Mert",
    2: "Çağan",
    3: "Samet",
    4: "Rüzgar",
    5: "Ege",
    6: "Efe"
}

class Boss:
    def __init__(self, display: pygame.Surface, type: int) -> None:
        """
        ``type``: 
            0 -> can (special boss)
            1 -> mert
            2 -> çağan
            3 -> samet
            4 -> rüzgar
            5 -> ege
            6 -> efe
        """

        self.display = display

        self.rect: pygame.Rect = pygame.Rect(
            (SETTINGS.PLAYABLE_AREA[0] / 2, 40 * SETTINGS.normalize_h),
            (SETTINGS.BOSS_WIDTH, SETTINGS.BOSS_HEIGHT)
        )
        self.image: pygame.Surface = None

        self.type: int = type
        self.ai: BossAI = ai_map[self.type]

    def update(self):
        pass
        #self.ai.update()

    def draw(self):
        pygame.draw.rect(self.display, "orange", self.rect)