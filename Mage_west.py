"""Главный файл игры. Тут мы описываем само построение игры и как она идет"""

# На работе рефакторинг я не делаю что бы ничего не сломать. Буду писать в коментах что тут надо сделать.

import pygame
import os
from constants import *
from characters import Hero
from grounds import *
from levels import Training_ground


class Game:
    """Класс игры. Вынесенно в класс что бы у нас была в уровне отсылка на нужные елементы (экран, часы и так далее)"""
    def __init__(self):
        """Функция запускается перед началом игры и инициализирует все необходимые данные"""

        # Инициализируем движок игры
        pygame.init()

        # создаем экран и задаем ему параметры
        size = [SCREEN_WIDTH, SCREEN_HEIGHT]
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

        # Устанавливаем название окна
        pygame.display.set_caption("Wizard West: Spellslinger")

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
        self.hero = Hero('.//characters//E_2.png', sprite_list)

        # Добавляем стоящую анимацию. Это я вынесу в класс персонажа,
        # что бы такие анимации были у всех врагов и так далее.
        image = pygame.image.load(os.path.join('.//characters//E_2_standing.png')).convert()
        image.set_colorkey(BLACK)
        self.hero.standing_ani = [image, pygame.transform.flip(image, True, False)]

        # Создаем список уровней и наполняем его, всеми уровнями которые у нас есть.
        # Думаю что лучше будет это сделать дикшенари, но посмотрим
        self.level_list = []
        self.level_list.extend([Training_ground(self.hero)])

        # Устанавливаем текущий уровень
        self.level_number = 0
        self.current_level = self.level_list[self.level_number]

        # Создаем активные элементы и добавдяем туда героя. Плюс даем герою ссылку на текущий уровень.
        self.hero.ground = self.current_level

        # Создаем часы и токен окончания игры. Когда токен будет тру - игры выходит
        self.clock = pygame.time.Clock()
        self.gameExit = False

    def game_loop(self):
        while not self.gameExit:
            # Собственно сам цикл игры. Пока он выполняется игра идет

            # тут у нас проверяются нажатыве кнопки игроком, и в зависимости от них что то происходит.
            # Это надо переносить на уровень, и нам тогда будет легче менять управление в диалогах, меню и обычной игре
            self.gameExit = self.current_level.player_control(self)

            # Тут у нас идут обновления и отрисовки. Тогже надо вынести на уровень наверное,
            # что бы главный луп просто переводил нас с уровня на уровень в зависимости от надобности.
            self.hero.update()
            self.current_level.update()

            # Проверяем, не надо ли сдвигать мир
            self.hero.world_shift()

            # Заполняем экран фоном, и потом отрисовываем все элементы
            self.screen.fill(SAND)
            self.current_level.draw(self.screen)
            self.hero.hud_draw(self.screen)
            self.active_elements.draw(self.screen)

            # Тут мы следим за тем что бы у нас было 60 кадров в секунду
            self.clock.tick(60)

            # и вызываем функцию что бы все обновилось
            pygame.display.flip()

            # Проверяем, не надо ли нам перейти на новый уровень.
            # Функции сцены и предметы могут менять значения level_number
            self._check_level()

            # если мы вышли из цикла, то просто выходим из игры
        pygame.quit()

    def _check_level(self):
        """Функция проверки уровня. Если уровень поменялся, то сообщает об этом герою"""
        if self.current_level != self.level_list[self.level_number]:
            self.current_level = self.level_list[self.level_number]
            self.hero.ground = self.hero.ground = self.current_level


if __name__ == '__main__':
    # запускаем игры, стандартная питоновская тема
    WizardWest = Game()
    WizardWest.game_loop()