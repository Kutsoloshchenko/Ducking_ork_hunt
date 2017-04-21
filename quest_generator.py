def quest_generator():
    array = header()

def quest_stage():

    def write(array):
        for i in array:
            print(i, array.index(i))

    array_to_write = []

    k = ''
    while k == '':
        array_to_write.append(input('Введите слова нпс\n'))
        write(array_to_write)
        k = input('Если вы закончили редактировать, введите любой символ. Если нет - нажмите enter\n')

    answers_array = []

    for entry in array_to_write:
        k = ''
        while k == '':
            type = input('Выберите тип ответа\n '
                         ' 1 - Обычный ответ\n'
                         ' 2 - Взять квест 3\n'
                         ' 3 - Проверка выполнения квеста\n'
                         ' 4 - Успешное завершение квеста\n'
                         ' 5 - Выход из диалога\n'
                         ' 6 - помощь\n')

            if type == '1':
                text = input('Введите текст ответа\n')
                write(array_to_write)
                number = input('Введите номер ответа нпс куда ведет данный ответ\n')

                answers_array.append('Answer# %s# %s@' % (text, number))

            elif type == '2':
                text = input('Введите текст активации квеста\n')
                write(array_to_write)
                number = input('Введите номер ответа нпс куда ведет данный ответ\n')

                answers_array.append('Answer# %s# %s@' % (text, number))

            elif type == '3':
                text = input('Введите текст проверки выполнения квеста\n')
                write(array_to_write)
                number = input('Введите номер ответа нпс куда ведет выполненый квест\n')
                number2 = input('Введите номер ответа нпс куда ведет не выполненный квест\n')

                answers_array.append('Answer# %s# %s# %s@' % (text, number, number2))

            elif type == '4':
                text = input('Введите текст при успешного завершении квеста\n')
                write(array_to_write)

                answers_array.append('Answer# %s# %s@' % (text, number))


def header():
     array_to_write = []
     path = 'Image = &s' % input('Введите путь к картинке персонажа квестодателя\n')
     array_to_write.append(path)

     task = input('Выберите задание\n 1 - убийство \n 2 - нахождение предмета\n')
     if task == '1':
         array_to_write.append('Task = kill')
         enemy = input('Выберите обьект квестовый\n 1 - Бандит\n 2 - Ведьма\n ')
         if enemy == '1':
             array_to_write.append('Object = Bandit([self.ground])')
         else:
             array_to_write.append('Object = Witch([self.ground])')
     else:
         array_to_write.append('Task = find')
         array_to_write.append('Object = Quest_object([self.ground])')

     x = 'Object X = &s' % input('Введите координату Х квестового задания\n')
     array_to_write.append(x)
     y = 'Object y = &s' % input('Введите координату y квестового задания\n')
     array_to_write.append(y)

     reward = input('Выберите награду\n 1 - Мана поушен\n 2 - Хэлс поушен\n ')

     if reward == '1':
         array_to_write.append('Reward = Mana_potion')
     else:
         array_to_write.append('Reward = Health_potion')

     name = 'Name = ' % input('Введите имя NPC\n')
     array_to_write.append(name)

     return array_to_write
