from __future__ import annotations

import random
from tkinter import *
from enum import Enum


class Point:
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.x = x
        self.y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    def __str__(self) -> str:
        return f'Point({self._x},{self._y})'

    def __repr__(self) -> str:
        return self.__str__()


class Clamp:
    def __init__(self, left_limit: int = 0, right_limit: int = 800, top_limit: int = 0,
                 bottom_limit: int = 600) -> None:
        super().__init__()
        self.left_limit = left_limit
        self.right_limit = right_limit
        self.top_limit = top_limit
        self.bottom_limit = bottom_limit

    def clampall(self, sprite: Sprite):
        Clamp.clamp_all(sprite, self.left_limit, self.right_limit, self.top_limit, self.bottom_limit)

    @classmethod
    def clamp_x(cls, sprite: Sprite, left_limit: int = 0, right_limit: int = 800):
        if sprite.x < left_limit:
            sprite.x = left_limit
        elif sprite.right > right_limit:
            sprite.right = right_limit

    @classmethod
    def clamp_y(cls, sprite: Sprite, top_limit: int = 0,
                bottom_limit: int = 600):
        if sprite.y < top_limit:
            sprite.y = top_limit
        elif sprite.bottom > bottom_limit:
            sprite.bottom = bottom_limit

    @classmethod
    def clamp_all(cls, sprite: Sprite, left_limit: int = 0, right_limit: int = 800,
                  top_limit: int = 0, bottom_limit: int = 600):
        cls.clamp_x(sprite, left_limit, right_limit)
        cls.clamp_y(sprite, top_limit, bottom_limit)


class Direction(Enum):
    LEFT = "Left"
    UP = "Up"
    RIGHT = "Right"
    DOWN = "Down"
    STOPPED = "Stopped"


class Sprite:
    def __init__(self, x: int = 0, y: int = 0, width: int = 25,
                 height: int = 25,
                 border_color: str = 'black', border_width: int = 2,
                 fill_color: str = '', image: PhotoImage = None) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self._width = width
        self._height = height
        self.border_color = border_color
        self.border_width = border_width
        self.fill_color = fill_color
        self._image = image
        if self._image is not None:
            self._width = self._image.width()
            self._height = self._image.height()

    @property
    def center_x(self):
        return self.x + self._width // 2

    @center_x.setter
    def center_x(self, value: int):
        self.x = value - self._width // 2

    @property
    def center_y(self):
        return self.y + self._height // 2

    @center_y.setter
    def center_y(self, value):
        self.y = value - self._height // 2

    @property
    def center(self):
        return Point(self.x + self._width // 2, self.y + self._height // 2)

    @center.setter
    def center(self, value: Point):
        self.x = value.x - self._width // 2
        self.y = value.y - self._height // 2

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if self._image is not None:
            raise Exception('cannot set width if sprite has image')
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if self._image is not None:
            raise Exception('cannot set height if sprite has image')
        self._height = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value
        self._width = self._image.width()
        self._height = self._image.height()

    @property
    def left(self):
        return self.x

    @left.setter
    def left(self, value):
        self.x = value

    @property
    def right(self):
        return self.x + self._width

    @right.setter
    def right(self, value):
        self.x = value - self._width

    @property
    def top(self):
        return self.y

    @top.setter
    def top(self, value):
        self.y = value

    @property
    def bottom(self):
        return self.y + self._height

    @bottom.setter
    def bottom(self, value):
        self.y = value - self._height

    def draw(self, canvas: Canvas):
        canvas.create_rectangle(self.left, self.top,
                                self.right, self.bottom,
                                outline=self.border_color,
                                fill=self.fill_color,
                                width=self.border_width)
        canvas.create_image(self.x, self.y, anchor=NW,
                            image=self._image)

    def increment_x(self, distance: int):
        self.x += distance

    def increment_y(self, distance: int):
        self.y += distance

    def bbox(self):
        t = (self.left, self.top, self.right, self.bottom)
        return t

    def intersects(self, box):
        a = self
        b = Sprite(box[0], box[1], box[2] - box[0], box[3] - box[1])
        return not (a.right < b.left or a.left > b.right
                    or a.bottom < b.top or a.top > b.bottom)

    def contains(self, x: int, y: int):
        return (x in range(self.left, self.right)) \
               and (y in range(self.top, self.bottom))

    def __str__(self) -> str:
        return str(self.__dict__).replace('_', '')


class Mover:
    def __init__(self, sprite: Sprite,
                 direction: Direction = Direction.RIGHT,
                 delay_time: int = 100, speed: int = 1):
        self._sprite = sprite
        self._direction = direction
        self._delay_time = delay_time
        self._speed = abs(speed)
        self._elapsed_time = 0

    def update(self, delta_time: int):
        self._elapsed_time += delta_time
        if self._elapsed_time >= self._delay_time:
            self._elapsed_time = 0
            if self._direction == Direction.LEFT:
                self._sprite.increment_x(-self._speed)
            elif self._direction == Direction.RIGHT:
                self._sprite.increment_x(self._speed)
            elif self._direction == Direction.UP:
                self._sprite.increment_y(-self._speed)
            elif self._direction == Direction.DOWN:
                self._sprite.increment_y(self._speed)

    @property
    def sprite(self):
        return self._sprite

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value: Direction):
        self._direction = value

    @property
    def delay_time(self):
        return self._delay_time

    @delay_time.setter
    def delay_time(self, value: int):
        self._delay_time = value

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value: int):
        self._speed = abs(value)

    def backup(self):
        if self._direction == Direction.LEFT:
            self._sprite.increment_x(self._speed)
        elif self._direction == Direction.RIGHT:
            self._sprite.increment_x(-self._speed)
        elif self._direction == Direction.UP:
            self._sprite.increment_y(self._speed)
        elif self._direction == Direction.DOWN:
            self._sprite.increment_y(-self._speed)


