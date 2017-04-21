"""Главный файл игры. Тут мы описываем само построение игры и как она идет"""

# На работе рефакторинг я не делаю что бы ничего не сломать. Буду писать в коментах что тут надо сделать.

import pygame
import os
from constants import *
from characters import Hero, Bandit
from grounds import *
from spells import Fire_lion, Fireball
from levels import Training_ground


def main():
    """Функция основной игры. Надо оформить в класс, и по сути дать ему заниматся только выбором уровня.
    А сам уровень уже будет сканировать действия и все обновлять и рисовать."""

    # Инициализируем движок игры
    pygame.init()

    # создаем экран и задаем ему параметры
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size,pygame.FULLSCREEN)

    # Устанавливаем название окна
    pygame.display.set_caption("Wizard West^ Spellslinger")

    # Тут у нас создается игрок и его рисунки и спрайты.
    # Это надо вынести в отдельный уровень создания героя, или если фигурка героя будет одна - то в лкасс героя
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

    # Тут продолжаем инициализировать героя и пилить костыли по его добавлению в игру.
    # Этого быть не должно, все надо перенести или в создание персонажа, или в класс героя
    hero = Hero('.//characters//E_2.png', sprite_list)

    # Добавляем стоящую анимацию. Это я вынесу в класс персонажа, что бы такие анимации были у всех врагов и так далее.
    image = pygame.image.load(os.path.join('.//characters//E_2_standing.png')).convert()
    image.set_colorkey(BLACK)
    hero.standing_ani = [image, pygame.transform.flip(image, True, False)]

    # Создаем список уровней и наполняем его, всеми уровнями которые у нас есть.
    # Думаю что лучше будет это сделать дикшенари, но посмотрим
    level_list = []
    level_list.extend([Training_ground(hero)])

    # Устанавливаем текущий уровень
    level_number = 0
    current_level = level_list[level_number]

    # Создаем активные элементы и добавдяем туда героя. Плюс даем герою ссылку на текущий уровень.
    active_elements = pygame.sprite.Group()
    hero.ground = current_level

    active_elements.add(hero)

    # Создаем часы и токен окончания игры. Когда токен будет тру - игры выходит
    clock = pygame.time.Clock()
    gameExit = False

    while not gameExit:
        # Собственно сам цикл игры. Пока он выполняется игра идет

        # тут у нас проверяются нажатыве кнопки игроком, и в зависимости от них что то происходит.
        # Это надо переносить на уровень, и нам тогда будет легче менять управление в диалогах, меню и обычной игре
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gameExit = True

            if event.type == pygame.MOUSEBUTTONDOWN:
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
                elif event.key == pygame.K_e:
                    hero.drink_potion()
                elif event.key == pygame.K_RETURN:
                    hero.use(clock, screen)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    hero.stop()
                elif event.key == pygame.K_w:
                    hero.stop_y()

        # Тут у нас идут обновления и отрисовки. Тогже надо вынести на уровень наверное,
        # что бы главный луп просто переводил нас с уровня на уровень в зависимости от надобности.
        active_elements.update()
        current_level.update()

        # Проверяем, не надо ли сдвигать мир
        hero.world_shift()

        # Заполняем экран фоном, и потом отрисовываем все элементы
        screen.fill(SAND)
        current_level.draw(screen)
        hero.hud_draw(screen)
        active_elements.draw(screen)

        # Тут мы следим за тем что бы у нас было 60 кадров в секунду
        clock.tick(60)

        # и вызываем функцию что бы все обновилось
        pygame.display.flip()

    # если мы вышли из цикла, то просто выходим из игры
    pygame.quit()

if __name__ == '__main__':
    # запускаем игры, стандартная питоновская тема
    main()