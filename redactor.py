import pygame
import os
from constants import *
from grounds import *

class Redactor():
    def __init__(self):
        pygame.init()
        self.size = [1280, 720]
        self.shift_x = 0
        self.shift_y = 0
        self.screen = pygame.display.set_mode(self.size)
        self.ground_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.character_list = pygame.sprite.Group()
        self.projectile_list = pygame.sprite.Group()
        self.items_list = pygame.sprite.Group()
        self.use_list = pygame.sprite.Group()
        pygame.display.set_caption("redactor")
        self.background = (WHITE)
        self.clock = pygame.time.Clock()
        self.statick_menu = [Ground_long_static(self.ground_list)]
        self.file = ".//redactor//test_file.py"

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

    def _draw(self):

        self.screen.fill(self.background)
        self.ground_list.draw(self.screen)
        self.enemy_list.draw(self.screen)
        self.projectile_list.draw(self.screen)
        self.items_list.draw(self.screen)
        self.use_list.draw(self.screen)
        pygame.draw.rect(self.screen, BLACK, (950, 0, 10, 720))
        for i in self.statick_menu:
            i.draw(self.screen)

    def run(self):

        gameExit = None
        active_object = None
        while not gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    print(pos)
                    if active_object:
                        active_object = None

                    for sprite in self.statick_menu:
                        if sprite.rect.collidepoint(pos):
                            print(sprite.rect.x, sprite.rect.y)
                            active_object = sprite.on_click()


                    for sprite in self.ground_list.sprites():
                        if sprite.rect.collidepoint(pos):
                            active_object = sprite

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pos = pygame.mouse.get_pos()
                        print(pos[0]+1, pos[1]+1)

                    elif event.key == pygame.K_a:
                        self.shift_level(-10,0)
                    elif event.key == pygame.K_d:
                        self.shift_level(10, 0)
                    elif event.key == pygame.K_w:
                        self.shift_level(0, -10)
                    elif event.key == pygame.K_s:
                        self.shift_level(0, +10)
                    elif event.key == pygame.K_r:
                        self.shift_level(-1*self.shift_x, -1*self.shift_y)
                    elif event.key == pygame.K_DELETE:
                        if active_object:
                            active_object.kill()
                            active_object = None

            if active_object:
                pos = pygame.mouse.get_pos()
                active_object.set_possition(pos[0]+1, pos[1]+1)
            self._draw()
            pygame.display.flip()
            self.clock.tick()

        self._write_grounds()
        pygame.quit()

    def _write_grounds(self):
        for ground in self.ground_list.sprites():
            file = open(self.file, 'a')
            file.write('platform=Ground()\n')
            file.write('platform.set_possition(%d, %d)\n' % (ground.rect.x, ground.rect.y))
            file.write('self.ground_list.add(platform)\n')
            file.write('\n')
            file.close()


class Static_image():
    def __init__(self, list_type, image, class_type):
        self.image_path = image
        self.image = pygame.image.load(os.path.join(self.image_path)).convert()
        self.rect = self.image.get_rect()
        self.list = list_type
        self.object = class_type
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    def on_click(self):
        obj = self.object(self.image_path)
        obj.set_possition(0,0)
        self.list.add(obj)

class Ground_long_static(Static_image):
    def __init__(self, list_type):
        image = './/Grass//block_grass.png'
        class_type = Ground
        super().__init__(list_type, image, class_type)
        self.rect.x = 1100
        self.rect.y = 100





if __name__ == '__main__':
    redactor = Redactor()
    redactor.run()