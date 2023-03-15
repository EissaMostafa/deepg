import pygame
import random
import sys
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
        self.grid = set(
            [
                (row, col)
                for row in range(0, self.display_cfg.width, self.display_cfg.block_size)
                for col in range(
                    0, self.display_cfg.height, self.display_cfg.block_size
                )
            ]
        )
        self._set_initial_state()
        self.score = 0
        self.clock = pygame.time.Clock()
        self._draw_display()

    def _set_initial_state(self):
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
        self.key_pressed = []

    def _draw_food(self):
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

    def _draw_score(self):
        score = pygame.font.SysFont(None, 32).render(
            f"Score: {self.score}", True, self.display_cfg.red
        )
        self.display.blit(score, (20, 20))

    def _draw_display(self):
        self.display.fill(self.display_cfg.black)
        self._draw_score()
        self._draw_food()
        self._draw_snake()
        pygame.display.flip()

    def _get_next_location(self):
        h_x, h_y = self.snake[-1]
        if self.direction == Direction.UP:
            h_y -= self.display_cfg.block_size
        if self.direction == Direction.DOWN:
            h_y += self.display_cfg.block_size
        if self.direction == Direction.LEFT:
            h_x -= self.display_cfg.block_size
        if self.direction == Direction.RIGHT:
            h_x += self.display_cfg.block_size
        return h_x, h_y

    def _move_snake(self):
        h_x, h_y = self._get_next_location()
        if (h_x, h_y) == self.food:
            self.score += 50
        else:
            x_dist_new = abs(self.food.x - h_x)
            x_dist_old = abs(self.food.x - self.snake[-1][0])
            y_dist_new = abs(self.food.y - h_y)
            y_dist_old = abs(self.food.y - self.snake[-1][1])
            # if (x_dist_new > x_dist_new) or (y_dist_new > y_dist_old):
            #    self.score -= 1

            self.snake.pop(0)  # Remove the end of the snake tail
        self.snake.append((h_x, h_y))  # Append a new head

    def _check_game_over(self):
        h_x, h_y = self.snake[-1]
        width_cond = (h_x < 0) or (h_x >= self.display_cfg.width)
        height_cond = (h_y < 0) or (h_y >= self.display_cfg.height)
        self_hit_cond = (h_x, h_y) in self.snake[:-1]
        if width_cond or height_cond or self_hit_cond:
            self._game_over()
            self.score -= 100
            self._set_initial_state()
            # sys.exit()

    def _game_over(self):
        # If game over is true, draw game over
        text = pygame.font.SysFont("arial", 70).render(
            "Game Over", True, self.display_cfg.white, self.display_cfg.black
        )
        text_rect = text.get_rect()
        text_x = self.display.get_width() / 2 - text_rect.width / 2
        text_y = self.display.get_height() / 2 - text_rect.height / 2
        self.display.blit(text, [text_x, text_y])
        pygame.display.flip()
        pygame.time.wait(1000)

    def _exec_key(self):
        key = self.key_pressed.pop(0) if self.key_pressed else None
        if key == pygame.K_UP and self.direction is not Direction.DOWN:
            self.direction = Direction.UP
        if key == pygame.K_DOWN and self.direction is not Direction.UP:
            self.direction = Direction.DOWN
        if key == pygame.K_LEFT and self.direction is not Direction.RIGHT:
            self.direction = Direction.LEFT
        if key == pygame.K_RIGHT and self.direction is not Direction.LEFT:
            self.direction = Direction.RIGHT

    def _create_new_food(self):
        # Method 1
        if self.snake[-1] == self.food:
            r = random.choice(list(self.grid - set(self.snake)))
            self.food = Food(r[0], r[1])
        # Method 2
        # if self.snake[-1] == self.food:
        #     self.food = Food(
        #         random.choice(
        #             range(0, self.display_cfg.width, self.display_cfg.block_size)
        #         ),
        #         random.choice(
        #             range(0, self.display_cfg.height, self.display_cfg.block_size)
        #         ),
        #     )
        # if self.food in self.snake:
        #     self._create_new_food()

    def read_key(self, key_event):
        self.key_pressed.append(key_event)

    def play_step(self):
        self._exec_key()
        self._move_snake()
        self._create_new_food()
        self._check_game_over()
        self._draw_display()
        self.clock.tick(self.game_cfg.speed)

    def get_state(self):
        h_x, h_y = self.snake[-1]
        f_x, f_y = self.food.x, self.food.y

        obstacle_left_state = ((h_x - self.display_cfg.block_size) < 0) or (
            (h_x - self.display_cfg.block_size, h_y) in self.snake
        )
        obstacle_right_state = (
            (h_x + self.display_cfg.block_size) >= self.display_cfg.width
        ) or ((h_x + self.display_cfg.block_size, h_y) in self.snake)
        obstacle_up_state = ((h_y - self.display_cfg.block_size) < 0) or (
            (h_x, h_y - self.display_cfg.block_size) in self.snake
        )
        obstacle_down_state = (
            (h_y + self.display_cfg.block_size) >= self.display_cfg.height
        ) or ((h_x, h_y + self.display_cfg.block_size) in self.snake)
        # --> 4*4 = 16 states

        # 3*3 = 9 states

        moving_left_state = self.direction == Direction.LEFT
        moving_right_state = self.direction == Direction.RIGHT
        moving_up_state = self.direction == Direction.UP
        moving_down_state = self.direction == Direction.DOWN

        food_left_state = f_x < h_x
        food_right_state = f_x > h_x
        food_up_state = f_y < h_y
        food_down_state = f_y > h_y

        horizontal_binary = "".join(
            ["1" if x else "0" for x in [food_left_state, food_right_state]]
        )
        vertical_binary = "".join(
            ["1" if x else "0" for x in [food_up_state, food_down_state]]
        )
        horizontal_number = int(horizontal_binary, 2)
        vertical_number = int(vertical_binary, 2)
        # food_number = horizontal_number * 3 + vertical_number  # (= max 9)

        if moving_left_state:
            moving_number = 0
        elif moving_right_state:
            moving_number = 1
        elif moving_up_state:
            moving_number = 2
        else:
            moving_number = 3

        obstacle_binary = "".join(
            [
                "1" if x else "0"
                for x in [
                    obstacle_left_state,
                    obstacle_right_state,
                    obstacle_up_state,
                    obstacle_down_state,
                ]
            ]
        )
        obstacle_number = int(obstacle_binary, 2)

        state_number = obstacle_number * 36 + (
            moving_number * 9 + (horizontal_number * 3 + vertical_number)
        )

        return state_number
