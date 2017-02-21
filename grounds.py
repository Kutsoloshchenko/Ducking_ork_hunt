import pygame
import os
from constants import *

class Ground(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(image)).convert()
        self.rect = self.image.get_rect()

    def set_possition(self, x=0, y=0):
        self.rect.x = x
        self.rect.y = y


class Hover_ground(Ground):
    def __init__(self, x, y, speed, level, characters_list, image):
        super().__init__(image)
        self.boundaries_x = x
        self.boundaries_y = y
        self.speed = speed
        self.level = level
        self.characters = characters_list

    def update(self):
        self.rect.x += self.speed[0]

        hit = pygame.sprite.spritecollide(self, self.characters, False)

        for object in hit:
            if self.speed[0] > 0:
                object.rect.left = self.rect.right
            else:
                object.rect.right = self.rect.left

        self.rect.y +=self.speed[1]

        hit = pygame.sprite.spritecollide(self, self.characters, False)

        for object in hit:
            if self.speed[1] > 0:
                object.rect.top = self.rect.bottom
            else:
                object.rect.bottom = self.rect.top


        cur_pos = self.rect.x - self.level.shift
        if cur_pos <= self.boundaries_x[0] or cur_pos >= self.boundaries_x[1]:
            self.speed[0] *= -1
        if self.rect.bottom <= self.boundaries_y[0] or self.rect.top >= self.boundaries_y[1]:
            self.speed[1] *= -1