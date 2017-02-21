from constants import *
import pygame
import os


class Quest_dialog():
    def __init__(self, NPC, not_active, active, compleated):
        self.font = pygame.font.SysFont('Pinewood', 20)
        self.object = NPC.object
        self.NPC = NPC
        self.name = self.font.render(self.NPC.name, 1, BROWN)

        self.answers_quest_is_not_active = not_active[1]
        self.text_quest_is_not_active = self._get_conversation_text(not_active[0])

        self.answers_quest_is_active = active[1]
        self.text_quest_is_active = self._get_conversation_text(active[0])

        self.answers_quest_is_complete = compleated[1]
        self.text_quest_is_compleat = self._get_conversation_text(compleated[0])

    def _get_conversation_text(self, text):
        level_text = []
        for string in text:
            string = string.split('&')
            item_list = []
            for i in string:
                item_list.append(self.font.render(i, 1, BROWN))
            level_text.append(item_list)
        return level_text

    def _get_active_conversation(self):
        if self.NPC.quest_taken:
            if self.NPC.quest_completed:
                return self.text_quest_is_compleat, self.answers_quest_is_complete
            else:
                return self.text_quest_is_active, self.answers_quest_is_active
        else:
            return self.text_quest_is_not_active, self.answers_quest_is_not_active

    def draw(self, clock, screen):
        quest_exit = None
        image = pygame.image.load(os.path.join('.//quests//template.jpg'))

        active_text, active_answers = self._get_active_conversation()

        number = 0
        answer_number = self._get_answer_tuple(len(active_answers[number]))
        ans_num = 0
        while not quest_exit:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        if ans_num == 0:
                            ans_num = len(answer_number) - 1
                        else:
                            ans_num -= 1
                    elif event.key == pygame.K_s:
                        if ans_num == len(answer_number) - 1:
                            ans_num = 0
                        else:
                            ans_num += 1

                    if event.key == pygame.K_RETURN:
                        quest_exit, number, answer_number, ans_num = self._get_next_step(number, ans_num, active_answers)

            screen.blit(image, (0, 400))
            screen.blit(self.name, (60,420))
            x = 0
            for element in active_text[number]:
                screen.blit(element, (120, 450+x))
                x += 25
            x = 0
            y = 0
            for answer in active_answers[number]:
                if answer_number and answer is not None:
                    ans = answer_number[ans_num][y]
                    screen.blit((answer.text[ans]), (100, 520 + x))
                    x += 25
                    y += 1

            clock.tick(60)

            pygame.display.flip()

    def _get_next_step(self, number, ans_number, answers):
        number = answers[number][ans_number].if_picked(self.NPC)
        if number != 'exit':
            answer_number = self._get_answer_tuple(len(answers[number]))
            return 0, number, answer_number, 0
        else:
            return 1, 0, 0, 0

    def _get_answer_tuple(self, number):
        string = []
        if number == 'exit':
            return None
        for n in range(number):
            new_string = [0 for i in range(number)]
            new_string[n] += 1
            string.append(tuple(new_string))

        return tuple(string)


class Answer:
    def __init__(self, text, number=0):
        font = pygame.font.SysFont('Pinewood', 20)
        self.text = (font.render(text, 1, BROWN), font.render(text, 1, GREEN))
        self.return_number = number

    def if_picked(self, NPC):
        return self.return_number


class Confirm(Answer):
    def if_picked(self, NPC):
        NPC.quest_taken = 1
        return self.return_number


class Complete_quest(Answer):
    def __init__(self, text, number, number2):
        Answer.__init__(self,text, number)
        self.number_2 = number2

    def if_picked(self, NPC):
        if not NPC.check_if_complete():
            return self.number_2
        else:
            return self.return_number


class Exit(Answer):
    def if_picked(self, NPC):
        return 'exit'


class Success(Answer):
    def if_picked(self, NPC):
        NPC.reward()
        return 'exit'









