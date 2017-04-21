import pygame
import os
from constants import *
from grounds import *
from levels import Level
from characters import Bandit, Witch, Hero, NPC
from pick_objects import Mana_potion, Health_potion


class Redactor(Level):
    def __init__(self):
        pygame.init()
        self.size = [1280, 720]
        self.screen = pygame.display.set_mode(self.size)
        sprite_list = [(0, 97, 32, 47),
                       (32, 97, 32, 47),
                       (64, 97, 32, 47),
                       (96, 97, 32, 47)
                       ]
        self.hero = Hero('.//characters//hero.png', sprite_list)
        super().__init__(player =self.hero, file = None)
        self.hero.set_possition(0, 0)
        self.image = pygame.image.load(os.path.join('.//redactor//images//grid.bmp')).convert()
        self.image_coord = [0, 0]
        self.menu = pygame.image.load(os.path.join('.//redactor//images//menu2.jpg')).convert()
        pygame.mouse.set_visible(True)
        self.speed_x, self.speed_y = 0, 0

        self.shift_x = 0
        self.shift_y = 0

        pygame.display.set_caption("redactor")
        self.background = pygame.image.load(os.path.join('.//redactor//images//sample.jpg')).convert()
        self.clock = pygame.time.Clock()
        self.statick_menu = [
            Grass_ground_static(self.ground_list, self),
            Wood_ground_static(self.ground_list, self),
            Sand_ground_static(self.ground_list, self),
            Grass_ground_hover(self.ground_list, self),
            Bandit_statick(self.enemy_list, self),
            Witch_static(self.enemy_list, self),
            Mana_potion_static(self.items_list, self),
            Health_potion_static(self.items_list, self),
            NPC_static(self.use_list, self),
            Ladder_static(self.items_list, self)
        ]
        self.file = ".//redactor//test_file.py"
        self.update_switch = -1

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

        self.image_coord[0] += shift_x
        self.image_coord[1] += shift_y

    def _draw(self):

        self.screen.fill(WHITE)
        self.screen.blit(self.background, (self.shift_x, self.shift_y))
        #self.screen.blit(self.image, tuple(self.image_coord))
        self.ground_list.draw(self.screen)
        self.enemy_list.draw(self.screen)
        self.projectile_list.draw(self.screen)
        self.items_list.draw(self.screen)
        self.use_list.draw(self.screen)
        self.character_list.draw(self.screen)
        self.screen.blit(self.menu, (1000, 0))

        for i in self.statick_menu:
            i.draw(self.screen)

    def _reload(self):
        for use in self.use_list:
            use.reload()

        for item in self.items_list:
            item.reload()

        for enemy in self.enemy_list:
            enemy.reload()

        for projectile in self.projectile_list:
            projectile.reload()

        for ground in self.ground_list:
            ground.reload()

    def _change_speed(self,x,y):
        self.speed_x = x
        self.speed_y = y

    def _active_element(self, list, pos, active_object):
        for sprite in list:
            if sprite.rect.collidepoint(pos):
                return sprite
        return active_object

    def run(self):

        gameExit = None
        active_object = None
        while not gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    print(pos[0] - self.shift_x, pos[1] - self.shift_y)
                    if active_object:
                        active_object.set_possition(pos[0] + 1 - self.shift_x, pos[1] + 1 - self.shift_y)
                        active_object.on_click()
                        active_object.set_possition(pos[0] + 1, pos[1] + 1)
                        active_object = None

                    for sprite in self.statick_menu:
                        if sprite.rect.collidepoint(pos):
                            print(sprite.rect.x, sprite.rect.y)
                            pos = pygame.mouse.get_pos()
                            pos = (pos[0]+1 - self.shift_x, pos[1] + 1 - self.shift_y)
                            active_object = sprite.on_click(pos)

                    for list in [self.ground_list, self.enemy_list, self.character_list, self.use_list, self.items_list]:
                        active_object = self._active_element(list, pos, active_object)


                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self._change_speed(0, 0)
                    elif event.key == pygame.K_d:
                        self._change_speed(0, 0)
                    elif event.key == pygame.K_w:
                        self._change_speed(0, 0)
                    elif event.key == pygame.K_s:
                        self._change_speed(0, 0)


                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pos = pygame.mouse.get_pos()
                        print(pos[0]+1 - self.shift_x, pos[1] + 1 - self.shift_y)

                    elif event.key == pygame.K_a:
                        self._change_speed(-10, 0)
                    elif event.key == pygame.K_d:
                        self._change_speed(10, 0)
                    elif event.key == pygame.K_w:
                        self._change_speed(0, +10)
                    elif event.key == pygame.K_s:
                        self._change_speed(0, -10)
                    elif event.key == pygame.K_r:
                        self.shift_level(-1 * self.shift_x, -1 * self.shift_y)
                        self._reload()

                        self.shift_x, self.shift_y = 0, 0

                    elif event.key == pygame.K_u:
                        pos = pygame.mouse.get_pos()
                        for sprite in self.ground_list:
                            if active_object and sprite.rect.collidepoint(pos):
                                sprite.rect = sprite.rect.union(active_object)
                                active_object = None



                    elif event.key == pygame.K_t:
                        self.update_switch *= -1
                    elif event.key == pygame.K_LALT:
                        self._console_commands()
                    elif event.key == pygame.K_DELETE:
                        if active_object:
                            active_object.kill()
                            active_object = None

            if active_object:
                pos = pygame.mouse.get_pos()
                active_object.set_possition(pos[0]+1, pos[1]+1)
            self._draw()
            if self.update_switch > 0:
                self.update()
            self.shift_level(self.speed_x, self.speed_y)
            pygame.display.flip()
            self.clock.tick()

        self._reload()
        self._write_grounds()
        self._write_enemies()
        self._write_items()
        self._write_use_items()
        with open(self.file, 'a') as file:
            file.write('self.player.set_possition(%d,%d)' % (self.hero.rect.x, self.hero.rect.y))

        pygame.quit()

    def _console_commands(self):

        command = input('Введите имя команды (h - помощь)\n')

        if command == 'h':
            print('goto = переместиться в заданые координаты\n'
                  'load = загрузить уровень (прогресс потеряется, Вася, помни об этом)\n'
                  'set xy = если выбран елемент - то позволяет задавать координаты X и Y')
        elif command == 'goto':
            pass
        elif command == 'load':
            pass
        elif command == 'set xy':
            pass

    def _write_grounds(self):
        with open(self.file, 'a') as file:
            for ground in self.ground_list.sprites():
                if 'hover' in ground.__class__.__name__.lower():
                    parameters = ''.join('%s((%d, %d, [%d, %d], self, "%s" ,%d))'
                                         % (ground.__class__.__name__, ground.boundary_x, ground.boundary_y,
                                            ground.speed[0], ground.speed[1], ground.image_path, ground.rect.width)
                                         )
                    file.write('platform= %s\n' % parameters)
                    file.write('platform.set_possition(%d, %d)\n' % (ground.rect.x, ground.rect.y))
                    file.write('platform.get_boundaries()\n')
                    file.write('self.ground_list.add(platform)\n')
                    file.write('\n')

                else:

                    file.write('platform= %s(["%s", %d])\n' % (ground.__class__.__name__, ground.image_path ,ground.rect.width))
                    file.write('platform.set_possition(%d, %d)\n' % (ground.rect.x, ground.rect.y))
                    file.write('self.ground_list.add(platform)\n')
                    file.write('\n')

    def _write_enemies(self):
        with open(self.file, 'a') as file:
            for enemy in self.enemy_list.sprites():
                file.write('enemy= %s([self])\n' % enemy.__class__.__name__)
                file.write('enemy.set_possition(%d, %d)\n' % (enemy.rect.x, enemy.rect.y))
                file.write('enemy.get_boundaries(%d)\n' % int(enemy.boundary[1] - enemy.rect.x))
                file.write('self.enemy_list.add(enemy)\n')
                file.write('\n')

    def _write_items(self):
        with open(self.file, 'a') as file:
            for item in self.items_list.sprites():
                file.write('item= %s([self])\n' % item.__class__.__name__)
                file.write('item.set_possition(%d, %d)\n' % (item.rect.x, item.rect.y))
                file.write('self.items_list.add(item)\n')
                file.write('\n')

    def _write_use_items(self):
        with open(self.file, 'a') as file:
            for item in self.use_list.sprites():
                file.write('npc= %s([self, "%s"])\n' % (item.__class__.__name__, item.file))
                file.write('npc.set_possition(%d, %d)\n' % (item.rect.x, item.rect.y))
                file.write('self.use_list.add(npc)\n')
                file.write('\n')


