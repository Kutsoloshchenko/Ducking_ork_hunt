import pygame
import os
from constants import *
from grounds import Hover_ground


class Pickappble_object(Animated_sprite):
    """Базовый класс всех елементов которые можно поднимать"""
    def __init__(self, ground, image):
        """Инициализирует обьект, придает ему нулевую скорость, и получает изображение"""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(image)).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.speed_y = 0
        self.ground = ground

    def update(self):
        """По сути следит за тем что бы предмет упал если он будет висеть в воздухе"""
        self.gravity()
        self.rect.y += self.speed_y

        collisions_with_y = pygame.sprite.spritecollide(self, self.ground.ground_list, False)

        for hit in collisions_with_y:
            if self.speed_y > 0:
                self.rect.bottom = hit.rect.top
            else:
                self.rect.top = hit.rect.bottom
            self.speed_y = 0

            if isinstance(hit, Hover_ground):
                self.rect.x += hit.speed[0]

    def gravity(self):
        """Точно такая же гравитация как у персонажей"""

        # Apply gravity, and make sure we have collision with any block we are staying at
        if self.speed_y == 0:
            self.speed_y = 2
        else:
            self.speed_y += 0.35



class Health_potion(Pickappble_object):
    """Хэлс поушен. Получает картинку жизни просто"""
    def __init__(self, ground):
        image = './/items//whiskey.png'
        super().__init__(ground[0], image)


class Mana_potion(Pickappble_object) :
    """Мана поушен. Получает картинку манны просто"""
    def __init__(self, ground):
        image = './/items//pt2_test.png'
        super().__init__(ground[0], image)


class Quest_object(Pickappble_object):
    """Квестовый обьект. Получает картинку при инициплизации"""
    def __init__(self, ground):
        super().__init__(ground[0], ground[1])

