import pygame
import os
from constants import *
from grounds import *
from characters import Bandit, Witch, NPC
from pick_objects import Health_potion, Mana_potion, Quest_object
from quest_menu import *


class Level:
    #Level superclass
    def __init__(self, player):
        # list of ground, enemies, and adding player
        self.ground_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.character_list = pygame.sprite.Group()
        self.projectile_list = pygame.sprite.Group()
        self.items_list = pygame.sprite.Group()
        self.use_list = pygame.sprite.Group()
        self.player = player
        self.character_list.add(player)
        # This is background
        self.background = None
        # Level settings
        self.shift_x = 0
        self.shift_y = 0
        self.world_limit = -1000

    def shift_level(self, shift_x, shift_y):
        self.shift_x += shift_x
        self.shift_y += shift_y

        for use in self.use_list:
            use.rect.x += shift_x
            use.rect.y += shift_y

        for item in self.items_list:
            item.rect.x += shift_x
            item.rect.y += shift_y

        for ground in self.ground_list:
            ground.rect.x += shift_x
            ground.rect.y += shift_y

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
            enemy.rect.y += shift_y

        for projectile in self.projectile_list:
            projectile.rect.x += shift_x
            projectile.rect.y += shift_y

    def update(self):
        self.items_list.update()
        self.ground_list.update()
        self.enemy_list.update()
        self.projectile_list.update()
        self.use_list.update()

    def draw(self, screen):
        screen.fill(self.background)
        self.ground_list.draw(screen)
        self.enemy_list.draw(screen)
        self.projectile_list.draw(screen)
        self.items_list.draw(screen)
        self.use_list.draw(screen)

class Training_ground(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        self.background = SKY

        # Вставлять то что в файле ниже, перед этим все удалить


        platform = Ground([".//Grass//Grass_walls.png", 200])
        platform.set_possition(-10, 275)
        self.ground_list.add(platform)

        platform = Hover_ground((500, 0, [2, 0], self, ".//Grass//Grass_walls.png", 200))
        platform.set_possition(498, 276)
        platform.get_boundaries()
        self.ground_list.add(platform)

        enemy = Bandit([self])
        enemy.set_possition(669, 359)
        enemy.get_boundaries(150)
        self.enemy_list.add(enemy)

        item = Health_potion([self])
        item.set_possition(705, 249)
        self.items_list.add(item)

        self.player.set_possition(0, 0)