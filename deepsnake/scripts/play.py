from deepsnake.lib.games import SnakeGame
from deepsnake.cfg.default import DisplayConfig, GameConfig


def main():
    _ = SnakeGame(DisplayConfig(), GameConfig())


if __name__ == "__main__":
    main()
