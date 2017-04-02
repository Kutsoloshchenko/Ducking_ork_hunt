import pygame
from constants import *
from grounds import Hover_ground
from spells import Enemy_Fireball
from pick_objects import Mana_potion, Health_potion, Quest_object, Ladder
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
        self.climbing = False

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
        ground_hit_list = ground_hit_list + pygame.sprite.spritecollide(self, self.ground.items_list, False)
        self.rect.y -= 2

        # If there is ground under feet of hero - it will jump 10 inches
        for i in ground_hit_list:
            if self.rect.bottom <= i.rect.bottom:
                self.speed_y = -10
                break

    def _animation(self):
        pos = self.rect.x + self.ground.shift_x
        if self.direction == 'R':
            frame = (pos // 24) % len(self.animation_frames_r)
            self.image = self.animation_frames_r[frame]
        else:
            frame = (pos // 24) % len(self.animation_frames_r)
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


            if self.rect.bottom >= hit.rect.bottom:
                continue


            if self.rect.bottom >= hit.rect.top:
                self.rect.bottom = hit.rect.top
                self.speed_y = 0

            #else:
            #self.rect.top = hit.rect.bottom


            if isinstance(hit, Hover_ground):
                self.rect.x += hit.speed[0]

        collisions_with_ladder = pygame.sprite.spritecollide(self, self.ground.items_list, False)
        for hit in collisions_with_ladder:
            if isinstance(hit, Ladder):
                if self.rect.bottom <= hit.rect.top+20:
                    self.rect.bottom = hit.rect.top
                    self.speed_y = 0
                    break

    def update(self):
        # updates position of element

        self.rect.x +=self.speed_x

        self._animation()

        #self._collision_with_x()
        if not self.climbing:
            self.gravity()
        self.rect.y += self.speed_y
        self._collision_with_y()


class Enemy(Character):
    def __init__(self, ground, sprite_list, image):
        super().__init__(image, sprite_list)
        self.HP = 0
        self.ground = ground[0]
        self._in_boundaries = 1
        self.boundary = None
        self.revive_counter = 0

    def on_click(self):
        self.get_boundaries(int(input('Введите границы патрулирования = ')))
        self.initial_x, self.initial_y = self.rect.x, self.rect.y

    def revive(self):
        self.revive_counter +=1
        if self.revive_counter == 500:
            self.ground.dead_enemy_list.remove(self)
            self.ground.enemy_list.add(self)
            self.reload()
            self.HP = self.start_HP
            self.revive_counter = 0

    def dead_or_alive(self):
        if self.HP <= 0 or self.rect.y > SCREEN_HEIGHT:
            self.kill()
            self.ground.dead_enemy_list.append(self)

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
        self.HP, self.start_HP = 25, 25
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
        self.HP, self.start_HP = 15, 15
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
        self.HP, self.bullets_num, self.max_HP, self.max_MP = (50, 6, 100, 100)
        self._get_teleporta_frames()
        self.teleporta_time, self.spell_cd, self.inactive_time = [0 for i in range(3)]
        self.teleporta_distance = 30
        self.image_health = pygame.image.load(os.path.join('.//HUD//health.png')).convert()
        self.bullets = pygame.image.load(os.path.join('.//HUD//cilinder.jpg')).convert()
        self.image_hud = pygame.image.load(os.path.join('.//HUD//menu.jpg')).convert()
        self.empty_bar = pygame.image.load(os.path.join('.//HUD//SleekBars_empty.png')).convert()
        self.bullets_animation = self._get_bullets_animations()
        self._get_potions()
        self.quest_items = []
        self.target = pygame.image.load(os.path.join('.//HUD//target.png')).convert()
        self.target.set_colorkey(BLACK)
        pygame.mouse.set_visible(False)

    def reload(self):
        if self.bullets_num !=6 :
            self.bullets_num += 1
            self.inactive_time = 10
            file = self.ground.m_player('.//sound//Sound_exf//reload.wav')
            self.ground.m_player.play(file, loops=0)

    def world_shift(self):
        if self.rect.right >= (SCREEN_WIDTH * 4 // 5):
            diff = self.rect.right - (SCREEN_WIDTH * 4 // 5)
            self.ground.shift_level(-diff, 0)
            self.rect.right = (SCREEN_WIDTH * 4 // 5)
        elif self.rect.left <= (SCREEN_WIDTH // 5):
            self.ground.shift_level((SCREEN_WIDTH // 5) - self.rect.left, 0)
            self.rect.left = (SCREEN_WIDTH // 5)

        if self.rect.bottom >= (SCREEN_HEIGHT - 220):
            diff = self.rect.bottom - (SCREEN_HEIGHT - 220)
            self.ground.shift_level(0, -diff)
            self.rect.bottom = (SCREEN_HEIGHT - 220)
        elif self.rect.top <= (SCREEN_WIDTH // 5):
            self.ground.shift_level(0, (SCREEN_WIDTH // 5) - self.rect.top)
            self.rect.top = (SCREEN_WIDTH // 5)

    def cast(self, spell, directions=None):
        if self.bullets_num > 0 and self.spell_cd == 0:
            self.bullets_num -= 1
            self.inactive_time = 10
            if directions:
                self.ground.projectile_list.add(spell(self, directions))
                file = self.ground.m_player(spell.music_file)
                self.ground.m_player.play(file, loops = 0)
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
        health_image = pygame.image.load(os.path.join('.//HUD//whiskey(0,50y,40,90).png')).convert()
        self.image_health_potion = self._get_animation(health_image, sprite_list)[0]
        self.health_potions = 0

    def _draw_target(self, screen):
        pos = pygame.mouse.get_pos()
        offset = (pos[0] + 35, pos[1] - 35)
        screen.blit(self.target, offset)

    def move_right(self):
        self.speed_x = 6
        self.direction = 'R'

    def move_left(self):
        self.speed_x = -6
        self.direction = 'L'

    def move_up(self):
        collisions_with_ladder = pygame.sprite.spritecollide(self, self.ground.items_list, False)
        for hit in collisions_with_ladder:
            if isinstance(hit, Ladder):
                self.climbing = True
                self.speed_y = -2
                return

        self.jump()

    def fall(self):
        self.rect.y +=2
        collisions_with_y = pygame.sprite.spritecollide(self, self.ground.ground_list, False)
        collisions_with_y= collisions_with_y + pygame.sprite.spritecollide(self, self.ground.items_list, False)
        self.rect.y -= 2

        for hit in collisions_with_y:
            self.rect.bottom += 40
            break

    def stop(self):
        self.speed_x = 0

    def stop_y(self):
        if self.climbing:
            self.speed_y = 0
            self.climbing = False

    def teleporta(self):
        if self.MP >= 20:
            self.MP -= 20
            self.teleporta_time = 10
            self.inactive_time = 10
            self.invul_time = 10

    def _get_bullets_animations(self):
        return_list = []
        sprite_image = pygame.image.load(os.path.join('.//HUD//cilinder.jpg')).convert()
        y = 150
        x = 0
        sprite_list = [(x, y*0, 140, 150),
                       (x, y*1, 140, 150),
                       (x, y*2, 140, 150),
                       (x, y*3, 140, 150),
                       (x, y*4, 140, 150),
                       (x, y*5, 140, 150),
                       (x, y*6, 140, 150),
                       (x, y*7, 140, 150),
                       (x, y*8, 140, 150),
                       (x, y*9, 140, 150),
                       (x, y*10, 140, 150),
                       (x, y * 11, 140, 150)
                       ]
        for sprite in sprite_list:
            return_list.append(self._get_image(sprite[0], sprite[1], sprite[2], sprite[3], sprite_image))
        return return_list

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
        if self.inactive_time:
            self.inactive_time-=1
        Character.update(self)
        self.pick_up()
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

        screen.blit(self.image_hud, (0, SCREEN_HEIGHT-150), pygame.Rect(0, 0, SCREEN_WIDTH, 150))

        percent = self.HP/100
        screen.blit(self.empty_bar, (35, SCREEN_HEIGHT-150))
        screen.blit(self.image_health, (35, SCREEN_HEIGHT-150), pygame.Rect(0, 0, 32, 128*percent))
        screen.blit(self.bullets_animation[6-self.bullets_num], (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 150))



        if self.health_potions >= 0:
            screen.blit(self.image_health_potion[self.health_potions], (400, SCREEN_HEIGHT - 100))

        self._draw_target(screen)

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