import pygame
from constants import *
from grounds import Hover_ground
from spells import Enemy_Fireball
from pick_objects import Mana_potion, Health_potion, Quest_object
from quest_menu import *
import os


class Character(Animated_sprite):
    def __init__(self, image, sprite_list):
        pygame.sprite.Sprite.__init__(self)
        self.HP, self.MP, self.speed_x, self.speed_y, self.invul_time = [0 for i in range(5)]
        sprite_image = pygame.image.load(os.path.join(image)).convert()
        self.animation_frames_r, self.animation_frames_l = self._get_animation(sprite_image, sprite_list)
        self.image = self.animation_frames_r[0]
        self.rect = self.image.get_rect()
        self.ground = None
        self.direction = 'R'

    def dead_or_alive(self):
        if self.HP <=0 or self.rect.y > SCREEN_HEIGHT:
            self.kill()

    def gravity(self):
        # Apply gravity, and make sure we have collision with any block we are staying at
        if self.speed_y == 0:
            self.speed_y = 2
        else:
            self.speed_y += 0.35

    def jump(self):
        # Check that we have platform under, by moving 2 pixels down and checking for collision
        self.rect.y += 2
        ground_hit_list = pygame.sprite.spritecollide(self, self.ground.ground_list, False)
        self.rect.y -= 2

        # If there is ground under feet of hero - it will jump 10 inches
        if len(ground_hit_list) > 0:
            self.speed_y = -10

    def set_possition(self, x=0, y=0):
        self.rect.x = x
        self.rect.y = y

    def _animation(self):
        pos = self.rect.x + self.ground.shift_x
        if self.direction == 'R':
            frame = (pos // 30) % len(self.animation_frames_r)
            self.image = self.animation_frames_r[frame]
        else:
            frame = (pos // 30) % len(self.animation_frames_r)
            self.image = self.animation_frames_l[frame]

    def _collision_with_x(self):
        collisions_with_x = pygame.sprite.spritecollide(self, self.ground.ground_list, False)

        for hit in collisions_with_x:
            if self.speed_x > 0:
                self.rect.right = hit.rect.left
            else:
                self.rect.left = hit.rect.right

    def _collision_with_y(self):
        collisions_with_y = pygame.sprite.spritecollide(self, self.ground.ground_list, False)

        for hit in collisions_with_y:
            if self.speed_y > 0:
                self.rect.bottom = hit.rect.top
            else:
                self.rect.top = hit.rect.bottom
            self.speed_y = 0

            if isinstance(hit, Hover_ground):
                self.rect.x += hit.speed[0]

    def update(self):
        # updates position of element

        self.gravity()

        self.rect.x +=self.speed_x

        self._animation()

        self._collision_with_x()

        self.rect.y += self.speed_y
        self._collision_with_y()


class Enemy(Character):
    def __init__(self, ground, sprite_list, image):
        super().__init__(image, sprite_list)
        self.HP = 0
        self.ground = ground[0]
        self._in_boundaries = 1
        self.boundary = None

    def on_click(self):
        self.get_boundaries(int(input('Введите границы патрулирования = ')))

    def set_possition(self, x=0, y=0):
        Character.set_possition(self, x, y)
        if not self.boundary:
            self.get_boundaries(200)

    def get_boundaries(self, boundary):
        self.boundary_1 = boundary
        self.boundary = [self.rect.x, self.rect.x + self.boundary_1]

    def _check_if_will_fall(self):
        if self.speed_x > 0 and self.speed_y == 0:
            self.rect.right += 10
            self.rect.bottom += 40
            if not pygame.sprite.spritecollide(self, self.ground.ground_list, False):
                self.speed_x *= -1
            self.rect.right -= 10
            self.rect.bottom -= 40
        elif self.speed_x < 0 and self.speed_y == 0:
            self.rect.left -= 10
            self.rect.bottom += 40
            if not pygame.sprite.spritecollide(self, self.ground.ground_list, False):
                self.speed_x *= -1
            self.rect.left += 10
            self.rect.bottom -= 40

    def reload(self):
        self.rect.x = self.boundary[0]

    def _see_enemy(self):
        self.rect.x += self.vision
        if pygame.sprite.collide_rect(self, self.ground.player) and self.cool_down == 0:
            self.attack_mode = 1
            self.it_got_away = 60
        elif self.attack_mode == 1:
            self.it_got_away -= 1
            if not self.it_got_away:
                self.attack_mode = 0

        self.rect.x -= self.vision*2
        if pygame.sprite.collide_rect(self, self.ground.player) and self.cool_down == 0:
            self.attack_mode = 1
            self.it_got_away = 60
        elif self.attack_mode == 1:
            self.it_got_away -= 1
            if not self.it_got_away:
                self.attack_mode = 0
        self.rect.x += self.vision

    def _attack_if_touched(self):

        if pygame.sprite.collide_rect(self, self.ground.player):
            if not self.ground.player.invul_time:
                self.cool_down = 25
                self.attack_mode = 0
                self.ground.player.HP -= self.damage
                self.ground.player.dead_or_alive()
                self.ground.player.receive_mellie_hit()

    def _cool_downs(self):
        if self.invul_time != 0:
            self.invul_time -= 1
        if self.cool_down != 0:
            self.cool_down -= 1

    def _passing(self):
        if self.speed_x < 0:
            self.direction = 'L'
        else:
            self.direction = 'R'
        if self._in_boundaries:

            cur_pos = self.rect.x - self.ground.shift_x
            if (cur_pos >= self.boundary[0] and cur_pos >= self.boundary[1]) or (
                    cur_pos <= self.boundary[0] and cur_pos <= self.boundary[1]):
                self._in_boundaries = 0
            elif cur_pos <= self.boundary[0] or cur_pos >= self.boundary[1]:
                self.speed_x *= -1
                self._in_boundaries = 1
        else:
            cur_pos = self.rect.x - self.ground.shift_x
            if cur_pos <= self.boundary[0]+10 and self.speed_x <0:
                self.speed_x *= -1
            elif cur_pos >= self.boundary[1]-10 and self.speed_x >0:
                self.speed_x *= -1

    def update(self):

        self._see_enemy()

        self._check_if_will_fall()

        if not self.attack_mode:

            super().update()

            self._attack_if_touched()

            self._passing()

        if self.attack_mode:

            self.gravity()

            self._attack()
            self._attack_if_touched()

            self._animation()

            self._collision_with_x()

            self.rect.y += self.speed_y
            self._collision_with_y()

        self._cool_downs()


class Bandit(Enemy):
    def __init__(self, ground):
        sprite_list = [ (0, 108, 30, 50),
                        (37, 108, 30, 50),
                        (70, 108, 30, 50),
                        (102, 108, 30, 50)
        ]
        super().__init__(ground, sprite_list, image='.//characters//bandit.png')
        self.speed_x = 5
        self.HP = 25
        self.damage = 5
        self.attack_mode = 0
        self.cool_down = 0
        self.vision = 200

    def _attack(self):
        if self.ground.player.rect.x > self.rect.x:
            if self.speed_x < 0:
                self.speed_x *= -1
            self.rect.x += self.speed_x
            self.direction = 'R'
        else:
            if self.speed_x > 0:
                self.speed_x *= -1
            self.rect.x += self.speed_x
            self.direction = 'L'


class Witch(Enemy):
    def __init__(self, ground):
        sprite_list = [(0, 97, 30, 45),
                       (34, 97, 30, 45),
                       (66, 97, 30, 45),
                       (98, 97, 30, 45)
                       ]
        super().__init__(ground, sprite_list, image='.//characters//witch.png')
        self.speed_x = 5
        self.HP = 15
        self.damage = 15
        self.attack_mode = 0
        self.cool_down = 0
        self.vision = 300

    def _attack(self):
        if self.ground.player.rect.x > self.rect.x:
            self.direction = 'R'
        else:
            self.direction = 'L'

        self.ground.projectile_list.add(Enemy_Fireball(self, self.direction, self.ground.player))
        self.cool_down = 20
        self.attack_mode = 0


class Hero(Character):

    def __init__(self, image, sprite_list):
        Character.__init__(self, image, sprite_list)
        self.HP, self.MP, self.max_HP, self.max_MP = (100, 100, 100, 100)
        self._get_teleporta_frames()
        self.teleporta_time, self.spell_cd, self.inactive_time = [0 for i in range(3)]
        self.teleporta_distance = 30
        self.image_health = pygame.image.load(os.path.join('.//HUD//health.png')).convert()
        self.image_mana = pygame.image.load(os.path.join('.//HUD//mana.png')).convert()
        self._get_potions()
        self.quest_items = []

    def world_shift(self):
        if self.rect.right >= 500:
            diff = self.rect.right - 500
            self.ground.shift_level(-diff, 0)
            self.rect.right = 500
        elif self.rect.left <= 100:
            self.ground.shift_level(100 - self.rect.left, 0)
            self.rect.left = 100

        if self.rect.bottom >= 600:
            diff = self.rect.bottom - 600
            self.ground.shift_level(0, -diff)
            self.rect.bottom = 600
        elif self.rect.top <= 100:
            self.ground.shift_level(0, 100 - self.rect.top)
            self.rect.top = 100

    def cast(self, spell, directions=None):
        if self.MP - spell.mana_cost >= 0 and self.spell_cd == 0:
            self.MP -= spell.mana_cost
            self.spell_cd = 10
            if directions:
                self.ground.projectile_list.add(spell(self, directions))
            else: self.ground.projectile_list.add(spell(self))

    def _get_potions(self):
        sprite_list = [(0, 0, 90, 40),
                        (0, 50, 90, 40),
                        (0, 50*2, 90, 40),
                        (0, 50*3, 90, 40),
                        (0, 50*4, 90, 40),
                        (0, 50*5, 90, 40),
                        (0, 50*6, 90, 40),
                        (0, 50*7, 90, 40),
                        (0, 50*8, 90, 40),
                        (0, 50*9, 90, 40),
        ]
        mana_image = pygame.image.load(os.path.join('.//HUD//mana_potions(0,50y,40,90).png')).convert()
        health_image = pygame.image.load(os.path.join('.//HUD//health_potions(0,50y,40,90).png')).convert()
        self.image_mana_potion = self._get_animation(mana_image, sprite_list)[0]
        self.image_health_potion = self._get_animation(health_image, sprite_list)[0]
        self.mana_potions, self.health_potions = (0,0)

    def move_right(self):
        self.speed_x = 6
        self.direction = 'R'

    def move_left(self):
        self.speed_x = -6
        self.direction = 'L'

    def stop(self):
        self.speed_x = 0

    def teleporta(self):
        if self.MP >= 20:
            self.MP -= 20
            self.teleporta_time = 10
            self.inactive_time = 10
            self.invul_time = 10

    def _get_teleporta_frames(self):
        self.teleporta_frames = []
        sprite_image = pygame.image.load(os.path.join('.//magic_pack//sheets//teleporta.png')).convert()
        sprite_list = [ (11, 102, 5, 5),
                        (19, 102, 5, 5),
                        (27, 101, 7, 7),
                        (37, 101, 7, 7),
                        (47, 100, 8, 8),
                        (58, 99, 9, 9),
                        (70, 98, 10, 10),
                        (83, 97, 11, 11),
                        (97, 96, 12, 12),
                        (112, 95, 13, 13),
                        (128, 94, 14, 14)
        ]
        for sprite in sprite_list:
            self.teleporta_frames.append(self._get_image(sprite[0], sprite[1], sprite[2], sprite[3], sprite_image))

    def _teleporta_animation(self):
        pos = self.rect.x + self.ground.shift_x
        if self.direction == 'R':
            frame = (pos // 2) % len(self.teleporta_frames)
            self.image = self.teleporta_frames[frame]
        else:
            frame = (pos // 2) % len(self.teleporta_frames)
            self.image = self.teleporta_frames[frame]

    def _teleporta_collision(self):
        collisions_with_x = pygame.sprite.spritecollide(self, self.ground.ground_list, False)

        for hit in collisions_with_x:
            if self.direction == 'R':
                self.rect.right = hit.rect.left
            else:
                self.rect.left = hit.rect.right

    def _cool_downs(self):
        if self.spell_cd != 0:
            self.spell_cd -= 1
        if self.invul_time != 0:
            self.invul_time -= 1

    def use(self, clock, screen):
        hits = pygame.sprite.spritecollide(self, self.ground.use_list, False)
        for hit in hits:
            hit.use(clock, screen)

    def pick_up(self):
        hits = pygame.sprite.spritecollide(self, self.ground.items_list, False)

        for hit in hits:
            if isinstance(hit, Health_potion) and self.health_potions < 9:
                self.health_potions += 1
                hit.kill()
            elif isinstance(hit, Mana_potion) and self.mana_potions < 9:
                self.mana_potions += 1
                hit.kill()
            elif isinstance(hit, Quest_object):
                self.quest_items.append(hit)
                hit.kill()

    def update(self):

        if not self.teleporta_time:
            Character.update(self)
            self.pick_up()

        else:
            self.teleporta_time -= 1
            self.inactive_time -= 1

            if self.direction == 'R':
                self.rect.x += self.teleporta_distance
            else:
                self.rect.x -= self.teleporta_distance

            self._teleporta_animation()

            if self.teleporta_time == 0:
                self._teleporta_collision()

                self.rect.y += self.speed_y

                self._collision_with_y()

            if self.invul_time != 0:
                self.invul_time -= 1

        self._cool_downs()

    def drink_potion(self, type):
        if type == 'mana':
            if self.mana_potions and self.MP < self.max_MP:
                self.mana_potions -= 1
                self.MP += int(self.max_MP*0.25)
        else:
            if self.health_potions and self.HP < self.max_HP:
                self.health_potions -= 1
                self.HP += int(self.max_HP*0.25)

    def hud_draw(self, screen):
        if self.HP == 100 :
            screen.blit(self.image_health, (35, 35))
        else:
            percent = self.HP/100
            screen.blit(self.image_health, (35, 35), pygame.Rect(0, 0, 128*percent, 32))

        if self.MP == 100:
            screen.blit(self.image_mana, (35, 68))
        else:
            percent = self.MP / 100
            screen.blit(self.image_mana, (35, 68), pygame.Rect(0, 0, 128 * percent, 32))

        if self.mana_potions >= 0:
            screen.blit(self.image_mana_potion[self.mana_potions], (700, 30+40))

        if self.health_potions >= 0:
            screen.blit(self.image_health_potion[self.health_potions], (700, 30))

    def receive_mellie_hit(self):
        self.invul_time = 10
        if self.direction == 'R':
            self.rect.x -= 20
        else:
            self.rect.x +=20


class NPC(Character):
    def __init__(self, settings):
        sprite_list = [(68, 0, 25, 46)]
        not_taken, taken, completed = self._get_text_from_txt(settings[1])
        Character.__init__(self, self.image, sprite_list)
        self.ground = settings[0]
        self.quest_taken = 0
        self.quest_completed = 0
        self.quest = Quest_dialog(self, not_taken, taken, completed)

    def check_if_complete(self):
        if self.task == 'kill':
            if not self.object.alive():
                return True
            else:
                return False

        else:
            if self.object in self.ground.player.quest_items:
                self.ground.player.quest_items.remove(self.object)
                return True

            return False

    def init_quest(self):
        self.quest_taken = 1
        exec('self.object = %s' % self.target_object)
        self.object.set_possition(self.object_coordinates[0], self.object_coordinates[1])
        if self.task == 'kill':
            self.ground.enemy_list.add(self.object)
        else:
            self.ground.items_list.add(self.object)

    def use(self, clock, screen):
        self.quest.draw(clock, screen)

    def reward(self):
        if self.reward_item == 'Mana_potion':
            if self.ground.player.mana_potions < 9:
                self.ground.player.mana_potions += 1
            else:
                self.ground.items_list.add(Mana_potion(self.ground, self.rect.x-20, self.rect.y))
            self.quest_completed = 1

        if self.reward_item == 'Health_potion':
            if self.ground.player.health_potions < 9:
                self.ground.player.health_potions += 1
            else:
                self.ground.items_list.add(Health_potion(self.ground, self.rect.x-20, self.rect.y))
            self.quest_completed = 1

    def _get_text_from_txt(self, file):
        with open(file, 'r') as file:
            file_read = file.read()

        file = file_read.split('***')
        file_header = file[0]
        self._get_header_info(file_header)

        file_not_taken = file[1:3]
        file_taken = file[3:5]
        file_complete = file[5:]

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

    def _get_header_info(self, big_string):
        text = big_string.split('\n')
        self.image = text[0].split('Image = ')[1].lstrip()
        self.task = text[1].split('Task = ')[1].lstrip()
        self.target_object = text[2].split('Object = ')[1].lstrip()
        self.object_coordinates = (int(text[3].split('Object X = ')[1].lstrip()),
                                   int(text[4].split('Object y = ')[1].lstrip()))
        self.reward_item = text[5].split('Reward = ')[1].lstrip()
        self.name = text[6].split('Name = ')[1].lstrip()

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