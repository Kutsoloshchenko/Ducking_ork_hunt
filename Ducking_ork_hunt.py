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
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Ducking Ork Hunt")

    sprite_list = [(0, 97, 32, 47),
                   (32, 97, 32, 47),
                   (64, 97, 32, 47),
                   (96, 97, 32, 47)
                   ]
    hero = Hero('.//characters//green_mage.png', sprite_list)

    hud = pygame.image.load(os.path.join('.//HUD//SleekBars_empty.png')).convert()

    level_list = []
    level_list.extend([Training_ground(hero)])

    level_number = 0
    current_level = level_list[level_number]

    active_elements = pygame.sprite.Group()
    hero.ground = current_level
    hero.rect.x = 100
    hero.rect.bottom = SCREEN_HEIGHT - 70 - 100
    active_elements.add(hero)
    clock = pygame.time.Clock()
    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if hero.inactive_time:
                break

            if event.type == pygame.QUIT:
                gameExit = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    hero.move_left()
                elif event.key == pygame.K_d:
                    hero.move_right()
                elif event.key == pygame.K_w:
                    hero.jump()
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
                    hero.drink_potion('health')
                elif event.key == pygame.K_RETURN:
                    hero.use(clock, screen)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    hero.stop()
                elif event.key == pygame.K_d:
                    hero.stop()

            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                hero.teleporta()

        active_elements.update()
        current_level.update()

        hero.world_shift()


        current_level.draw(screen)
        screen.blit(hud, (35, 35))
        hero.hud_draw(screen)
        active_elements.draw(screen)



        clock.tick(60)

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()