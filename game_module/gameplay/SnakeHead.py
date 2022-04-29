"""SnakeHead.py: File that handle the snake head display and movement"""

import pygame
from game_module.gameplay.Enumerations import Movement, CollideType
from game_module.gameplay.Apple import Apple
from game_module.gameplay.Settings import Grill

__author__ = "Magalie Vandenbriele"
__credits__ = ["Magalie Vandenbriele", "Pierre Ghyzel", "Irama Chaouch"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Magalie Vandenbriele"
__email__ = "magalie.vandenbriele@epitech.eu"

HEAD_UP = "game/assets/snake/head_up.png"
HEAD_DOWN = "game/assets/snake/head_down.png"
HEAD_LEFT = "game/assets/snake/head_left.png"
HEAD_RIGHT = "game/assets/snake/head_right.png"
SPEED = 8


class SnakeHead:
    actual_head = None
    head_position = None

    def __init__(self, window, window_size, save_movement=None, save_head=None):
        self._heads = {Movement.UP: pygame.image.load(HEAD_UP).convert_alpha(),
                       Movement.DOWN: pygame.image.load(HEAD_DOWN).convert_alpha(),
                       Movement.LEFT: pygame.image.load(HEAD_LEFT).convert_alpha(),
                       Movement.RIGHT: pygame.image.load(HEAD_RIGHT).convert_alpha()}
        self._sprite_size = 32
        self._window = window
        self._window_size = window_size
        self._next_head_movement = []
        if save_movement is None:
            self.actual_head = Movement.UP
            self.head_position = ((round(window_size[0] / self._sprite_size) / 2 * self._sprite_size), (round(window_size[1] / self._sprite_size) / 2 * self._sprite_size))
        else:
            self.actual_head = save_movement
            self.head_position = save_head

    def get_head_info(self):
        return Grill(self.actual_head, self.head_position[0], self.head_position[1])

    def collide(self, apple):
        if self.head_position[0] < 0 or (self.head_position[0] + self._sprite_size) > self._window_size[0] \
                or self.head_position[1] < 0 or (self.head_position[1] + self._sprite_size) > self._window_size[1]:
            return CollideType.BORDER
        middle_snake_x = self.head_position[0] + (self._sprite_size / 2)
        middle_snake_y = self.head_position[1] + (self._sprite_size / 2)
        middle_apple_x = apple.position[0] + (apple.sprite_size / 2)
        middle_apple_y = apple.position[1] + (apple.sprite_size / 2)
        if middle_snake_x == middle_apple_x and middle_snake_y == middle_apple_y:
            apple.generate()
            return CollideType.APPLE
        return CollideType.NONE

    def display(self):
        self._window.blit(self._heads[self.actual_head], self.head_position)

    def update(self):
        square_x = self.head_position[0] / self._sprite_size
        square_y = self.head_position[1] / self._sprite_size
        grill = None
        if square_x.is_integer() and square_y.is_integer() and len(self._next_head_movement) > 0:
            tmp = self._next_head_movement.pop(0)
            while tmp == self.actual_head and len(self._next_head_movement) > 0:
                tmp = self._next_head_movement.pop(0)
            if tmp is not self.actual_head:
                self.actual_head = tmp
                grill = Grill(tmp, square_x, square_y)
        if self.actual_head == Movement.UP:
            self.head_position = (self.head_position[0], self.head_position[1] - SPEED)
        elif self.actual_head == Movement.DOWN:
            self.head_position = (self.head_position[0], self.head_position[1] + SPEED)
        elif self.actual_head == Movement.LEFT:
            self.head_position = (self.head_position[0] - SPEED, self.head_position[1])
        elif self.actual_head == Movement.RIGHT:
            self.head_position = (self.head_position[0] + SPEED, self.head_position[1])
        return grill

    def event_trigger(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and (len(self._next_head_movement) == 0 or self._next_head_movement[0] != Movement.LEFT):
                if self.actual_head is not Movement.RIGHT:
                    self._next_head_movement.append(Movement.LEFT)
            elif event.key == pygame.K_RIGHT \
                    and (len(self._next_head_movement) == 0 or self._next_head_movement[0] != Movement.RIGHT):
                if self.actual_head is not Movement.LEFT:
                    self._next_head_movement.append(Movement.RIGHT)
            elif event.key == pygame.K_UP \
                    and (len(self._next_head_movement) == 0 or self._next_head_movement[0] != Movement.UP):
                if self.actual_head is not Movement.DOWN:
                    self._next_head_movement.append(Movement.UP)
            elif event.key == pygame.K_DOWN \
                    and (len(self._next_head_movement) == 0 or self._next_head_movement[0] != Movement.DOWN):
                if self.actual_head is not Movement.UP:
                    self._next_head_movement.append(Movement.DOWN)
