import pygame

from util.entity_handler import EntityHandler

class Attack:
    def __init__(self, projectiles: list, instructions: dict = None) -> None:
        """
            ``insturctions`` appicable format:
                {
                    "goto": (x, y),
                }
        """

        self.projs = projectiles
        self.instructions = instructions

    def commence(self, entity_handler: EntityHandler, parent) -> None:
        [entity_handler.create_projectile(proj) for proj in self.projs]

        if self.instruction is not None:
            if "goto" in self.instructions:
                parent.rect.topleft = self.instructions["goto"]
