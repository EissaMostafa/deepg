import pygame
import random
import time
from deepsnake.cfg.default import Direction, DisplayConfig, GameConfig


class SnakeGame:
    def __init__(self):
        pygame.init()
        self.display_cfg = DisplayConfig()
        self.game_cfg = GameConfig()
        self.display = pygame.display.set_mode(
            (self.display_cfg.width, self.display_cfg.height)
        )
        self.display.fill(self.display_cfg.black)
        pygame.display.set_caption(self.display_cfg.caption)
        self.snake = [(300, 300)]
        self._draw_food()
        self.draw_snake()

    def _draw_food(self):
        # TODO: make sure to generate the food outside the snake, and substract the block_size from the randint
        pygame.draw.rect(
            self.display,
            self.display_cfg.green,
            pygame.Rect(
                random.randint(0, self.display_cfg.width),
                random.randint(0, self.display_cfg.height),
                self.display_cfg.block_size,
                self.display_cfg.block_size,
            ),
        )
        pygame.display.flip()

    def draw_snake(self):
        for x, y in self.snake:
            pygame.draw.rect(
                self.display,
                self.display_cfg.blue,
                pygame.Rect(
                    x,
                    y,
                    self.display_cfg.block_size,
                    self.display_cfg.block_size,
                ),
            )
        pygame.display.flip()

    def move(self, direction: Direction):
        h_x, h_y = self.snake[-1]
        self.snake = self.snake[1:]  # Remove last block (end of the snake tail)
        if direction == Direction.UP:
            self.snake.append((h_x, h_y - self.display_cfg.block_size))
        if direction == Direction.DOWN:
            self.snake.append((h_x, h_y + self.display_cfg.block_size))
        if direction == Direction.LEFT:
            self.snake.append((h_x - self.display_cfg.block_size, h_y))
        if direction == Direction.RIGHT:
            self.snake.append((h_x + self.display_cfg.block_size, h_y))

    def exec_key(self, keys):
        if keys[pygame.K_UP]:
            self.move(Direction.UP)
        if keys[pygame.K_DOWN]:
            self.move(Direction.DOWN)
        if keys[pygame.K_LEFT]:
            self.move(Direction.LEFT)
        if keys[pygame.K_RIGHT]:
            self.move(Direction.RIGHT)
