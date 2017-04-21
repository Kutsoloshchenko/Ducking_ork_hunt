"""Все классы земли и платформ по которым можно ходить"""

import pygame
import os
from constants import *

class Ground(Animated_sprite):
    """Базовый класс земли, от которого наследуются все об"""
    def __init__(self, settings, ground_width = 70):

        # Получаем путь к картинке, и инициализируем родительский класс
        pygame.sprite.Sprite.__init__(self)
        self.image_path = settings[0]

        # Получаем картинку нужной длины (получается из редактора в settings[1]) и ширины
        self.image = pygame.image.load(os.path.join(self.image_path)).convert()
        self.image = self._get_image(0, 0, settings[1], ground_width, self.image)
        self.rect = self.image.get_rect()


class Small_ground(Ground):
    """Класс не широкой земли, на 20 пикселей"""
    def __init__(self, settings):
        super().__init__(settings, ground_width= 20)


class Hover_ground(Ground):
    """Класс движущейся землию Я не уверен что нам понадобится данный элемент в вестерне"""

    def __init__(self, settings):
        """Инициализируем наш класс"""
        # Загружаем родительский класс
        super().__init__([settings[4], settings[5]])

        # Получаем значение границы движения по у и по х
        self.boundary_x = settings[0]
        self.boundary_y = settings[1]

        # Получаем скорость и ссылку на уровень на котором находится земля
        self.speed = settings[2]
        self.level = settings[3]

        # Получаем непосредственные граныц
        self.get_boundaries()

    def get_boundaries(self):
        """Функция получения границы от текущего положения"""
        self.boundaries_x = (self.rect.x, self.boundary_x + self.rect.x)
        self.boundaries_y = (self.rect.y, self.boundary_y + self.rect.y)

    def on_click(self):
        """РЕДАКТОР. Функция вызывается при клике"""
        self.get_boundaries()
        self.initial_x, self.initial_y = self.rect.x, self.rect.y

    def update(self):
        """Функция обновления передвижения земли. По идее вся логика столкновений на игроке а не на земле"""
        self.rect.x += self.speed[0]

        self.rect.y +=self.speed[1]

        cur_pos = self.rect.x - self.level.shift_x
        if cur_pos <= self.boundaries_x[0] or cur_pos >= self.boundaries_x[1]:
            self.speed[0] *= -1
        cur_pos = self.rect.y - self.level.shift_y
        if cur_pos <= self.boundaries_y[0] or cur_pos >= self.boundaries_y[1]:
            self.speed[1] *= -1

class Ladder(Ground):
    """Специальный класс для лестницю Главное в нем это его имя, а в остальном это обычная земля"""
    def __init__(self):
        image = './/Grass//ladder.png'
        super().__init__(settings=(image, 150), ground_width=500)

