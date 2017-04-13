import pygame
import os
from constants import *
from characters import Hero, Bandit
from grounds import *
from spells import Fire_lion, Fireball, Ice_spikes
from levels import Training_ground

def main():

    pygame.init()
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size,pygame.FULLSCREEN)

    pygame.display.set_caption("Wizard West^ Spellslinger")

    x = 180
    y = 237

    sprite_list = [(x * 0, y * 0, x, y),
                       (x * 1, y * 0, x, y),
                       (x * 2, y * 0, x, y),
                       (x * 3, y * 0, x, y),
                       (x * 4, y * 0, x, y),
                       (x * 5, y * 0, x, y),
                       (x * 6, y * 0, x, y),
                       (x * 7, y * 0, x, y),
                       (x * 8, y * 0, x, y),
                       (x * 9, y * 0, x, y),
                       (x * 10, y * 0, x, y),
                       (x * 11, y * 0, x, y)
                   ]


    hero = Hero('.//characters//E_2.png', sprite_list)

    image = pygame.image.load(os.path.join('.//characters//E_2_standing.png')).convert()
    image.set_colorkey(BLACK)
    hero.standing_ani = [image, pygame.transform.flip(image, True, False)]

    level_list = []
    level_list.extend([Training_ground(hero)])

    level_number = 0
    current_level = level_list[level_number]

    active_elements = pygame.sprite.Group()
    hero.ground = current_level
    active_elements.add(hero)
    clock = pygame.time.Clock()
    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gameExit = True

            if hero.inactive_time:
                break

            elif event.type == pygame.MOUSEBUTTONDOWN:
                hero.cast(Fireball)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    hero.reload()
                elif event.key == pygame.K_a:
                    hero.move_left()
                elif event.key == pygame.K_d:
                    hero.move_right()
                elif event.key == pygame.K_w:
                    hero.move_up()
                elif event.key == pygame.K_s:
                    hero.fall()
                elif event.key == pygame.K_LSHIFT:
                    hero.cast(Fire_lion)
                elif event.key == pygame.K_KP6:
                    hero.cast(Fireball, 'R')
                elif event.key == pygame.K_KP9:
                    hero.cast(Fireball, 'RU')
                elif event.key == pygame.K_KP3:
                    hero.cast(Fireball, 'RD')
                elif event.key == pygame.K_KP4:
                    hero.cast(Fireball, 'L')
                elif event.key == pygame.K_KP7:
                    hero.cast(Fireball, 'LU')
                elif event.key == pygame.K_KP1:
                    hero.cast(Fireball, 'LD')
                elif event.key == pygame.K_KP0:
                    hero.cast(Ice_spikes)
                elif event.key == pygame.K_q:
                    hero.drink_potion('mana')
                elif event.key == pygame.K_e:
                    hero.drink_potion()
                elif event.key == pygame.K_RETURN:
                    hero.use(clock, screen)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    hero.stop()
                elif event.key == pygame.K_w:
                    hero.stop_y()


            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                hero.teleporta()

        active_elements.update()
        current_level.update()

        hero.world_shift()

        screen.fill(SAND)
        current_level.draw(screen)
        hero.hud_draw(screen)
        active_elements.draw(screen)



        clock.tick(60)

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()