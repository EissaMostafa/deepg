import pygame
import random
from deepsnake.cfg.default import Direction, DisplayConfig, GameConfig, GameStatus
from collections import namedtuple

Food = namedtuple("Food", "x y")


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
        snake_head_init = (
            self.display_cfg.block_size
            * int(self.display_cfg.width / (2 * self.display_cfg.block_size)),
            self.display_cfg.block_size
            * int(self.display_cfg.height / (2 * self.display_cfg.block_size)),
        )
        self.snake = [
            (
                snake_head_init[0] - 2 * self.display_cfg.block_size,
                snake_head_init[1],
            ),
            (
                snake_head_init[0] - self.display_cfg.block_size,
                snake_head_init[1],
            ),
            snake_head_init,
        ]
        self.food = Food(
            random.choice(
                range(0, self.display_cfg.width, self.display_cfg.block_size)
            ),
            random.choice(
                range(0, self.display_cfg.height, self.display_cfg.block_size)
            ),
        )
        self.direction = Direction.RIGHT
        self.status = GameStatus.RUNNING
        self.clock = pygame.time.Clock()
        self._draw_display()

    def _draw_food(self):
        # TODO: make sure to generate the food outside the snake, and substract the block_size from the randint
        pygame.draw.rect(
            self.display,
            self.display_cfg.green,
            pygame.Rect(
                self.food.x,
                self.food.y,
                self.display_cfg.block_size,
                self.display_cfg.block_size,
            ),
        )

    def _draw_snake(self):
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

    def _draw_display(self):
        self.display.fill(self.display_cfg.black)
        self._draw_food()
        self._draw_snake()
        pygame.display.flip()

    def _move_snake(self):
        h_x, h_y = self.snake[-1]
        self.snake.pop(0)  # Remove last block (end of the snake tail)
        if self.direction == Direction.UP:
            h_y -= self.display_cfg.block_size
        if self.direction == Direction.DOWN:
            h_y += self.display_cfg.block_size
        if self.direction == Direction.LEFT:
            h_x -= self.display_cfg.block_size
        if self.direction == Direction.RIGHT:
            h_x += self.display_cfg.block_size

        self.snake.append((h_x, h_y))

    def _check_game_over(self):
        h_x, h_y = self.snake[-1]
        width_cond = (h_x < 0) or (h_x >= self.display_cfg.width)
        height_cond = (h_y < 0) or (h_y >= self.display_cfg.height)
        self_hit_cond = (h_x, h_y) in self.snake[:-1]
        if width_cond or height_cond or self_hit_cond:
            self.status = GameStatus.GAME_OVER

    def _game_over(self):
        # If game over is true, draw game over
        text = pygame.font.SysFont("arial", 70).render(
            "Game Over", True, (255, 255, 255), (0, 0, 0)
        )
        text_rect = text.get_rect()
        text_x = self.display.get_width() / 2 - text_rect.width / 2
        text_y = self.display.get_height() / 2 - text_rect.height / 2
        self.display.blit(text, [text_x, text_y])
        pygame.display.flip()
        pygame.time.wait(1000)

    def handle_key(self, key):
        if key == pygame.K_UP and self.direction is not Direction.DOWN:
            self.direction = Direction.UP
        if key == pygame.K_DOWN and self.direction is not Direction.UP:
            self.direction = Direction.DOWN
        if key == pygame.K_LEFT and self.direction is not Direction.RIGHT:
            self.direction = Direction.LEFT
        if key == pygame.K_RIGHT and self.direction is not Direction.LEFT:
            self.direction = Direction.RIGHT

    def play_step(self):
        self._move_snake()
        self._check_game_over()
        self._draw_display()
        self.clock.tick(self.game_cfg.speed)
