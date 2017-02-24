import pygame
import os
from constants import *
from grounds import *
from characters import Bandit, Witch, Ahriman_mage, Elf_girl
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
        self.shift = 0
        self.world_limit = -1000

    def shift_level(self, shift_x):
        self.shift += shift_x

        for use in self.use_list:
            use.rect.x += shift_x

        for item in self.items_list:
            item.rect.x += shift_x

        for ground in self.ground_list:
            ground.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

        for projectile in self.projectile_list:
            projectile.rect.x += shift_x

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

    def _get_text_from_txt(self, file):
        file = open(file, 'r')
        file_read = file.read()
        file.close()

        file = file_read.split('***')
        file_not_taken = file[0:2]
        file_taken = file[2:4]
        file_complete = file[4:]

        not_taken = self._get_object_from_list(file_not_taken)
        taken = self._get_object_from_list(file_taken)
        comleated = self._get_object_from_list(file_complete)

        for el in not_taken:
            for element in el:
                if not element:
                    el.remove(element)

        for el in taken:
            for element in el:
                if not element:
                    el.remove(element)

        for el in comleated:
            for element in el:
                if not element:
                    el.remove(element)

        return not_taken, taken, comleated

    def _get_object_from_list(self, list):
        text = list[0].split('\n')
        text = [i.lstrip() for i in text]
        answers = list[1].split('\n')
        return_answers = []
        for i in answers:
            answers_list = i.split('@')
            temp = []
            for answer in answers_list:
                answer_from_func = self._get_class_from_answer(answer)
                if answer_from_func:
                    temp.append(self._get_class_from_answer(answer))
            return_answers.append(temp)

        return [text, return_answers]

    def _get_class_from_answer(self, answer):
        answer_line = answer.split('#')
        answer_line = [i.lstrip() for i in answer_line]
        if 'Confirm' in answer_line[0]:
            return Confirm(answer_line[1], int(answer_line[2]))
        elif 'Answer' in answer_line[0]:
            return Answer(answer_line[1], int(answer_line[2]))
        elif 'Exit' in answer_line[0]:
            return Exit(answer_line[1])
        elif 'Complete_quest' in answer_line[0]:
            return Complete_quest(answer_line[1], int(answer_line[2]), int(answer_line[3]))
        elif 'Success' in answer_line[0]:
            return Success(answer_line[1])


class Training_ground(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        self.background = SKY

        wall = Ground('.//Grass//stonewall.png')
        wall.set_possition(0, 0)
        self.ground_list.add(wall)

        wall = Ground('.//Grass//Grass_wals.png')
        wall.set_possition(0, SCREEN_HEIGHT-70)
        self.ground_list.add(wall)

        wall = Ground('.//Grass//Grass_wals.png')
        wall.set_possition(1600, SCREEN_HEIGHT - 70)
        self.ground_list.add(wall)

        platform = Ground('.//Grass//big_grass.png')
        platform.set_possition(250, 185)
        self.ground_list.add(platform)


        platform = Ground('.//Grass//block_grass.png')
        platform.set_possition(480, SCREEN_HEIGHT - 210)
        self.ground_list.add(platform)

        platform = Ground('.//Grass//block_grass.png')
        platform.set_possition(300, SCREEN_HEIGHT - 210)
        self.ground_list.add(platform)

        platform = Hover_ground((0, 0), (280, 400), [0, -2], self, self.character_list, './/Grass//block_grass.png')
        platform.set_possition(130, 344)
        self.ground_list.add(platform)

        platform = Hover_ground((700, 1300), (0, 0), [2, 0], self, self.character_list, './/Grass//block_grass.png')
        platform.set_possition(700, 185)
        self.ground_list.add(platform)

        platform = Ground('.//Grass//small_grass.png')
        platform.set_possition(1450, 250)
        self.ground_list.add(platform)


        item = Health_potion(self)
        item.set_possition(200,200)
        self.items_list.add(item)

        item = Mana_potion(self)
        item.set_possition(1800, 500)
        self.items_list.add(item)

        gem = Quest_object(self)
        gem.set_possition(300,200)
        self.items_list.add(gem)

        witch = Witch(self, (750, SCREEN_HEIGHT-150, 400))

        self.enemy_list.add(witch)
        self.enemy_list.add(Bandit(self, (400, 135, 400)))

        file = os.path.join('.//quests//ahriman_quest')
        not_taken, taken, comleated = self._get_text_from_txt(file)
        quest_npc = Ahriman_mage(self, witch, (1600, 200), Mana_potion, 'kill', not_taken, taken, comleated)
        self.use_list.add(quest_npc)

        file = os.path.join('.//quests//forest_elf_quest')
        not_taken, taken, comleated = self._get_text_from_txt(file)
        quest_npc = Elf_girl(self, gem, (2000, 200), Health_potion, 'bring', not_taken, taken, comleated)
        self.use_list.add(quest_npc)