class Animation:
    def __init__(self, sprite: Sprite, images: list,
                 frame_delay: int = 100, loop: bool = True) -> None:
        self._images = images
        self._frame_delay = frame_delay
        self._current_frame = 0
        self._elapsed_time = 0
        self._paused = False
        self._sprite = sprite
        self._loop = loop

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    def update(self, deltaTime: int):
        if self._paused:
            self._elapsed_time = 0
        else:
            self._elapsed_time += deltaTime
            if self._elapsed_time > self._frame_delay:
                self._elapsed_time = 0
                self._current_frame += 1
                if self._current_frame >= len(self._images):
                    if not self._loop:
                        self._paused = True
                        self.current_frame = len(self._images) - 1
                    else:
                        self._current_frame = 0

            self._sprite.image = self._images[self._current_frame]

    @property
    def paused(self):
        return self._paused

    @paused.setter
    def paused(self, value: bool):
        self._paused = value

    @property
    def frame_delay(self):
        return self._frame_delay

    @frame_delay.setter
    def frame_delay(self, value: int):
        self._frame_delay = value

    @property
    def current_frame(self):
        return self._current_frame

    @current_frame.setter
    def current_frame(self, value):
        self._current_frame = value

    @property
    def images(self):
        return self._images

    @property
    def current_image(self):
        return self._images[self._current_frame]

    @images.setter
    def images(self, image_list: list):
        self._images = image_list

    def __str__(self) -> str:
        return "frame delay: {}, current frame: {}, elapsed time: {}".format(self._frame_delay, self._current_frame,
                                                                             self._elapsed_time)


class AnimatedSprite:
    def __init__(self, images: list, x: int = 0, y: int = 0,
                 border_color: str = 'black', border_width: int = 0,
                 fill_color: str = '', frame_delay: int = 100, loop=True) -> None:
        self._sprite = Sprite(x, y, 32, 32, border_color, border_width, fill_color, images[0])
        self._animation = Animation(self._sprite, images, frame_delay, loop)

    @property
    def sprite(self):
        return self._sprite

    @property
    def animation(self):
        return self._animation

    def draw(self, canvas: Canvas):
        self._sprite.draw(canvas)

    def update(self, delta_time):
        self._animation.update(delta_time)


class MovingSprite:
    def __init__(self, x: int = 0, y: int = 0, width: int = 32, height: int = 32,
                 border_color: str = 'black', border_width: int = 2,
                 fill_color: str = '', image=None,
                 direction: Direction = Direction.RIGHT,
                 delay_time: int = 15, speed: int = 1,
                 left_limit: int = 0, right_limit: int = 452,
                 top_limit: int = 0, bottom_limit: int = 500
                 ) -> None:
        super().__init__()
        self._sprite = Sprite(x, y, width, height, border_color, border_width,
                              fill_color, image)
        self._mover = Mover(self._sprite, direction, delay_time, speed)
        self.clamp = Clamp(left_limit, right_limit, top_limit, bottom_limit)

    @property
    def sprite(self):
        return self._sprite

    @property
    def mover(self):
        return self._mover

    def draw(self, canvas):
        self._sprite.draw(canvas)

    def update(self, delta_time):
        self._mover.update(delta_time)
        Clamp.clamp_all(self._sprite, self.clamp.left_limit, self.clamp.right_limit, self.clamp.top_limit,
                        self.clamp.bottom_limit)


