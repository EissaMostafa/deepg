from deepsnake.lib.games import SnakeGame
import pygame, sys
from deepsnake.cfg.default import Direction


def main():
    snake_game = SnakeGame()
    # Game Loop
    direction = Direction.RIGHT
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                direction = snake_game.exec_key(event.key)
        run = snake_game.move(direction)
        pygame.time.wait(500)
    snake_game._game_over()
    pygame.time.wait(1000)


if __name__ == "__main__":
    main()
