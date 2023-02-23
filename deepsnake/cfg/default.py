from enum import Enum

conf_dict = {
    # GAME
    "caption": "Snake Game!",
    "speed": 12,
    "block_size": 25,
    # DISPLAY
    "height": 800,
    "width": 800,
    # COLORS
    "white": (255, 255, 255),
    "red": (200, 0, 0),
    "green": (0, 200, 0),
    "blue": (0, 0, 200),
    "black": (0, 0, 0),
}


class Direction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4


class GameStatus(Enum):
    RUNNING = 1
    GAME_OVER = 0


class Config(object):
    def __init__(self):
        self._config = conf_dict

    def get_property(self, property_name):
        if property_name not in self._config.keys():
            return None
        return self._config[property_name]


class DisplayConfig(Config):
    @property
    def caption(self):
        return self.get_property("caption")

    @property
    def height(self):
        return self.get_property("height")

    @property
    def width(self):
        return self.get_property("width")

    @property
    def block_size(self):
        return self.get_property("block_size")

    @property
    def white(self):
        return self.get_property("white")

    @property
    def red(self):
        return self.get_property("red")

    @property
    def green(self):
        return self.get_property("green")

    @property
    def blue(self):
        return self.get_property("blue")

    @property
    def black(self):
        return self.get_property("black")


class GameConfig(Config):
    @property
    def speed(self):
        return self.get_property("speed")
