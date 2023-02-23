from deepsnake.lib.games import SnakeGame
import pygame, sys
from deepsnake.cfg.default import GameStatus


def main():
    snake_game = SnakeGame()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                snake_game.read_key(event.key)
        snake_game.play_step()


if __name__ == "__main__":
    main()
