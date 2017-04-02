import pygame
import os
from constants import *

class Ground(Animated_sprite):
    def __init__(self, settings, ground_width = 70):
        pygame.sprite.Sprite.__init__(self)
        self.image_path = settings[0]
        self.image = pygame.image.load(os.path.join(self.image_path)).convert()
        self.image = self._get_image(0, 0, settings[1], ground_width, self.image)
        self.rect = self.image.get_rect()



class Small_ground(Ground):
    def __init__(self, settings):
        super().__init__(settings, ground_width= 20)


class Hover_ground(Ground):

    def __init__(self, settings):
        super().__init__([settings[4], settings[5]])
        self.boundary_x = settings[0]
        self.boundary_y = settings[1]
        self.speed = settings[2]
        self.level = settings[3]
        self.get_boundaries()

    def get_boundaries(self):
        self.boundaries_x = (self.rect.x, self.boundary_x + self.rect.x)
        self.boundaries_y = (self.rect.y, self.boundary_y + self.rect.y)

    def on_click(self):
        self.get_boundaries()
        self.initial_x, self.initial_y = self.rect.x, self.rect.y

    def update(self):
        self.rect.x += self.speed[0]

        hit = pygame.sprite.spritecollide(self, self.level.character_list, False)

        for object in hit:
            if self.speed[0] > 0:
                object.rect.left = self.rect.right
            else:
                object.rect.right = self.rect.left

        self.rect.y +=self.speed[1]

        hit = pygame.sprite.spritecollide(self, self.level.character_list, False)

        for object in hit:
            if self.speed[1] > 0:
                object.rect.top = self.rect.bottom
            else:
                object.rect.bottom = self.rect.top


        cur_pos = self.rect.x - self.level.shift_x
        if cur_pos <= self.boundaries_x[0] or cur_pos >= self.boundaries_x[1]:
            self.speed[0] *= -1
        cur_pos = self.rect.y - self.level.shift_y
        if cur_pos <= self.boundaries_y[0] or cur_pos >= self.boundaries_y[1]:
            self.speed[1] *= -1


class Grass_hover_ground(Hover_ground):
    def __init__(self, args):
        image = './/Grass//Grass_walls.png'
        x, y, speed, level, width = args
        super().__init__(x, y, speed, level, image, width)


class Grass_ground(Ground):
    def __init__(self, args):
        image = './/Grass//Grass_walls.png'
        width = args[0]
        print(width)
        super().__init__(image, width)



