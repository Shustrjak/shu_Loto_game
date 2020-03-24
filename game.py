#  Copyright (c) 2020.
#  Author: Rudenko Alexander
#  Study package for search pair text-link
import random
import sys

"""Лото
Правила игры.
Игра состоит из специальных карточек на которых отмечены числа и бочонков
с цифрами

Всего 90 бочонков с цифрами от 1 до 90 (В жизни они обычно достаются из мешка
чтобы можно было вытянуть случайно)

Каждая карточка содержит 3 строки по 9 клеток. В каждой строке по 5 случайных
цифр, расположенных по возрастанию. Все цифры в карточке уникальны.
Так выглядит пример карточки:

--------------------------
    9 43 62          74 90
 2    27    75 78    82
   41 56 63     76      86
--------------------------

В игре 2 игрока: пользователь и компьютер (*так же может быть 2 пользователя
или 2 компьютера).
Каждому в начале выдается случайная карточка.

Каждый ход выбирается один случайный бочонок и выводится на экран.
Также выводятся карточка игрока и карточка компьютера.

Пользователю предлагается зачеркнуть цифру на карточке или продолжить.
Если игрок выбрал "зачеркнуть":
__Если цифра есть на карточке - она зачеркивается и игра продолжается.
__Если цифры на карточке нет - игрок проигрывает и игра завершается.
Если игрок выбрал "продолжить":
__Если цифра есть на карточке - игрок проигрывает и игра завершается.
__Если цифры на карточке нет - игра продолжается.

Компьютер всегда правильно зачеркивает свои цифры если они есть и продолжает
если их нет.

Побеждает тот, кто первый закроет все числа на своей карточке.

Пример одного хода (как может выглядеть интерфейс игры):
-- (знаком минус) отмечены уже зачеркнутые цифры

Новый бочонок: 70 (осталось 76)
------ Ваша карточка -----
 6  7          49    57 58
   14 26     -    78    85
23 33    38    48    71
--------------------------
-- Карточка компьютера ---
 7 87     - 14    11
      16 49    55 88    77
   15 20     -       76  -
--------------------------
Зачеркнуть цифру? (y/n)

Подсказка: для работы с псевдослучайными числами удобно использовать
модуль random: http://docs.python.org/3/library/random.html

Подсказка: для написания программы удобно использовать ООП, примеры возможных
классов: Игрок, Бочонок, Мешок, Карточка, ...
Так же можно придумать свою структуру классов либо воспользоваться процедурным
программированием
"""


class Cask:
    # Достаем бочонки по 1 штуке
    def take_out_casks(self):
        lst = [x for x in range(1, self.quantity + 1)]  # последовательный список бочонков
        random.shuffle(lst)  # "перемешаем мешок с бочонками"
        for numeric, number_cask in enumerate(lst):
            print('{:*^30}'.format('*'))
            print('Новый бочонок: {} (осталось {})'.format(
                number_cask,
                self.quantity - (numeric + 1))
            )
            yield number_cask

    def __init__(self, quantity):
        self.quantity = quantity
        self.gen = self.take_out_casks()


class Game:
    # Создаем карточки по 3 ряда, в каждом по 5 чисел
    def __set_card(self):
        num = set()
        while len(num) < self.all_row * 5:
            num.add(random.randint(1, 90))
        cards = list(num)
        random.shuffle(cards)
        while len(cards) % self.all_row != 0:
            cards.append('None')
        self.all_row = int(len(cards) / self.all_row)
        cards = [cards[i: i + self.all_row] for i in range(
            0,
            len(cards), self.all_row)
                 ]
        for i in range(len(cards)):
            cards[i].sort()

        self.card_user = cards[:3]
        self.card_comp = cards[3:]
        self.card_user.sort()
        self.card_comp.sort()

    def __init__(self, quantity_card):
        row = 3
        self.all_row = row * quantity_card
        self.__set_card()

    def get_card_user(self, card_player):
        print('{:-^28}'.format(self.name))
        print('{0[0]:>2}\t{0[1]:>2}{0[2]:^5}{0[3]:^5}{0[4]:>4}'
              .format(card_player[0]))
        print('{0[0]:>2}\t{0[1]:>5}\t{0[2]:>5}{0[3]:>5}{0[4]:>5}'
              .format(card_player[1]))
        print('{0[0]:>2}\t{0[1]:>1}{0[2]:^5}{0[3]:^5}{0[4]:>4}'
              .format(card_player[2]))
        print('{:-^28}'.format('-'))

    def get_card_comp(self, card_player):
        print('{:-^28}'.format(self.name))
        print('{0[0]:>2}\t{0[1]:>2} {0[2]:^5} {0[3]:^5} {0[4]:>4}'
              .format(card_player[0]))
        print('{0[0]:>2}\t{0[1]:>5} {0[2]:<5} {0[3]:>5} {0[4]:>4}'
              .format(card_player[1]))
        print('{0[0]:>2}\t{0[1]:<2} {0[2]:^5} {0[3]:<5} {0[4]:>4}'
              .format(card_player[2]))
        print('{:-^28}'.format('-'))

    # Поиск номера на карточке и определение победителя
    def search(self, card_player, num_cask):
        for i, n in enumerate(card_player):
            if num_cask in n:
                card_player[i][n.index(num_cask)] = '--'
                self.score += 1
                if self.score == 15:
                    print('{} победила!'.format(self.name))
                    sys.exit(1)
                return True
        return False


class Player(Game):
    def __init__(self, name):
        self.name = name
        self.score = 0


def main():
    game = Game(2)
    cask = Cask(90)
    gamer_user = Player('Ваша карточка')
    gamer_comp = Player('Карточка компьютера')
    while True:
        num_cask = next(cask.gen)
        gamer_user.get_card_user(game.card_user)
        gamer_comp.get_card_comp(game.card_comp)
        input_user = input('Зачеркнуть цифру? |\"Да\"(y)|\"Нет\"(n)|: ')
        if input_user == 'y':
            if gamer_user.search(game.card_user, num_cask):
                print('Ok')
                continue
            else:
                print('Проигрыш')
                sys.exit(1)
        elif input_user == 'n':
            if gamer_comp.search(game.card_comp, num_cask):
                print('Ok')
                continue
            elif gamer_user.search(game.card_user, num_cask):
                print('Проигрыш')
                sys.exit(1)
        else:
            print('Вы ввели неправильную команду')
            print(input_user)
            sys.exit(1)


if __name__ == '__main__':
    main()
