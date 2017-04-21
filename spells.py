"""Тут у нас заклинания которіе наносят урон"""

from constants import *
from math import sqrt, atan, cos, sin, degrees
import pygame
import os

class Spell(Animated_sprite):
    """Базовый класс заклинания от которого наследуются все"""
    def _move_x(self):
        """Базовая функция движения заклинания по оси Х и смена анимации"""
        self.rect.x += self.speed_x

        if self.direction == 'R':
            frame = (self.rect.x // 15) % len(self.animation_r)
            self.image = self.animation_r[frame]
        else:
            frame = (self.rect.x // 15) % len(self.animation_l)
            self.image = self.animation_l[frame]

    def _on_hit(self):
        """Функция которая определяет что же случается с персонажем когда в него врезается заклинание.
        В базовом классе пустое, поэтому будет переопределенно в наследнике"""
        pass

    def _check_if_should_end(self):
        """Функция котороая определяет когда заклинание должно закончиться. Определяется в классах наследниках"""
        pass

    def update(self):
        """Базовая функция обновления положения и статуса заклинания. Двигается,
        проверяет во что оно врезалось, наносит удар и проверяет не закончилось ли время действия спела"""

        self._move_x()

        hits = pygame.sprite.spritecollide(self, self.caster.ground.enemy_list, False)

        self._on_hit(hits)

        self._check_if_should_end()


class Shotgun(Spell):
    """Базовый класс заклинания Дробовика. Ближняя дистанция, большой урон, бьет всех"""
    def __init__(self, caster, sprite_image, sprite_list):
        """Функция инициализации. Получает анимации, картинки, ссылки на кастера."""
        super().__init__()
        self.caster = caster
        self.animation_r, self.animation_l = self._get_animation(sprite_image, sprite_list)
        self.image = self.animation_r[0]
        self.rect = self.image.get_rect()
        self._get_possition()

    def _get_possition(self):
        """Получает начальную позицию кастера. В зависимости от этого выбирает куда двигатся и где начинать движение"""
        self.direction = self.caster.direction
        if self.direction == 'R':
            self.rect.left = self.caster.rect.right
            self.speed_x = 8
        else:
            self.rect.right = self.caster.rect.left
            self.speed_x = -8
        self.rect.y = self.caster.rect.top - 85

    def _on_hit(self, hits):
        """Функция которая обрабатывает каждое попадание по противникам. Если противник не в инвуле,
        то уменьшает ему хп, устанавливает время инвуля и проверяет, не померла ли цель."""

        for hit in hits:
            if not hit.invul_time:
                hit.HP -= self.damage
                hit.invul_time = 10
                hit.dead_or_alive()

    def _check_if_should_end(self):
        """Проверяет не должно ли заклинание закончится.
        Для дробовика оно проверяет - не достигла ли анимация последней картинки или нет."""

        if self.image == self.animation_r[-1] or self.image == self.animation_l[-1]:
            self.kill()
            del self


class Ground_spell(Spell):
    """Заклинания типа динамит. Взрывается при столкновении с землей, наносит уровн всем в зоне поражения.
    Чем ближе к центру - тем больше урона. Заканчивается или по времени, или при первом столкновении с землей.
    Именно таким оно будет, пока что его нет"""
    pass


class Projectile(Spell):
    """Заклинание одиночного выстрела. """

    # Звук выстрела хранится именно тут. У всех спелов будет свой файл звука выстрела и или взрыва.
    music_file = './/sound//Sound_exf//shot.wav'

    def __init__(self, caster, sprite_image, pos):
        """Функция инициализации. Получает картинку, анимации, и траекторию, что выражается в скорости по х и по у.
        Ну и ссылку на кастера получает"""
        super().__init__()
        self.caster = caster
        y = 64 * 4
        sprite_list = [(0, y, 64, 64),
                       (64, y, 64, 64),
                       (64 * 2, y, 64, 64),
                       (64 * 3, y, 64, 64),
                       (64 * 4, y, 64, 64),
                       (64 * 5, y, 64, 64),
                       (64 * 6, y, 64, 64),
                       (64 * 7, y, 64, 64)
                       ]

        self.animation_r, self.animation_l = self._get_animation(sprite_image, sprite_list)
        self.image = self.animation_r[0]
        self.rect = self.image.get_rect()
        self.speed_x, self.speed_y = self._find_traectory(pos)

    def _player_move(self):
        """Функция которая устанавливает позицию игрока в зависимости от направления выстрела"""
        if self.direction == 'R':
            self.caster.direction = 'R'
            if self.caster.speed_x == 0:
                self.caster.image = self.caster.standing_ani[0]
        else:
            self.caster.direction = 'L'
            if self.caster.speed_x == 0:
                self.caster.image = self.caster.standing_ani[1]

    def _find_traectory(self, pos):
        """Функция поиска траектории и направления движения для пули"""

        # Вначале находим в какую сторону полетит снаряд, и где будет его начальная точка
        if pos[0] >= self.caster.rect.x:
            # Если стреляли вправо, тоесть координата мыши больше координаты игрока, то летим в плюсовые координаты
            self.direction = 'R'
            original_x = self.caster.rect.right
            was_x = 1
            was_y = 1
        else:
            # Если нет, то используем минусовые координаты
            self.direction = 'L'
            original_x = self.caster.rect.left
            # А так же переворачиваем анимацию заклинани
            was_x = -1
            was_y = -1

        # Выставляем игрока в нужную позицию
        self._player_move()

        # Находим катеты прямоугольного треугольника,
        # который получается если соеденить точку начала и точку указаную мышкой
        x = pos[0] - original_x
        y = pos[1] - self.caster.rect.y - 20

        # Находим угол межджу гипотенузой и горизонтальным катетом
        angle = atan(y/x)

        # При помощи магии математики получаем скорость по оси х и у так,
        # что бы в сумме снаряд проходил 15 пикселей по гипотенузе за один кадр
        x = 15 * cos(angle) * was_x
        y = 15 * sin(angle) * was_y

        # Поворачиваем анимацию на угол между нашими сторонами.
        # Так как на ноль делить нельзя, то вставляем условие что если ноль, то поворачиваем на 90 градусов
        if x != 0:
            self.animation_r = [pygame.transform.rotate(i, degrees(-1*atan(y/x))) for i in self.animation_r]
            self.animation_l = [pygame.transform.rotate(i, degrees(-1*atan(y/x))) for i in self.animation_l]
        else:
            self.animation_r = [pygame.transform.rotate(i, degrees(-90)) for i in self.animation_r]
            self.animation_l = [pygame.transform.rotate(i, degrees(-90)) for i in self.animation_l]
        self.rect.x = original_x
        # Возвращаем наши скорости
        return x, y

    def _on_hit(self, hits):
        """При столкновении наносим урон, и уничтожаем снаряд."""
        if hits:
            if not hits[0].invul_time:
                hits[0].HP -= self.damage
                hits[0].invul_time = 10
                hits[0].dead_or_alive()
                self.kill()
                del self

    def _check_if_should_end(self):
        """Заклинание действует определенное кол во фреймов. Єта функция каждій фрейм отнимает один от времени.
        Когда достигаеит нуля - убирает заклинание"""
        self.duration -=1
        if self.duration <=0:
            self.kill()
            del self

    def update(self):
        """Добавляет заклинанию движение по оси У, так как пуля летит и вверх"""
        super().update()

        self.rect.y += self.speed_y

        hits = pygame.sprite.spritecollide(self, self.caster.ground.enemy_list, False)

        self._on_hit(hits)


class Fireball(Projectile):
    """Заклинание типа фаербол. Обічній проджектайл со своими свойствами и картинкой"""

    def __init__(self, caster):

        sprite_image = pygame.image.load(os.path.join('.//magic_pack//sheets//fireball_0.png')).convert()
        self.damage = 5
        pos = pygame.mouse.get_pos()
        super().__init__(caster, sprite_image, pos)
        self.duration = 60
        self.rect.y = self.caster.rect.top - 20


class Fire_lion(Shotgun):
    """Заклинание для шотгана. Его надо переделывать, поэтому коментов пока не будет"""
    mana_cost = 10

    def __init__(self, caster):
        sprite_image = pygame.image.load(os.path.join('.//magic_pack//sheets//firelion_right.png')).convert()
        sprite_list = [ (0, 0, 130, 130),
                        (130, 0, 130, 130),
                        (260, 0, 130, 130),
                        (390, 0, 130, 130),
                        (0, 130, 130, 130),
                        (130, 130, 130, 130),
                        (260, 130, 130, 130),
                        (390, 130, 130, 130),
                        (0, 260, 130, 130),
                        (130, 260, 130, 130),
                        (260, 260, 130, 130),
                        (390, 260, 130, 130),
                        (0, 390, 130, 130),
                        (130, 390, 130, 130),
                        (260, 390, 130, 130),
                        (390, 390, 130, 130)
        ]
        super().__init__(caster, sprite_image, sprite_list)
        self.damage = 30


class Enemy_projectile(Projectile):
    """Специальный класс, который перезаписывает функцию обновления у вражеских спелов.
    После этого они работают точно так же как и обычные, но при этом демажат игрока"""
    def update(self):
        self._move_x()

        hits = pygame.sprite.collide_rect(self, self.caster.ground.player)
        if hits:
            self._on_hit([self.caster.ground.player])

        self._check_if_should_end()


# """Что бы сделать копию заклинания для врага, нужно наследовать два класа,
# первый это базовый класс заклинания, а второй - класс вражеского заклинания"""
class Enemy_Fireball(Fireball, Enemy_projectile):
    """Фаербол врага"""
    pass

