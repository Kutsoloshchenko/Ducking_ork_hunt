"""Константы игры используемые во всех модулях"""

import pygame

# Тут у нас размеры экранна. В будущем сделаем динамическим. Используется для отрисовки разных вещей
# и для того что бы создавать экран
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Математические или физические константы
GRAVITATION = 0.35

# РГБ код часто используеммых цветов
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
SKY = (88, 157, 214)
BROWN= (127, 51, 0)
SAND = (255, 238, 155)


class Animated_sprite(pygame.sprite.Sprite):
    """Базовый класс обьекта у которого присутствует анимация. Содержит самые основные функции"""
    def on_click(self):
        """РЕДАКТОР. При установке позиции элемента сохраняет данные координаты как начальные, что бы знать
        куда поставить этот элемент при перезагрузке редактора"""

        self.initial_x, self.initial_y = self.rect.x, self.rect.y

    def reload(self):
        """РЕДАКТОР. При перезагрузке редактора устанавливает элемент в начальное положение"""
        self.rect.x, self.rect.y = self.initial_x, self.initial_y

    def set_possition(self, x=0, y=0):
        """Устанавливает координату х и у в указаные значения. Имеет значение по умолчанию 0,0.
        Используется Обьектом уровня что бы позиционировать элементы на экране"""

        self.rect.x = x
        self.rect.y = y

    @staticmethod
    def _get_image(x, y, width, height, sprite_sheet):
        """Метода который по заданным координатам верхнего левого угла (x, y), ширине и длине (width, height)
        вырезает прямоугольник из картинки. Используется для того что бы с одного файла, там где нарисованны все
        картинки анимации, вырезать одну нужную. Возвращает вырезанную картинку"""

        image = pygame.Surface([width, height]).convert()
        image.blit(sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(BLACK)
        return image


    def _get_animation(self, sprite_image, sprite_list):
        """Функция получения набора (масива) картинок для анимациию На вход принимает файл с нужными картинка и
        масив кортежей с координатами по типу - [(x,y,w,h), (x1,y1,w1,h1)...] где x и y это левый верхний угол,
        а w и h это ширина и высота прямоугольника который покрывает ону отджельную картинку"""

        walking_frames_r = []

        # Для каждого элемента набора координат мы получаем одну картинку для масива анимации
        for sprite in sprite_list:
            # Добавляем в список картинку вырезаную методом _get_image (описан выше)
            walking_frames_r.append(self._get_image(sprite[0], sprite[1], sprite[2], sprite[3], sprite_image))

        # Для левой стороны переворачиваем картинки в анимации для правой, зеркально по вертикали
        walking_frames_l = [pygame.transform.flip(image, True, False) for image in walking_frames_r]

        # Возвращаем наши два списка
        return (walking_frames_r, walking_frames_l)
    
