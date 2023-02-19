import pygame
import random
import time


class SnakeGame:
    def __init__(self, display_cfg, game_cfg):
        pygame.init()
        self.display = pygame.display.set_mode((display_cfg.width, display_cfg.height))
        self.display.fill(display_cfg.black)
        pygame.display.set_caption(display_cfg.caption)
        pygame.draw.rect(
            self.display,
            display_cfg.green,
            pygame.Rect(
                random.randint(0, display_cfg.width),
                random.randint(0, display_cfg.height),
                display_cfg.block_size,
                display_cfg.block_size,
            ),
        )
        pygame.display.flip()
        time.sleep(2)
