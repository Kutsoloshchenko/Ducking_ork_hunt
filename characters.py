"""Модуль с классами персонажей. Все первсонажи наследуют баззовый класс Character
   который определяет основные способы движения и взаимодействия"""

# Импортим все. Слава Украине

import pygame
from constants import *
from grounds import Hover_ground, Ladder
from useobjects import NewSceneTrigger
from spells import Enemy_Fireball
from pick_objects import Mana_potion, Health_potion, Quest_object
from quest_menu import *
import os


class Character(Animated_sprite):
    """Базовый класс любого персонажа. Наследуется врагами и героем. Сам по себе наследует класс Animated sprite"""
    def __init__(self, image, sprite_list):
        """Класс инициализации. Вызывается один раз, при создании экземпляра данного класса. На вход берет
           файл с картинками анимации, и список кортеджей координат конкретных картинок
           по типу - [(x,y,w,h), (x1,y1,w1,h1)...] (в Animated_sprite смотри _get_image)"""

        # Запускаем инициализатор класса движка что бы наш класс получил все плюшки спрайта
        pygame.sprite.Sprite.__init__(self)
        # Устанавливаем все основные характеристики, которые изменяются в ходе игры, в начальное значение 0
        self.speed_x, self.speed_y, self.invul_time = [0 for i in range(3)]

        # Тут мы загружаем наш файл со всеми рисунками в движок, а потом получаем два списка, один с анимацией на правую
        # сторону, один на левую. Пока только для ходьбы, но все получение анимации будет идти сюда.
        # Нап. карабкается, стреляет, бежит, получил удар и т.д.
        # Метод _get_animation определен в родительском классе Animated_sprite
        sprite_image = pygame.image.load(os.path.join(image)).convert()
        self.animation_frames_r, self.animation_frames_l = self._get_animation(sprite_image, sprite_list)

        # Изначальной картинкой, отображаемой на экране, принимаем первую картинку в списке
        self.image = self.animation_frames_r[0]
        self.standing_ani = None
        # Получаем размеры этой картинки, точнее специальный обьект который строит невидимый прямоугольник
        # по этой картинке, и через этот прямоугольник мы получаем всякие геометрические данные типа координат и размеров
        self.rect = self.image.get_rect()
        # Тут мы устанавливаем направление персонажа НАПРАВО (что бы прога знала какую анимацию врубать). Деус Вульт
        self.direction = 'R'
        # Тумблер состояние персонажа. В данный момент персонаж не карабкается по лестнице.
        # В будещем этих тумблеров будет много (стреляет, бежит, получил удар и т.д.)
        self.climbing = False

    def dead_or_alive(self):
        """Функция проверки, а не помер ли наш персонаж. Если его ХП стало меньше 0,, то функция убирает его с экрана"""
        if self.HP <= 0:
            # Это функция определенна в классе спрайта движка pygame.sprite.Sprite, она просто убирает данный спрайт из
            # всех списков спрайтов в которых он есть. В нашем случае, так как отрисовываются только группы,
            # персонаж перестает отрисовываться на экране.
            self.kill()

    def gravity(self):
        """Функция которая эмулирует базовую гравитацию"""

        # Если персонаж не падает в данный момент и не прыгает, то даем ему скорость
        # 2 (тоесть он падает вниз, для игрыка знаки наоборот). В дальнейшем, если он стоит на земле,
        # эта земля вернет ему нейтральную скорость, а если не стоит на земле, то он начнет падать.
        if self.speed_y == 0:
            self.speed_y = 2
        else:
            # А вот если он уже в процессе падения или прыжка, мы добавляем к его скорости падения гравитационную константу,
            # в нашей игре 0.35
            self.speed_y += GRAVITATION

    def _check_if_standing(self):
        """Проверяем, стоит ли персонаж на земле. Перемещаем его на два пикселя вниз, сохраняем все столкновения
           и возвращаем персонажа на место. Возвращаем список (а вот если он пуст, то мы падаем)"""
        self.rect.y += 2
        ground_hit_list = pygame.sprite.spritecollide(self, self.ground.groups['ground'], False)
        self.rect.y -= 2

        return ground_hit_list

    def jump(self):
        """Функция прыжка. Проверяем можем ли мы прыгнуть, и если можем - то уменьшает скорость по игрику"""

        for i in self._check_if_standing():
            # Смотрим на тот элемент с которым мы столкнулись. Если мы выше его - то мы можем прыгнуть.
            # А если ниже его, тоесть персонаж с ним столкнулся в полете, то мы не можем с него прыгнуть.
            if self.rect.bottom <= i.rect.bottom:
                self.speed_y = -10
                # Если мы уже смогли хоть раз прыгнуть, то дальше проверять не надо, просто прыгаем
                break

    def _animation(self):
        """Функция анимации персонажа. В данный момент только для ходьбы, но будет переделанна
         для всех типов анимации"""

        # Находим абсолютную позицию игрока на экране (учитывая сдвиг уровня)
        pos = self.rect.x + self.ground.shift_x
        # Если направление вправо, то берем анимацию из списка направо, влево соответственно
        if self.direction == 'R':
            # Берем позицию и делим на какое то число (сейчас это 24) это значит что каждые 24 пикселя меняется картинка
            # Функция % вычисляет остаток от деления. Остаток от деления у нап целочисленный,
            # от 0 до длины списка анимации -1. И именно это число мы используем что бы найти нужную картинку в списке
            frame = (pos // 24) % len(self.animation_frames_r)
            # Тут мы указываем что картинка должна стать той, которая идет по списку, в масиве картинок,
            # равная тому числу который мы нашли в прошлом шаге
            self.image = self.animation_frames_r[frame]
        else:
            # Аналогично для левой стороны
            frame = (pos // 24) % len(self.animation_frames_r)
            self.image = self.animation_frames_l[frame]

    def move_up(self):
        """Функция передвижения вверх. Если стоит возле лестницу, то лезет вверх. Если нет лестницы, то прыгает"""
        collisions_with_ladder = pygame.sprite.spritecollide(self, self.ground.groups['ground'], False)
        for hit in collisions_with_ladder:
            if isinstance(hit, Ladder):
                self.climbing = True
                self.speed_y = -2
                return

        self.jump()

    def _collision_with_y(self):
        """Базовая функция проверки столкновения игрока с предметами на экране"""

        # Получаем список всех елементов, из списка земли данного уровня, с которыми столкнулся персонаж
        collisions_with_y = pygame.sprite.spritecollide(self, self.ground.groups['ground'], False)

        # И теперь по каждому элементу проходимся, и смотрим что это за элемент и как на это реагировать
        for hit in collisions_with_y:

            # Если столкновение с Классом лестницы
            if isinstance(hit, Ladder):
                # Если дно персонажа добралось до немного ниже чем вершина лестницы,
                # то персонажа становится на вершину лестницы, и теряет скорость по координате у
                if self.rect.bottom <= hit.rect.top+20:
                    self.rect.bottom = hit.rect.top
                    self.speed_y = 0
                    # Если встали на вершину лестницы, то заканчиваем со всеми остальными провеками - они не нужны
                    break
                # А вот если персонаж на лестнице, но его дно не достигло нужной точки,
                # то продолжаем проверять другие столкновения
                continue

            # Если дно персонажа ниже чем дно земли с которым он столкнулся - то переходим сразу к след проверке
            if self.rect.bottom >= hit.rect.bottom:
                continue

            # Если дно персонажа было выше или равно верхней части земли,
            # то персонаж теряет всю скорость и становится на землю
            if self.rect.bottom >= hit.rect.top:
                self.rect.bottom = hit.rect.top
                self.speed_y = 0

            # Если земля движущаяся то игрой получает скорость по Х (возможно у нас не будет движущейся земли...)
            if isinstance(hit, Hover_ground):
                self.rect.x += hit.speed[0]

    def move_right(self):
        """Функция передвижения вправо"""
        self.speed_x = 10
        self.direction = 'R'

    def move_left(self):
        """Функция передвижения влево"""
        self.speed_x = -10
        self.direction = 'L'

    def fall(self):
        """Функция падения, вызывается когда пользователь нажимает Вниз.
            Если он на чем то стоит, то перемещает пользователя на 40 пикселей вниз, и он начинает падать"""

        if self._check_if_standing():
            self.rect.bottom += 40

    def stop(self):
        """Останавливает любое пережвижение по оси Х. Вызывается когда пользователь отпускает кнопку движения"""
        self.speed_x = 0
        if self.direction == 'R':
            self.image = self.standing_ani[0]
        else:
            self.image = self.standing_ani[1]

    def stop_y(self):
        """Если игрок отжимает кнопку ползти вверх, то он перестает лезть вверх"""
        if self.climbing:
            self.speed_y = 0
            self.climbing = False

    def update(self):
        """Эта функция обьединяет вышеперечисленные функции и обновляет положение персонажа на экране"""

        # Координату х меняем на скорость икса
        self.rect.x += self.speed_x
        # Отрисовываем анимацию
        if self.speed_x !=0:
            self._animation()

        # Если мы не лезем по лестнице - то учитываем гравитацию. Если лезем - то игнорируем ее
        if not self.climbing:
            self.gravity()
        # Меняем положение координаты у
        self.rect.y += self.speed_y
        # Проверяем с чем мы там столкнулись
        self._collision_with_y()


class Enemy(Character):
    def __init__(self, ground, sprite_list, image):
        """Функция инициализации которая назначает базовые атрибуты врага"""

        # Инициализируем родительскую функцию, что бы получить все плюшки
        super().__init__(image, sprite_list)
        # Тут стоит указать что ground это список элементов состоящий из одного элемента - ссылки на уровень
        # на котором мы находимся. Сделанно так потому что редактору так удобнее.
        # В версии без редактора передавать будем сам уровень
        self.ground = ground[0]

        # _in_boundaries - показывает находится ли враг находится в своей зоне патрулирования.
        # boundary - это те две координаты между которыми враг ходит.
        # revive_counter - счетчик респавна. Когда противник умирает,
        # он становится равен какому то значению, и потом каждый цикл отнимается
        self._in_boundaries = 1
        self.boundary = None
        self.revive_counter = 0

    def on_click(self):
        """РЕДАКТОР. Перезапись метода Animated_sprite. Задает границы патрулирования, и схороняет базовые координаты"""
        self.get_boundaries(int(input('Введите границы патрулирования = ')))
        super().on_click()

    def revive(self):
        """Функция респауна персонажа. Добавляет к ревайв каунтеру один,
         и сравнивает его с временем нужным для возрождения. Если равно - возвращает врага на уровень,
          на его старое место, дает ему полное ХП и ресетит ревайв каунтер"""

        self.revive_counter += 1
        if self.revive_counter == self.revive_time:
            self.ground.dead_enemy_list.remove(self)
            self.ground.groups['enemies'].add(self)
            self.reload()
            self.HP = self.start_HP
            self.revive_counter = 0

    def dead_or_alive(self):
        """Проверяет, помер ли враг или нет. Если помер - убирает его из всех листов уровня,
         и добавляет его в лист мертвых врагов, там где они ожидают оживления. """
        if self.HP <= 0:
            self.kill()
            try:
                self.rect.x =  self.initial_x
                self.ground.dead_enemy_list.append(self)
            except:
                del self

    def set_possition(self, x=0, y=0):
        """Вызхывает родительскую функцию задания координат,
         и дополнительно ставит дефолтные границы патрулирования, если из нет"""

        Character.set_possition(self, x, y)
        if not self.boundary:
            self.get_boundaries(200)

    def get_boundaries(self, boundary):
        """Принимает начальную точку Х как левую границу,
           а растояние в пикселях полученной функцией - как правую границу.
           Запоманиет нужное растояние патрулирования"""

        self.boundary_1 = boundary
        self.boundary = [self.rect.x, self.rect.x + self.boundary_1]

    def _check_if_will_fall(self):
        """Проверяет упадет ли враг, если пойдет вперед.
           Данная функция должна быть пересмотренна после определения логики действия врагов."""

        # Первый блок if  - это проверка стороны в которую идет враг. Логика принятия решений одинаковая для сторон
        if self.speed_x > 0 and self.speed_y == 0:

            # Перемещаем персонажа на 10 пикселей по х, и на 40 пикселей вниз.
            self.rect.right += 10
            self.rect.bottom += 40

            # Если мы не зарегестрировали столкновения с каким либо обьектом - то разворачиваемся
            if not pygame.sprite.spritecollide(self, self.ground.groups['ground'], False):
                self.speed_x *= -1

            # И потом возвращаемся на место.
            self.rect.right -= 10
            self.rect.bottom -= 40

        elif self.speed_x < 0 and self.speed_y == 0:
            self.rect.left -= 10
            self.rect.bottom += 40
            if not pygame.sprite.spritecollide(self, self.ground.groups['ground'], False):
                self.speed_x *= -1
            self.rect.left += 10
            self.rect.bottom -= 40

    def _see_enemy(self):
        """Проверяет, видит ли враг героя или нет. Нуждается в серьезной переделке"""

        # Перемещает врага на размер его зрения
        self.rect.x += self.vision

        if pygame.sprite.collide_rect(self, self.ground.player) and self.cool_down == 0:
            # Если мы столкнулись с героем то переходим в режим атаки, и ставим счетчик времени it_got_away на 60
            self.attack_mode = 1
            self.it_got_away = 60
        elif self.attack_mode == 1:
            # Если противник не столкнулся с героем, но уже находится в боевом режиме,
            # он будет оставаться в боевом режиме пока счетчик it_got_away не достигнет нуля,
            # после чего вернется к патрулированию
            self.it_got_away -= 1
            if not self.it_got_away:
                self.attack_mode = 0

        # Точно так же только для обратной стороны
        self.rect.x -= self.vision*2
        if pygame.sprite.collide_rect(self, self.ground.player) and self.cool_down == 0:
            self.attack_mode = 1
            self.it_got_away = 60
        elif self.attack_mode == 1:
            self.it_got_away -= 1
            if not self.it_got_away:
                self.attack_mode = 0
        self.rect.x += self.vision

    def _attack_if_touched(self):
        """Функция которая  проверяет - стукнулся ли персонаж в врага, и если да, то наносит ему урон"""
        # Если стукнулись...
        if pygame.sprite.collide_rect(self, self.ground.player):
            # Если счетчик времени неуязвимости ноль, то только тогда наносим урон
            if not self.ground.player.invul_time:
                # ставим счетчик кулл дауна на нужное значение
                self.cool_down = 25
                # Переходим в мирній режим
                self.attack_mode = 0
                # Отнимаем здоровье, проверяем - помер или нет, и запускаем функцию receive_mellie_hit,
                # что бы включить счетчик неуязвимости и отбросить персонажа
                self.ground.player.HP -= self.damage
                self.ground.player.dead_or_alive()
                self.ground.player.receive_mellie_hit()

    def _cool_downs(self):
        """Функция которая все счетчики персонажа уменьшает на один"""

        if self.invul_time != 0:
            self.invul_time -= 1
        if self.cool_down != 0:
            self.cool_down -= 1

    def _passing(self):
        """Функция патрулирования"""

        # Находим в какую сторону враг должен идти
        if self.speed_x < 0:
            self.direction = 'L'
        else:
            self.direction = 'R'

        # Текущая позиция врага с учетом смещения мира
        cur_pos = self.rect.x - self.ground.shift_x

        if self._in_boundaries:
            # Если мы в границах патрулируемой зоны, то проверяем, а не вышли ли мы за них

            if (cur_pos >= self.boundary[0] and cur_pos >= self.boundary[1]) or (
                    cur_pos <= self.boundary[0] and cur_pos <= self.boundary[1]):

                # Есди персонаж вышел за границы - то ставим тумблер в позицию 0
                self._in_boundaries = 0

            elif cur_pos <= self.boundary[0] or cur_pos >= self.boundary[1]:
                # Если мы немного вышли из за зоны, то разворачиваемся
                self.speed_x *= -1
                self._in_boundaries = 1
        else:
            # Тут мы заставляем его идти к границе, если он за нее вышел
            if cur_pos <= self.boundary[0]+10 and self.speed_x < 0:
                self.speed_x *= -1
            elif cur_pos >= self.boundary[1]-10 and self.speed_x > 0:
                self.speed_x *= -1

    def update(self):
        """Перезапись базавой функции обновления положения персонажа в пространстве"""

        # Проверяем, видит ли он противника или нет
        self._see_enemy()

        # Проверяем упадет он или нет
        self._check_if_will_fall()

        if not self.attack_mode:
            # Если врага мы не видем, то мы обновляемся как обычно, но при этом он еще занимается патрулированием,
            # и наносит урон если персонаж сам к нему прикоснулся
            super().update()

            self._attack_if_touched()

            self._passing()

        if self.attack_mode:
            # Если же враг в боевом режиме, то он атакует противника, и при этом обновляется как обычно

            self._attack()
            self._attack_if_touched()

            super().update()

        # Тут у нас все каунтеру нужніе уменьшаются на 1
        self._cool_downs()


class Bandit(Enemy):
    """Враг типа бандит. Имеет свои статы, свою картинку, и свой тип атаки"""

    def __init__(self, ground):
        """Функция инициализации которая вызывает родительскую функцию, и устанавливает нужные значения в поля"""

        # Спрайт лист с которого получаем картинки для анимации
        sprite_list = [(0, 108, 30, 50),
                       (37, 108, 30, 50),
                       (70, 108, 30, 50),
                       (102, 108, 30, 50)
                       ]
        # Родительский метод в который мы передаем все параметры для инициализации
        super().__init__(ground, sprite_list, image='.//characters//bandit.png')
        # Устанавливаем параметры
        self.speed_x = 5
        self.HP, self.start_HP = 25, 25
        self.damage = 5
        self.attack_mode = 0
        self.cool_down = 0
        self.vision = 200
        self.revive_time = 500

    def _attack(self):
        """Функция атаки. В данном случае бандит просто идет на сближение с противником, и наносит ему урон касанием"""

        if self.ground.player.rect.x > self.rect.x:
            if self.speed_x < 0:
                self.speed_x *= -1
            self.rect.x += self.speed_x
            self.direction = 'R'
        else:
            if self.speed_x > 0:
                self.speed_x *= -1
            self.rect.x += self.speed_x
            self.direction = 'L'


class Witch(Enemy):
    """Враг типа Ведьма. Имеет свои статы, свою картинку, и свой тип атаки"""

    def __init__(self, ground):
        y = 214
        x = 140
        sprite_list = [(x * 0, y * 0, x, y),
                       (x * 1, y * 1, x, y),
                       (x * 2, y * 1, x, y),
                       (x * 3, y * 1, x, y),
                       (x * 4, y * 1, x, y),
                       (x * 5, y * 1, x, y),
                       (x * 6, y * 1, x, y),
                       (x * 7, y * 1, x, y),
                       (x * 8, y * 1, x, y),
                       (x * 9, y * 1, x, y),
                       (x * 10, y * 1, x, y),
                       (x * 11, y * 1, x, y)
                       ]
        super().__init__(ground, sprite_list, image='.//characters//DC_si1.png')
        self.speed_x = 5
        self.HP, self.start_HP = 15, 15
        self.damage = 15
        self.attack_mode = 0
        self.cool_down = 0
        self.vision = 300
        self.revive_time = 500

    def _attack(self):
        """Функция атаки ведьмы. Смотрит в какой стороне враг, и кидает туда фаерболл"""
        if self.ground.player.rect.x > self.rect.x:
            self.direction = 'R'
        else:
            self.direction = 'L'

        self.ground.projectile_list.add(Enemy_Fireball(self))
        self.cool_down = 20
        self.attack_mode = 0


class Hero(Character):
    """Класс расписывающий все возможности героя"""

    def __init__(self, image, sprite_list):
        # Иницилизируем родительский класс
        Character.__init__(self, image, sprite_list)
        # Устанавливаем начальное и максимальное значение ХП, патроны
        self.HP, self.bullets_num, self.max_HP = (50, 6, 100)
        self.ground = None
        self.spell_cd, self.reload_time = [0 for i in range(2)]
        # Загружаем картинки для панели персонажа, здоровья и т.д.
        self.image_health = pygame.image.load(os.path.join('.//HUD//health.png')).convert()
        self.bullets = pygame.image.load(os.path.join('.//HUD//cilinder.jpg')).convert()
        self.image_hud = pygame.image.load(os.path.join('.//HUD//menu.jpg')).convert()
        self.empty_bar = pygame.image.load(os.path.join('.//HUD//SleekBars_empty.png')).convert()

        # Получаем цель, убираем фон, и убираем мышку
        self.target = pygame.image.load(os.path.join('.//HUD//target.png')).convert()
        self.target.set_colorkey(BLACK)
        pygame.mouse.set_visible(False)

        # Получаем отображение количества зелий, создаем пустой список квестовых предметов
        self._get_potions()
        self.quest_items = []

        # Получаем анимацию барабана револьвера
        self.bullets_animation = self._get_bullets_animations()

    def reload(self):
        """Функция перезарядки револьвера"""
        if self.bullets_num !=6 and self.reload_time ==0:
            # Если барабан не полный, то заряжаем один патрон, ставим кул даун всех действий 10, и воспроизводим звук
            self.bullets_num += 1
            self.reload_time = 10
            file = self.ground.m_player('.//sound//Sound_exf//reload.wav')
            self.ground.m_player.play(file)

    def world_shift(self):
        """Функция сдвига картинки мира и всех его елементов при достижении игроком определенных точек.
            Делается для того что бы создавалось ощющение что игрок идет по уровню"""

        if self.rect.right >= (SCREEN_WIDTH * 4 // 5):
            diff = self.rect.right - (SCREEN_WIDTH * 4 // 5)
            self.ground.shift_level(-diff, 0)
            self.rect.right = (SCREEN_WIDTH * 4 // 5)
        elif self.rect.left <= (SCREEN_WIDTH // 5):
            self.ground.shift_level((SCREEN_WIDTH // 5) - self.rect.left, 0)
            self.rect.left = (SCREEN_WIDTH // 5)

        if self.rect.bottom >= (SCREEN_HEIGHT - 220):
            diff = self.rect.bottom - (SCREEN_HEIGHT - 220)
            self.ground.shift_level(0, -diff)
            self.rect.bottom = (SCREEN_HEIGHT - 220)
        elif self.rect.top <= (SCREEN_WIDTH // 5):
            self.ground.shift_level(0, (SCREEN_WIDTH // 5) - self.rect.top)
            self.rect.top = (SCREEN_WIDTH // 5)

    def cast(self, spell):
        """Функция каста заклинания. Если в пистолете есть патроны, и кулл дауна нету,
            то онимает патрон, устанавливает куллдаун и создает заклинание, после чего проигрывает звук"""

        if self.bullets_num > 0 and self.spell_cd == 0:
            self.bullets_num -= 1
            self.spell_cd = 10
            self.ground.groups['projectile'].add(spell(self))
            file = self.ground.m_player(spell.music_file)
            self.ground.m_player.play(file)

    def _get_potions(self):
        """Функция получает картинки с счетчиком поушенов"""
        sprite_list = [(0, 0, 90, 40),
                        (0, 50, 90, 40),
                        (0, 50*2, 90, 40),
                        (0, 50*3, 90, 40),
                        (0, 50*4, 90, 40),
                        (0, 50*5, 90, 40),
                        (0, 50*6, 90, 40),
                        (0, 50*7, 90, 40),
                        (0, 50*8, 90, 40),
                        (0, 50*9, 90, 40),
        ]
        health_image = pygame.image.load(os.path.join('.//HUD//whiskey(0,50y,40,90).png')).convert()
        self.image_health_potion = self._get_animation(health_image, sprite_list)[0]
        self.health_potions = 0

    def _get_bullets_animations(self):
        """Получает анимацию цилиндра с пулями. Обычное получение анимациий как в базовом классе"""
        return_list = []
        sprite_image = pygame.image.load(os.path.join('.//HUD//cilinder.jpg')).convert()
        y = 150
        x = 0
        sprite_list = [(x, y*0, 140, 150),
                       (x, y*1, 140, 150),
                       (x, y*2, 140, 150),
                       (x, y*3, 140, 150),
                       (x, y*4, 140, 150),
                       (x, y*5, 140, 150),
                       (x, y*6, 140, 150),
                       (x, y*7, 140, 150),
                       (x, y*8, 140, 150),
                       (x, y*9, 140, 150),
                       (x, y*10, 140, 150),
                       (x, y * 11, 140, 150)
                       ]
        for sprite in sprite_list:
            return_list.append(self._get_image(sprite[0], sprite[1], sprite[2], sprite[3], sprite_image))
        return return_list

    def _cool_downs(self):
        """Функция уменьшение кулл даунов если они есть"""
        if self.spell_cd != 0:
            self.spell_cd -= 1
        if self.invul_time != 0:
            self.invul_time -= 1
        if self.reload_time !=0:
            self.reload_time-=1

    def use(self, clock, screen):
        """Функция использования НПС (в будущем и другие вещи). Если столкнулся с НПС,
            то передает ему инфу про чеса и экран игры, что бы тот мог запустить диалог"""
        hits = pygame.sprite.spritecollide(self, self.ground.groups['use'], False)
        for hit in hits:
            hit.use(clock, screen)

    def pick_up(self):
        """Функция подбора всяких обьектов. Если стулкнулся, и если у тебя таких обьектов не больше 9,
            то добавляет в скиски. После этого убирает обьект с экранна"""
        hits = pygame.sprite.spritecollide(self, self.ground.groups['items'], False)

        for hit in hits:
            if isinstance(hit, Health_potion) and self.health_potions < 9:
                self.health_potions += 1
                hit.kill()
                del hit
            elif isinstance(hit, Quest_object):
                self.quest_items.append(hit)
                hit.kill()
                del hit

    def update(self):
        """Обновление положения персонажа."""
        Character.update(self)
        self.pick_up()
        self._cool_downs()

    def drink_potion(self):
        """Если есть поушены и если здоровье не на максах - пьем зелье и отнимаем зелье из инвентаря"""
        if self.health_potions and self.HP < self.max_HP:
            self.health_potions -= 1
            self.HP += int(self.max_HP*0.25)

    def hud_draw(self, screen):
        """Функция отрисовки интерфейса персонажа. Просто рисует нужные картинки в нужных местах"""

        # Рисуем на экране, внизу, панель самого интерфейса
        screen.blit(self.image_hud, (0, SCREEN_HEIGHT-150), pygame.Rect(0, 0, SCREEN_WIDTH, 150))

        # Вычисляем процент оставшихся жизней
        percent = self.HP/100
        # Вначале рисуем пустую ячейку со сдоровьем
        screen.blit(self.empty_bar, (35, SCREEN_HEIGHT-150))
        # Потом рисуем полную ячейку со сдоровьем, но по длине отрисовываем только нужный нам процент
        screen.blit(self.image_health, (35, SCREEN_HEIGHT-150), pygame.Rect(0, 0, 32, 128*percent))
        # Тут рисуем барабан, в зависимости от оставшихся пуль.
        screen.blit(self.bullets_animation[6-self.bullets_num], (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 150))

        # Если у нас есть зелья - рисуем их количество
        if self.health_potions >= 0:
            screen.blit(self.image_health_potion[self.health_potions], (400, SCREEN_HEIGHT - 100))

        # Рисуем цельку, что бы поинтер мыши был прям в центре цельки
        pos = pygame.mouse.get_pos()
        offset = (pos[0] - 50, pos[1] - 49)
        screen.blit(self.target, offset)

    def receive_mellie_hit(self):
        """Функция которая отбрасывает назад на 20 пикселей, и добавляет 10 циклов неуязвимости"""
        self.invul_time = 10
        if self.direction == 'R':
            self.rect.x -= 20
        else:
            self.rect.x +=20


class NPC(Character, NewSceneTrigger):
    """Персонаж который выдает квест и диалог"""
    def __init__(self, settings):
        """Инициализация нпс с квестом"""
        sprite_list = [(0, 0, 133, 215)]
        # Функции которые парсят файл квеста и выбирают из него нужные слова и ответы.
        # Путь к фалу определяем в settings[1]
        not_taken, taken, completed = self._get_text_from_txt(settings[1])
        Character.__init__(self, self.image, sprite_list)
        # Даем ему ссылку на уровень на котором он находится, через settings[0
        self.ground = settings[0]
        # Квест не взят и не сделан. Поэтому устанавливаем каунтеры в 0
        self.quest_taken = 0
        self.quest_completed = 0
        # Создаем обраточик квестового диалога, и передаем ему все слова
        self.scene = Quest_dialog(self, not_taken, taken, completed)

    def check_if_complete(self):
        """Проверяем, выполнен ли квест или нет. Если задача убить - проверяет, жив ли персонаж или нет.
            Если задача что то найти, проверяет если ли у персонажа этот предмет"""

        if self.task == 'kill':
            if not self.object.alive():
                return True
            else:
                return False

        else:
            if self.object in self.ground.player.quest_items:
                self.ground.player.quest_items.remove(self.object)
                return True

            return False

    def init_quest(self):
        """Функция которая после того как Герой берет квест, создает обькт который должны убить\найти,
            и выставляет нужную позицию ему."""
        self.quest_taken = 1
        # Тут мы из строчки, которую мы пропарсили вытаскиваем код и используем его
        exec('self.object = %s' % self.target_object)
        self.object.set_possition(self.object_coordinates[0], self.object_coordinates[1])
        if self.task == 'kill':
            self.ground.groups['enemies'].add(self.object)
        else:
            self.ground.groups['items'].add(self.object)

    def reward(self):
        """Функция которая дает пользователю зелье здоровья, или кидает на землю зелье если у пользователя больше 9"""
        if self.reward_item == 'Health_potion':
            if self.ground.player.health_potions < 9:
                self.ground.player.health_potions += 1
            else:
                self.ground.groups['items'].add(Health_potion(self.ground, self.rect.x-20, self.rect.y))
            self.quest_completed = 1

    def _get_text_from_txt(self, file):
        """Основная функция парсера. Получает текст из файла, и потом разбирает его на нужные элементы"""
        with open(file, 'r') as file:
            file_read = file.read()

        file = file_read.split('***')
        file_header = file[0]
        self._get_header_info(file_header)

        file_not_taken = file[1:3]
        file_taken = file[3:5]
        file_complete = file[5:]

        not_taken = self._get_object_from_list(file_not_taken)
        taken = self._get_object_from_list(file_taken)
        comleated = self._get_object_from_list(file_complete)

        for el in not_taken:
            for element in el:
                if not element:
                    el.remove(element)

        for el in taken:
            for element in el:
                if not element:
                    el.remove(element)

        for el in comleated:
            for element in el:
                if not element:
                    el.remove(element)

        return not_taken, taken, comleated

    def _get_header_info(self, big_string):
        text = big_string.split('\n')
        self.image = text[0].split('Image = ')[1].lstrip()
        self.task = text[1].split('Task = ')[1].lstrip()
        self.target_object = text[2].split('Object = ')[1].lstrip()
        self.object_coordinates = (int(text[3].split('Object X = ')[1].lstrip()),
                                   int(text[4].split('Object y = ')[1].lstrip()))
        self.reward_item = text[5].split('Reward = ')[1].lstrip()
        self.name = text[6].split('Name = ')[1].lstrip()

    def _get_object_from_list(self, list):
        text = list[0].split('\n')
        text = [i.lstrip() for i in text]
        answers = list[1].split('\n')
        return_answers = []
        for i in answers:
            answers_list = i.split('@')
            temp = []
            for answer in answers_list:
                answer_from_func = self._get_class_from_answer(answer)
                if answer_from_func:
                    temp.append(self._get_class_from_answer(answer))
            return_answers.append(temp)

        return [text, return_answers]

    def _get_class_from_answer(self, answer):
        answer_line = answer.split('#')
        answer_line = [i.lstrip() for i in answer_line]
        if 'Confirm' in answer_line[0]:
            return Confirm(answer_line[1], int(answer_line[2]))
        elif 'Answer' in answer_line[0]:
            return Answer(answer_line[1], int(answer_line[2]))
        elif 'Exit' in answer_line[0]:
            return Exit(answer_line[1])
        elif 'Complete_quest' in answer_line[0]:
            return Complete_quest(answer_line[1], int(answer_line[2]), int(answer_line[3]))
        elif 'Success' in answer_line[0]:
            return Success(answer_line[1])