class Static_image():
    def __init__(self, list_type, image, class_type, level):
        self.image_path = image
        self.image = pygame.image.load(os.path.join(self.image_path)).convert()
        self.rect = self.image.get_rect()
        self.list = list_type
        self.object = class_type
        self.level = level
        self.image.set_colorkey(GREEN)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def on_click(self, pos, *args):
        obj = self.object(args)
        obj.set_possition(pos[0], pos[1])
        self.list.add(obj)
        return obj


class Grass_ground_static(Static_image):

    def __init__(self, list_type, level):
        image = './/redactor//images//grass.png'
        class_type = Ground
        super().__init__(list_type, image, class_type, level)
        self.rect.x = 1010
        self.rect.y = 20
        self.image_path = './/Grass//Grass_walls.png'

    def on_click(self, pos):
        super().on_click(pos, self.image_path, int(input("Введите ширину платформы (максимум - 1000) = ")))


class Sand_ground_static(Grass_ground_static):

    def __init__(self, list_type, level):
        super().__init__(list_type, level)
        self.image = pygame.image.load(os.path.join('.//redactor//images//sand.png')).convert()
        self.rect.x = 1110
        self.rect.y = 20
        self.image_path = './/Grass//Sand_walls.png'


class Wood_ground_static(Grass_ground_static):
    def __init__(self, list_type, level):
        super().__init__(list_type, level)
        self.image = pygame.image.load(os.path.join('.//redactor//images//wood.png')).convert()
        self.rect.x = 1180
        self.rect.y = 20
        self.image_path = './/Grass//wood_walls.png'
        self.object = Small_ground


