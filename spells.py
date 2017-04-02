from constants import *
from math import sqrt, atan, cos, sin, degrees
import pygame
import os

class Spell(Animated_sprite):
    def _move_x(self):
        self.rect.x += self.speed_x

        if self.direction == 'R':
            frame = (self.rect.x // 15) % len(self.animation_r)
            self.image = self.animation_r[frame]
        else:
            frame = (self.rect.x // 15) % len(self.animation_l)
            self.image = self.animation_l[frame]

    def _on_hit(self):
        pass

    def _check_if_should_end(self):
        pass

    def update(self):
        self._move_x()

        hits = pygame.sprite.spritecollide(self, self.caster.ground.enemy_list, False)

        self._on_hit(hits)

        self._check_if_should_end()


class Flamer(Spell):
    def __init__(self, caster, sprite_image, sprite_list):
        super().__init__()
        self.caster = caster
        self.animation_r, self.animation_l = self._get_animation(sprite_image, sprite_list)
        self.image = self.animation_r[0]
        self.rect = self.image.get_rect()
        self._get_possition()

    def _get_possition(self):
        self.direction = self.caster.direction
        if self.direction == 'R':
            self.rect.left = self.caster.rect.right
            self.speed_x = 8
        else:
            self.rect.right = self.caster.rect.left
            self.speed_x = -8
        self.rect.y = self.caster.rect.top - 85

    def _on_hit(self, hits):
        for hit in hits:
            if not hit.invul_time:
                hit.HP -= self.damage
                hit.invul_time = 10
                hit.dead_or_alive()

    def _check_if_should_end(self):
        if self.image == self.animation_r[-1] or self.image == self.animation_l[-1]:
            self.kill()


class Ground_spell(Spell):
    def __init__(self, caster, sprite_image, sprite_list):
        super().__init__()
        self.caster = caster
        self.animation =  self._get_animation(sprite_image, sprite_list)[0]
        self.image = self.animation[0]
        self.rect = self.image.get_rect()
        if self.caster.direction == 'R':
            self.rect.x = self.caster.rect.right + self.distance
        else:
            self.rect.x = self.caster.rect.left - self.distance - self.caster.rect.width*3
        self.rect.bottom = self.caster.rect.bottom + 35

    def _on_hit(self, hits):
        for hit in hits:
            if not hit.invul_time:
                hit.HP -= self.damage
                hit.invul_time = 10
                hit.dead_or_alive()

    def _check_if_should_end(self):
        if self.time == self.max_time:
            self.kill()

    def _move_x(self):
        self.time += 1
        frame = (self.time // 3) % len(self.animation)
        self.image = self.animation[frame]

    def update(self):

        if not self._check_if_on_ground():
            self.caster.MP += 35
            self.kill()

        else:
            super().update()

    def _check_if_on_ground(self):
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, self.caster.ground.ground_list, False)
        self.rect.y -= 2

        if hits:
            return True
        else:
            return False


class Projectile(Spell):

    speed_y = 0
    speed_x = 0
    music_file = './/sound//Sound_exf//shot.wav'

    def __init__(self, caster, sprite_image, direction):
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

        self.animation = self._get_animation(sprite_image, sprite_list)
        self.image = self.animation[0]
        self.rect = self.image.get_rect()
        self.speed_x, self.speed_y = self._mouse_shot()

    def _get_direction(self, direction):
        self.direction = direction
        if 'R' in self.direction:
            self.caster.direction = 'R'
        else:
            self.caster.direction = 'L'

        if self.direction is 'RU':
            y = 64*3
            self.speed_x = self.diagonal_speed
            self.speed_y = -1*self.diagonal_speed
        elif self.direction is 'R':
            y = 64*4
            self.speed_x = self.standart_speed
        elif self.direction is 'RD':
            y= 64*5
            self.speed_x = self.diagonal_speed
            self.speed_y = self.diagonal_speed
        elif self.direction is 'LU':
            y = 64
            self.speed_x = -1*self.diagonal_speed
            self.speed_y = -1*self.diagonal_speed
        elif self.direction is 'L':
            y = 0
            self.speed_x = -1*self.standart_speed
        elif self.direction is 'LD':
            y = 7*64
            self.speed_x = -1*self.diagonal_speed
            self.speed_y = self.diagonal_speed
        sprite_list = [ (0, y, 64, 64),
                        (64, y, 64, 64),
                        (64 * 2, y, 64, 64),
                        (64 * 3, y, 64, 64),
                        (64 * 4, y, 64, 64),
                        (64 * 5, y, 64, 64),
                        (64 * 6, y, 64, 64),
                        (64 * 7, y, 64, 64)
                           ]
        return sprite_list

    def _mouse_shot(self):
        pos = pygame.mouse.get_pos()

        if pos[0] >= self.caster.rect.x :
            self.direction = 'R'
            original_x = self.caster.rect.right
            was_x = 1
            was_y = 1
        else:
            self.direction = 'L'
            original_x = self.caster.rect.left
            was_x = -1
            was_y = -1

        x = pos[0] - original_x
        y = pos[1] - self.caster.rect.y - 20

        a = atan(y/x)

        x = 15 * cos(a) * was_x
        y = 15 * sin(a) * was_y

        if x != 0:
            self.animation = [pygame.transform.rotate(i, degrees(-1*atan(y/x))) for i in self.animation]
        else:
            self.animation = [pygame.transform.rotate(i, degrees(-90)) for i in self.animation]
        self.rect.x = original_x
        return x, y

    def _move_x(self):
        self.rect.x += self.speed_x

        pos = self.rect.x
        frame = (pos // 15) % len(self.animation)
        self.image = self.animation[frame]

    def _on_hit(self, hits):
        if hits:
            if not hits[0].invul_time:
                hits[0].HP -= self.damage
                hits[0].invul_time = 10
                hits[0].dead_or_alive()
                self.kill()

    def _check_if_should_end(self):
        self.duration -=1
        if self.duration <=0:
            self.kill()
            del self

    def update(self):
        super().update()

        self.rect.y += self.speed_y

        hits = pygame.sprite.spritecollide(self, self.caster.ground.enemy_list, False)

        self._on_hit(hits)

    def _get_animation(self, sprite_image, sprite_list):
        walking_frames_r = []

        for sprite in sprite_list:
            walking_frames_r.append(self._get_image(sprite[0], sprite[1], sprite[2], sprite[3], sprite_image))

        return walking_frames_r


class Fireball(Projectile):

    def __init__(self, caster, direction):
        sprite_image = pygame.image.load(os.path.join('.//magic_pack//sheets//fireball_0.png')).convert()
        self.damage = 5
        super().__init__(caster, sprite_image, direction)
        self.duration = 60
        self.rect.y = self.caster.rect.top - 20


class Fire_lion(Flamer):
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


class Ice_spikes(Ground_spell):

    mana_cost = 35

    def __init__(self, caster):
        self.time = 0
        self.max_time = 30
        self.damage = 50
        self.distance = 150
        sprite_image = pygame.image.load(os.path.join('.//magic_pack//sheets//icetacle.png')).convert()
        sprite_list = [ (0, 0, 128, 128),
                        (128, 0, 128, 128),
                        (128 * 2, 0, 128, 128),
                        (128 *3, 0, 128, 128),

                        (0, 128, 128, 128),
                        (128, 128, 128, 128),
                        (128 * 2, 128, 128, 128),
                        (128 * 3, 128, 128, 128),

                        (0, 128 * 2, 128, 128),
                        (128, 128 * 2, 128, 128),
                        (128*2, 128 * 2, 128, 128),
                        (128*3, 128 * 2, 128, 128),

                        (0, 128 * 3, 128, 128),
                        (128, 128 * 3, 128, 128),
                        (128*2, 128 * 3, 128, 128),
                        (128*3, 128 * 3, 128, 128),

        ]
        super().__init__(caster, sprite_image, sprite_list)


class Enemy_projectile(Projectile):
    def update(self):
        self._move_x()

        hits = pygame.sprite.collide_rect(self, self.hero)
        if hits:
            self._on_hit([self.hero])

        self._check_if_should_end()


class Enemy_Fireball(Enemy_projectile):
    def __init__(self, caster, direction, hero):
        sprite_image = pygame.image.load(os.path.join('.//magic_pack//sheets//fireball_0.png')).convert()
        self.standart_speed = 10
        self.hero = hero
        self.diagonal_speed = int(sqrt(pow(self.standart_speed, 2) / 2))
        self.damage = 5
        super().__init__(caster, sprite_image, direction)
        self.range = self.rect.x + self.speed_x * 40
        self.rect.y = self.caster.rect.top - 20