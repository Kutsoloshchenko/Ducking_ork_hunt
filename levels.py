import pygame
import os
from constants import *
from grounds import *
from characters import Bandit, Witch, NPC
from pick_objects import Health_potion, Mana_potion, Quest_object, Ladder
from quest_menu import *
from random import choice


class Level:
    #Level superclass
    def __init__(self, player,file = None):
        # list of ground, enemies, and adding player
        self.ground_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.dead_enemy_list = []
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

        if file:
            self._play(file)

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
        for i in self.dead_enemy_list:
                i.revive()

        self.items_list.update()
        self.ground_list.update()
        self.enemy_list.update()
        self.projectile_list.update()
        self.use_list.update()

    def draw(self, screen):
        screen.blit(self.background, (self.shift_x, self.shift_y))
        self.ground_list.draw(screen)
        self.enemy_list.draw(screen)
        self.projectile_list.draw(screen)
        self.items_list.draw(screen)
        self.use_list.draw(screen)

    def _play(self, file):
        pygame.mixer.init()
        self.m_player = pygame.mixer.Sound
        self.m_player.play(file, loops=-1)

class Training_ground(Level):
    def __init__(self, player):
        file = './/sound//Music//sound.wav'
        file = pygame.mixer.Sound(file = file)
        Level.__init__(self, player, file)
        self.level_size = (3072, 2304)
        self.background = pygame.image.load(os.path.join('.//BackGround//sample.jpg')).convert()

        # Вставлять то что в файле ниже, перед этим все удалить

        platform = Small_ground([".//Grass//wood_walls.png", 150])
        platform.set_possition(2159, 1343)
        self.ground_list.add(platform)

        item = Ladder([self])
        item.set_possition(1580, 1627)
        self.items_list.add(item)

        platform = Ground([".//Grass//Sand_walls.png", 1000])
        platform.set_possition(2000, 2233)
        self.ground_list.add(platform)

        platform = Ground([".//Grass//Sand_walls.png", 1000])
        platform.set_possition(1000, 2233)
        self.ground_list.add(platform)

        platform = Small_ground([".//Grass//wood_walls.png", 600])
        platform.set_possition(1538, 1113)
        self.ground_list.add(platform)

        platform = Small_ground([".//Grass//wood_walls.png", 600])
        platform.set_possition(1537, 1642)
        self.ground_list.add(platform)

        platform = Ground([".//Grass//Sand_walls.png", 1000])
        platform.set_possition(0, 2233)
        self.ground_list.add(platform)

        platform = Small_ground([".//Grass//wood_walls.png", 175])
        platform.set_possition(1364, 1792)
        self.ground_list.add(platform)

        platform = Small_ground([".//Grass//wood_walls.png", 100])
        platform.set_possition(1329, 1944)
        self.ground_list.add(platform)

        platform = Small_ground([".//Grass//wood_walls.png", 100])
        platform.set_possition(1175, 2096)
        self.ground_list.add(platform)

        platform = Small_ground([".//Grass//wood_walls.png", 100])
        platform.set_possition(1979, 1486)
        self.ground_list.add(platform)

        self.player.set_possition(173, 301)




class second_lvl(Level):
    def __init__(self, player):
        file = './/sound//Music//sound.wav'
        file = pygame.mixer.Sound(file = file)
        Level.__init__(self, player, file)
        self.background = pygame.image.load(os.path.join('.//redactor//images//sample.jpg')).convert()


        platform = Small_ground([".//Grass//wood_walls.png", 150])
        platform.set_possition(19, 374)
        self.ground_list.add(platform)

        self.player.set_possition(39, 317)
        platform = Ground([".//Grass//Sand_walls.png", 1000])
        platform.set_possition(0, 541)
        self.ground_list.add(platform)

        self.player.set_possition(0, 0)
        enemy = Bandit([self])
        enemy.set_possition(572, 483)
        enemy.get_boundaries(200)
        self.enemy_list.add(enemy)

        enemy = Bandit([self])
        enemy.set_possition(807, 248)
        enemy.get_boundaries(150)
        self.enemy_list.add(enemy)

        item = Health_potion([self])
        item.set_possition(924, 275)
        self.items_list.add(item)

        item = Health_potion([self])
        item.set_possition(552, 505)
        self.items_list.add(item)

        platform = Small_ground([".//Grass//wood_walls.png", 175])
        platform.set_possition(9, 372)
        self.ground_list.add(platform)

        platform = Small_ground([".//Grass//wood_walls.png", 200])
        platform.set_possition(212, 425)
        self.ground_list.add(platform)

        platform = Small_ground([".//Grass//wood_walls.png", 270])
        platform.set_possition(700, 316)
        self.ground_list.add(platform)

        platform = Small_ground([".//Grass//wood_walls.png", 300])
        platform.set_possition(686, 427)
        self.ground_list.add(platform)

        self.player.set_possition(39, 317)