class Grass_ground_hover(Static_image):
    def __init__(self, list_type, level):
        image = './/redactor//images//grass_hover.png'
        class_type = Hover_ground
        super().__init__(list_type, image, class_type, level)
        self.rect.x = 1010
        self.rect.y = 120
        self.image_path = './/Grass//Grass_walls.png'

    def on_click(self, pos):
        x = int(input('Введите границу по оси х = '))
        y = int(input('Введите границу по оси y = '))
        speed = [int(input('Введите скорость по x = ')), int(input('Введите скорость по y = '))]
        width = int(input('Введите ширину платформы = '))
        super().on_click(pos, x, y, speed, self.level, self.image_path, width)


class Bandit_statick(Static_image):
    def __init__(self, list_type, level):
        image = './/redactor//images//bandit.png'
        class_type = Bandit
        super().__init__(list_type, image, class_type, level)
        self.rect.x = 1010
        self.rect.y = 220
    def on_click(self, pos):
        super().on_click(pos, self.level)


class Witch_static(Static_image):
    def __init__(self, list_type, level):
        image = './/redactor//images//witch.png'
        class_type = Witch
        super().__init__(list_type, image, class_type, level)
        self.rect.x = 1050
        self.rect.y = 220
    def on_click(self, pos):
        super().on_click(pos, self.level)


class Mana_potion_static(Static_image):
    def __init__(self, list_type, level):
        image = './/redactor//images//pt2_test.png'
        class_type = Mana_potion
        super().__init__(list_type, image, class_type, level)
        self.rect.x = 1050
        self.rect.y = 270

    def on_click(self, pos):
        super().on_click(pos, self.level)


class Health_potion_static(Static_image):
    def __init__(self, list_type, level):
        image = './/redactor//images//pt1_test.png'
        class_type = Health_potion
        super().__init__(list_type, image, class_type, level)
        self.rect.x = 1010
        self.rect.y = 270

    def on_click(self, pos):
        super().on_click(pos, self.level)


class Ladder_static(Static_image):
    def __init__(self, list_type, level):
        image = './/redactor//images//ladder.png'
        class_type = Ladder
        super().__init__(list_type, image, class_type, level)
        self.rect.x = 1010
        self.rect.y = 400

    def on_click(self, pos):
        super().on_click(pos, self.level)


class NPC_static(Static_image):
    def __init__(self, list_type, level):
        image = './/redactor//images//ahriman.png'
        class_type = NPC
        super().__init__(list_type, image, class_type, level)
        self.rect.x = 1090
        self.rect.y = 220

    def on_click(self, pos):
        file = input('Введите путь к файлу с квестом (ентер - ввести позже)\n')

        if file == '':
            file = './/redactor//null_quest'

        try:
            obj = self.object([self.level, file])
            obj.set_possition(pos[0], pos[1])
            obj.file = file
            self.list.add(obj)
            return obj
        except:
            print('File is not found, try again')




if __name__ == '__main__':
    redactor = Redactor()
    redactor.run()