class AnimatedMovingSprite:

    def __init__(self, images: list, x: int = 0, y: int = 0,
                 border_color: str = 'black', border_width: int = 2,
                 fill_color: str = '',
                 direction: Direction = Direction.RIGHT,
                 delay_time: int = 25, speed: int = 3,
                 frame_delay: int = 100,
                 left_limit: int = 0, right_limit: int = 452,
                 top_limit: int = 0, bottom_limit: int = 500
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

    def draw(self, canvas):
        self._sprite.draw(canvas)

    def update(self, delta_time):
        self._mover.update(delta_time)
        self._animation.update(delta_time)
        Clamp.clamp_all(self._sprite, self.clamp.left_limit, self.clamp.right_limit, self.clamp.top_limit,
                        self.clamp.bottom_limit)


class AnimatedHorizontalMovingSprite:

    def __init__(self, left_images: list, right_images: list, x: int = 0, y: int = 0,
                 border_color: str = 'black', border_width: int = 2,
                 fill_color: str = '',
                 direction: Direction = Direction.RIGHT,
                 delay_time: int = 15, speed: int = 3,
                 frame_delay: int = 100,
                 left_limit: int = 0, right_limit: int = 800
                 ) -> None:
        super().__init__()
        self.left_images = left_images
        self.right_images = right_images
        self.left_limit = left_limit
        self.right_limit = right_limit
        self._sprite = Sprite(x, y, 32, 32, border_color, border_width,
                              fill_color, right_images[0])
        self._mover = Mover(self._sprite, direction, delay_time, speed)
        self._animation = Animation(self._sprite, right_images, frame_delay)

    @property
    def left_images(self):
        return self._left_images

    @left_images.setter
    def left_images(self, value):
        self._left_images = value

    @property
    def right_images(self):
        return self._right_images

    @right_images.setter
    def right_images(self, value):
        self._right_images = value

    @property
    def left_limit(self):
        return self._left_limit

    @left_limit.setter
    def left_limit(self, value):
        self._left_limit = value

    @property
    def right_limit(self):
        return self._right_limit

    @right_limit.setter
    def right_limit(self, value):
        self._right_limit = value

    @property
    def sprite(self):
        return self._sprite

    @property
    def mover(self):
        return self._mover

    @property
    def animation(self):
        return self._animation

    def draw(self, canvas):
        self._sprite.draw(canvas)

    def update(self, delta_time):
        self._mover.update(delta_time)

        if self._sprite.left < self._left_limit:
            self._sprite.left = self._left_limit
        elif self._sprite.right > self._right_limit:
            self._sprite.right = self._right_limit

        if self._mover.direction == Direction.LEFT:
            self._animation.images = self._left_images
        elif self._mover.direction == Direction.RIGHT:
            self._animation.images = self._right_images
        self._animation.update(delta_time)


class Animated4WayMovingSprite:

    def __init__(self, left_images: list, right_images: list,
                 up_images: list, down_images: list,
                 x: int = 0, y: int = 0,
                 border_color: str = 'black', border_width: int = 2,
                 fill_color: str = '',
                 direction: Direction = Direction.RIGHT,
                 delay_time: int = 100, speed: int = 1,
                 frame_delay: int = 100,
                 left_limit: int = 0, right_limit: int = 800,
                 top_limit: int = 0, bottom_limit: int = 600) -> None:
        super().__init__()
        self._animated_moving_sprite = AnimatedMovingSprite(right_images, x, y, border_color,
                                                            border_width, fill_color, direction, delay_time,
                                                            speed, frame_delay, left_limit, right_limit,
                                                            top_limit, bottom_limit)
        self._sprite = self._animated_moving_sprite.sprite
        self._mover = self._animated_moving_sprite.mover
        self._animation = self._animated_moving_sprite.animation
        self._left_images = left_images
        self._right_images = right_images
        self._up_images = up_images
        self._down_images = down_images
        if self.mover.direction == Direction.LEFT:
            self._animated_moving_sprite.animation.images = self._left_images
        elif self.mover.direction == Direction.RIGHT:
            self._animated_moving_sprite.animation.images = self._right_images
        elif self.mover.direction == Direction.UP:
            self._animated_moving_sprite.animation.images = self._up_images
        elif self.mover.direction == Direction.DOWN:
            self._animated_moving_sprite.animation.images = self._down_images

    @property
    def sprite(self):
        return self._sprite

    @property
    def mover(self):
        return self._mover

    @property
    def animation(self):
        return

    @property
    def left_images(self):
        return self._left_images

    @left_images.setter
    def left_images(self, images: list):
        self._left_images = images

    @property
    def right_images(self):
        return self._right_images

    @right_images.setter
    def right_images(self, images: list):
        self._right_images = images

    @property
    def up_images(self):
        return self.up_images

    @up_images.setter
    def up_images(self, images: list):
        self._up_images = images

    @property
    def down_images(self):
        return self._down_images

    @down_images.setter
    def down_images(self, images: list):
        self._down_images = images

    def draw(self, canvas):
        self._animated_moving_sprite.draw(canvas)

    def update(self, delta_time):
        self._animated_moving_sprite.update(delta_time)
        if self.mover.direction == Direction.LEFT:
            self._animated_moving_sprite.animation.images = self._left_images
        elif self.mover.direction == Direction.RIGHT:
            self._animated_moving_sprite.animation.images = self._right_images
        elif self.mover.direction == Direction.UP:
            self._animated_moving_sprite.animation.images = self._up_images
        elif self.mover.direction == Direction.DOWN:
            self._animated_moving_sprite.animation.images = self._down_images


class AnimatedHorizontalBouncer:
    def __init__(self, leftImages: list, rightImages: list,
                 x: int = 0, y: int = 0,
                 border_color: str = 'black', border_width: int = 2,
                 fill_color: str = '',
                 direction: Direction = Direction.RIGHT,
                 delay_time: int = 100, speed: int = 1,
                 frame_delay: int = 100,
                 left_limit: int = 0, right_limit: int = 800
                 ) -> None:
        super().__init__()
        self._left_images = leftImages
        self._right_images = rightImages
        self._sprite = Sprite(x, y, 32, 32, border_color, border_width,
                              fill_color, rightImages[0])
        self._sprite.border_width = 0
        self._mover = Mover(self._sprite, direction, delay_time, speed)
        self._animation = Animation(self._sprite, rightImages, frame_delay)
        self._left_limit = left_limit
        self._right_limit = right_limit

    @property
    def left_limit(self):
        return self._left_limit

    @left_limit.setter
    def left_limit(self, left_limit: int):
        self._left_limit = left_limit

    @property
    def right_limit(self):
        return self._right_limit

    @right_limit.setter
    def right_limit(self, right_limit: int):
        self._right_limit = right_limit

    @property
    def sprite(self):
        return self._sprite

    @property
    def mover(self):
        return self._mover

    @property
    def animation(self):
        return self._animation

    def draw(self, canvas):
        self._sprite.draw(canvas)

    def update(self, delta_time):
        self._mover.update(delta_time)
        if self._mover.direction == Direction.LEFT and \
                self._sprite.left < self._left_limit:
            self._sprite.left = self._left_limit
            self._mover.direction = Direction.RIGHT

        elif self._mover.direction == Direction.RIGHT and \
                self._sprite.right > self._right_limit:
            self._sprite.right = self._right_limit
            self._mover.direction = Direction.LEFT

        if self._mover.direction == Direction.LEFT:
            self._animation.images = self._left_images
        elif self._mover.direction == Direction.RIGHT:
            self._animation.images = self._right_images

        self._animation.update(delta_time)


class AnimatedHorizontalRepeater:
    def __init__(self, leftImages: list, rightImages: list,
                 x: int = 0, y: int = 0,
                 border_color: str = 'black', border_width: int = 2,
                 fill_color: str = '',
                 direction: Direction = Direction.RIGHT,
                 delay_time: int = 100, speed: int = 1,
                 frame_delay: int = 100,
                 left_limit: int = 0, right_limit: int = 800
                 ) -> None:
        super().__init__()
        self._left_images = leftImages
        self._right_images = rightImages
        self._sprite = Sprite(x, y, 32, 32, border_color, border_width,
                              fill_color, rightImages[0])
        self._sprite.border_width = 0
        self._mover = Mover(self._sprite, direction, delay_time, speed)
        self._animation = Animation(self._sprite, rightImages, frame_delay)
        self._left_limit = left_limit
        self._right_limit = right_limit

    @property
    def left_limit(self):
        return self._left_limit

    @left_limit.setter
    def left_limit(self, left_limit: int):
        self._left_limit = left_limit

    @property
    def right_limit(self):
        return self._right_limit

    @right_limit.setter
    def right_limit(self, right_limit: int):
        self._right_limit = right_limit

    @property
    def sprite(self):
        return self._sprite

    @property
    def mover(self):
        return self._mover

    @property
    def animation(self):
        return self._animation

    def draw(self, canvas):
        self._sprite.draw(canvas)

    def update(self, delta_time):
        self._mover.update(delta_time)
        if self._mover.direction == Direction.LEFT:
            self._animation.images = self._left_images
        elif self._mover.direction == Direction.RIGHT:
            self._animation.images = self._right_images

        if self._mover.direction == Direction.LEFT and \
                self._sprite.right < self._left_limit:
            self._sprite.left = self._right_limit
        elif self._mover.direction == Direction.RIGHT and \
                self._sprite.left > self._right_limit:
            self._sprite.right = self._left_limit

        self._animation.update(delta_time)


class AnimatedVerticalBouncer:
    def __init__(self, upImages: list, downImages: list,
                 x: int = 0, y: int = 0,
                 border_color: str = 'black', border_width: int = 2,
                 fill_color: str = '',
                 direction: Direction = Direction.DOWN,
                 delay_time: int = 100, speed: int = 1,
                 frame_delay: int = 100,
                 top_limit: int = 0, bottom_limit: int = 600
                 ) -> None:
        super().__init__()
        self._up_images = upImages
        self._down_images = downImages
        self._sprite = Sprite(x, y, 32, 32, border_color, border_width,
                              fill_color, downImages[0])
        self._sprite.border_width = 0
        self._mover = Mover(self._sprite, direction, delay_time, speed)
        self._animation = Animation(self._sprite, downImages, frame_delay)
        self.top_limit = top_limit
        self._bottom_limit = bottom_limit

    @property
    def top_limit(self):
        return self._top_limit

    @top_limit.setter
    def top_limit(self, top_limit: int):
        self._top_limit = top_limit

    @property
    def bottom_limit(self):
        return self._bottom_limit

    @bottom_limit.setter
    def bottom_limit(self, bottom_limit: int):
        self._bottom_limit = bottom_limit

    @property
    def sprite(self):
        return self._sprite

    @property
    def mover(self):
        return self._mover

    @property
    def animation(self):
        return self._animation

    def draw(self, canvas):
        self._sprite.draw(canvas)

    def update(self, delta_time):
        self._mover.update(delta_time)
        if self._mover.direction == Direction.UP and \
                self._sprite.top < self.top_limit:
            self._sprite.top = self.top_limit
            self._mover.direction = Direction.DOWN

        elif self._mover.direction == Direction.DOWN and \
                self._sprite.bottom > self._bottom_limit:
            self._sprite.bottom = self._bottom_limit
            self._mover.direction = Direction.UP

        if self._mover.direction == Direction.UP:
            self._animation.images = self._up_images
        elif self._mover.direction == Direction.DOWN:
            self._animation.images = self._down_images
        self._animation.update(delta_time)

        self._animation.update(delta_time)


class AnimatedVerticalRepeater:
    def __init__(self, upImages: list, downImages: list,
                 x: int = 0, y: int = 0,
                 border_color: str = 'black', border_width: int = 2,
                 fill_color: str = '',
                 direction: Direction = Direction.DOWN,
                 delay_time: int = 100, speed: int = 1,
                 frame_delay: int = 100,
                 top_limit: int = 0, bottom_limit: int = 600
                 ) -> None:
        super().__init__()
        self._up_images = upImages
        self._down_images = downImages
        self._sprite = Sprite(x, y, 32, 32, border_color, border_width,
                              fill_color, downImages[0])
        self._sprite.border_width = 0
        self._mover = Mover(self._sprite, direction, delay_time, speed)
        self._animation = Animation(self._sprite, downImages, frame_delay)
        self.top_limit = top_limit
        self._bottom_limit = bottom_limit

    @property
    def top_limit(self):
        return self._top_limit

    @top_limit.setter
    def top_limit(self, top_limit: int):
        self._top_limit = top_limit

    @property
    def bottom_limit(self):
        return self._bottom_limit

    @bottom_limit.setter
    def bottom_limit(self, bottom_limit: int):
        self._bottom_limit = bottom_limit

    @property
    def sprite(self):
        return self._sprite

    @property
    def mover(self):
        return self._mover

    @property
    def animation(self):
        return self._animation

    def draw(self, canvas):
        self._sprite.draw(canvas)

    def update(self, delta_time):
        self._mover.update(delta_time)

        if self._mover.direction == Direction.UP and \
                self._sprite.bottom < self.top_limit:
            self._sprite.top = self.bottom_limit
        elif self._mover.direction == Direction.DOWN and \
                self._sprite.top > self._bottom_limit:
            self._sprite.bottom = self._top_limit

        if self._mover.direction == Direction.UP:
            self._animation.images = self._up_images
        elif self._mover.direction == Direction.DOWN:
            self._animation.images = self._down_images
        self._animation.update(delta_time)