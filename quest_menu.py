"""Это модуль для отображения и обработки логики разговора и квеста"""

from constants import *
import pygame
import os


class Quest_dialog(Scene):
    def __init__(self, NPC, not_active, active, compleated):
        """Функция инициализации диалога. Принимает ссылку на НПС который его выдал,
        и три списка списка реплик и ответов персонажа"""

        # Аплоудим шрифт отображения записей. Возможно стоит это вынести или в глайвный файл игры, или в константы
        self.font = pygame.font.SysFont('Pinewood', 26)

        self.NPC = NPC

        # Рендерим имя НПС, что бы оно было готово для отображения
        self.name = self.font.render(self.NPC.name, 1, BROWN)

        # Записываем ответы и текст для одного диалога в отдельные переменные.
        # Функция get_conversation_text делит текст на несколько линий, если необходимо, и рендерит через наш шрифт.
        # Тоесть готовит для отображением обычной функцией блит

        # Тут у нас диалог когда квест еще не взяли
        self.answers_quest_is_not_active = not_active[1]
        self.text_quest_is_not_active = self._get_conversation_text(not_active[0])

        # Тут у нас текст и ответы когда мы квест взяли, но еще не выполнили
        self.answers_quest_is_active = active[1]
        self.text_quest_is_active = self._get_conversation_text(active[0])

        # Тут у нас слова когда мы уже закончили квест, и игрок снова говорит с персонажем
        self.answers_quest_is_complete = compleated[1]
        self.text_quest_is_complete = self._get_conversation_text(compleated[0])

    def _get_conversation_text(self, text):
        """Разделяет текст на строчки и подстрочки если необходимо, и рендерит текст для отображения"""
        level_text = []
        for string in text:
            string = string.split('&')
            item_list = []
            for i in string:
                item_list.append(self.font.render(i, 1, BROWN))
            level_text.append(item_list)
        return level_text

    def _get_active_conversation(self):
        """Определяет какой диалог включать. Запрашивает у НПС состояние квеста,
        и отправляет соответсвующий ответ и реплики персонажа"""

        if self.NPC.quest_taken:
            if self.NPC.quest_completed:
                return self.text_quest_is_complete, self.answers_quest_is_complete
            else:
                return self.text_quest_is_active, self.answers_quest_is_active
        else:
            return self.text_quest_is_not_active, self.answers_quest_is_not_active

    def run(self, clock, screen):
        """Непосредственно функция отрисовки квеста, которую запускает НПС.
        Получает контроль на часами и экраном игры"""

        quest_exit = None
        # На экран накладывает изображение диалога
        sprite_sheet = pygame.image.load(os.path.join('.//quests//template.jpg'))
        image = pygame.Surface([SCREEN_WIDTH, 200]).convert()
        image.blit(sprite_sheet, (0, 0), (0, 0, SCREEN_WIDTH, 200))
        # Получает неплодимые ответы и реплики, в зависимости от состояния квеста
        active_text, active_answers = self._get_active_conversation()

        # Номер реплики НПС, и соответствующих ответов которая отрисовывается на экране
        number = 0

        # Номер выбранного ответа
        ans_num = 0
        while not quest_exit:

            # Считываем инпут с клавиатуры
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        # Если нажимаем w то движемся вверх по списку,
                        # или переходим к последнему ответу (если стоим на первом)
                        if ans_num == 0:
                            ans_num = len(active_answers[number]) - 1
                        else:
                            ans_num -= 1
                    elif event.key == pygame.K_s:
                        # Двигаемся по списку вниз
                        if ans_num == len(active_answers[number]) - 1:
                            ans_num = 0
                        else:
                            ans_num += 1

                    if event.key == pygame.K_RETURN:
                        # При нажатии ентере выбираем ответ, и вызываем функцию получения следующего шага,
                        # из которой полчаем новое состояние диалога, при этом передав текущее
                        quest_exit, number, ans_num = self._get_next_step(number, ans_num, active_answers)

            # Рисуем темплейт диалога и имя нпс
            screen.blit(image, (0, SCREEN_HEIGHT - 200))
            screen.blit(self.name, (60 , SCREEN_HEIGHT-195))

            # Отрисовываем текст нпс, отступая по координате у вниз на 25 после каждой строки
            y = 0
            for element in active_text[number]:
                screen.blit(element, (250, (SCREEN_HEIGHT-180)+y))
                y += 25

            # Отрисовываем ответы. Х это номер ответа, а У - отступ по оси у для каждого ответа
            x = 0
            y = 0
            for answer in active_answers[number]:
                if active_answers[number].index(answer) == ans_num:
                    temp = 1
                else:
                    temp = 0

                screen.blit((answer.text[temp]), (100, (SCREEN_HEIGHT-150) + y))
                y += 25
                x += 1

            # Выставляем фрейм рейт
            clock.tick(60)
            # Обновляем отображение экрана
            pygame.display.flip()

    def _get_next_step(self, number, ans_number, answers):
        """Функция получения следуего списка ответов, и реплик.
            Если есть сигнал на выход - посылает флажок выхода в цикл"""
        number = answers[number][ans_number].if_picked(self.NPC)
        if number != 'exit':
            return 0, number, 0
        else:
            return 1, 0, 0


class Answer:
    """Базовый класс ответа. Содержит в себе текст двух цветов, и номер к которому ведет выбор данного ответа"""

    def __init__(self, text, number=0):
        """Функция инициализации. Берет текст и номер реплик к которым ведет"""
        font = pygame.font.SysFont('Pinewood', 26)
        self.text = (font.render(text, 1, BROWN), font.render(text, 1, GREEN))
        self.return_number = number

    def if_picked(self, NPC):
        """Функция которая вызывается когда ответ выбирают. Просто возвращает номер куда нужно перейти"""
        return self.return_number


class Confirm(Answer):
    def if_picked(self, NPC):
        """Функция которая вызывается когда ответ выбирают. Возвращает номер куда нужно перейти,
        а так же сообщает НПС что нужно пометить квест как активный"""
        NPC.init_quest()
        return self.return_number


class Complete_quest(Answer):
    def __init__(self, text, number, number2):
        """Функция инициализации. Когда вызывается, все проходит как у обычного ответа,
        но так же добавляется дополнительный вариант развития событий"""

        Answer.__init__(self, text, number)
        self.number_2 = number2

    def if_picked(self, NPC):
        """Функция которая вызывается когда ответ выбирают.
        Возвращает вариант ответа НПС, если квест действительно выполнен, или если персонаж врет."""

        if not NPC.check_if_complete():
            return self.number_2
        else:
            return self.return_number


class Exit(Answer):
    def if_picked(self, NPC):
        """Возвращает метку выхода из диалога"""
        return 'exit'


class Success(Answer):
    def if_picked(self, NPC):
        """Вначале сообщает НПС что он должен наградить героя, а потом посылает метку выхода из квеста"""
        NPC.reward()
        return 'exit'









