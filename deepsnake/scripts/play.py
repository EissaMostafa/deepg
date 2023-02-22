from deepsnake.lib.games import SnakeGame
import pygame, sys
from deepsnake.cfg.default import Direction


def main():
    snake_game = SnakeGame()
    # Game Loop
    direction = Direction.RIGHT
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                snake_game.handle_key(event.key)
        snake_game.play_step()
        pygame.time.wait(500)


if __name__ == "__main__":
    main()
