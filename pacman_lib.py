from tkinter import *
from spritelib_v4 import *
from imagehelper import *
from nonblockingdelay import *
import random
import pygame.mixer as mixer

class Monster:

    def __init__(self, images: list, x: int = 0, y: int = 0,
                 border_color: str = 'black', border_width: int = 2,
                 fill_color: str = '',
                 direction: Direction = Direction.RIGHT,
                 delay_time: int = 25, speed: int = 3,
                 frame_delay: int = 100,
                 left_limit: int = 0, right_limit: int = 800,
                 top_limit: int = 0, bottom_limit: int = 600
                 ) -> None:
        super().__init__()
        self._sprite = Sprite(x, y, 32, 32, border_color, border_width,
                              fill_color, images[0])
        self._mover = Mover(self._sprite, direction, delay_time, speed)
        self._animation = Animation(self._sprite, images, frame_delay)
        self.clamp = Clamp(left_limit, right_limit, top_limit, bottom_limit)

    @property
    def sprite(self):
        return self._sprite

    @property
    def mover(self):
        return self._mover

    @property
    def animation(self):
        return self._animation

    def random_direction(self):
        random_num = random.randint(1, 4)
        if random_num == 1:
            if self._mover.direction is not Direction.RIGHT:
                self._mover.direction = Direction.LEFT
        elif random_num == 2:
            if self._mover.direction is not Direction.LEFT:
                self._mover.direction = Direction.RIGHT
        elif random_num == 3:
            if self._mover.direction is not Direction.DOWN:
                self._mover.direction = Direction.UP
        else:
            if self._mover.direction is not Direction.UP:
                self._mover.direction = Direction.DOWN

    def draw(self, canvas):
        self._sprite.draw(canvas)

    def update(self, delta_time):
        self._mover.update(delta_time)
        self._animation.update(delta_time)
        Clamp.clamp_all(self._sprite, self.clamp.left_limit, self.clamp.right_limit, self.clamp.top_limit,
                        self.clamp.bottom_limit)
