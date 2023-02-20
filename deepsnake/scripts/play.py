from deepsnake.lib.games import SnakeGame
import pygame, sys


def main():
    snake_game = SnakeGame()
    # Game Loop
    while True:
        keys = pygame.key.get_pressed()
        snake_game.exec_key(keys)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        snake_game.draw_snake()


if __name__ == "__main__":
    main()
