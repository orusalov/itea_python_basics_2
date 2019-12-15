'''class Checker:

    POSSIBLE_MOVES = {'l':(1, -1), 'r':(1, 1)}

    def __init__(self, position, color, table):

        self.table = table
        self.table_size = (len(table), len(table[0]))
        self.is_king = False
        if self.is_valid_position(position):
            self.position = position
        else:
            raise Exception

        self.color = color

    def get_position_of_relative_change(self, supplement):
        return list(map(lambda n, m: n + m, self.position, supplement))

    def is_valid_position(self, position):

        if (position[0] < 0 or
            position[1] < 0 or
            position[0] >= len(self.table) or
            position[1] >= len(self.table[0]):
            return False

        return position

    def move_entity(self, move):

        move_tupple = self.POSSIBLE_MOVES[move]
        new_position = self.get_position_of_relative_change(move_tupple)
        new_position = self.is_valid_position(new_position)
        if not new_position:
            return 'Wrong move!'

        self.position = new_position

        return self.position

    def _get_backward_positions(self):

        relative_backward_positions = [(-1, -1), (-1, 1)]

        position_list = [self.get_position_of_relative_change(change) for change in relative_backward_positions]

        return_positions = [self.is_valid_position(pos) for pos in position_list]

        return return_positions

        
    def get_relative_backward_position(self, other):

        # проверка того, что позиция другого игрока реальна
        if not self.is_valid_position(other.position):
            return []

        back_positions = self._get_backward_positions()

        # надо отнять позиции, чтобы определить направление нападающего
        get_attacker_substruct_position = self.get_position_of_relative_change((-other.position[0], -other.position[1]))

        # if it's simple checker then it should be in front and less then 1 cell
        # or if relative position has 0, than definetely it's not diagonal, but could raize ZeroDivisionError
        if (not other.is_king and
            -1 not in get_attacker_substruct_position or
            0 in get_attacker_substruct_position):
            return []
        
        # если нападающий по диагонали справа, то координаты его относительной позиции
        # соотносятся как 1, если слева - то -1
        get_attacker_direction = get_attacker_substruct_position[0] // get_attacker_substruct_position[1]

        # if back_position is valid then return it, otherwise return empty position
        if get_attacker_direction == 1 and back_positions[0]:
            return back_positions[0]
        elif get_attacker_direction == -1 and back_positions[1]:
            return back_positions[1]
        else:
            return []
    
    def is_attack_possible(self, other, table):

        if self.color == other.color:
            return []
            
        possible_move = other.get_relative_backward_position(self)

        if possible_move not in table.get_checker_positions():
            return possible_move
        else:
            return []

    def attack(self, other, table):

        possible_move = self.is_attack_possible(other, table)

        if possible_move:
            self.position = possible_move
            table.remove_checker(other)

    def is_move_possible(self, table):

        for move_tuple in self.POSSIBLE_MOVES.values():

            possible_move = self.get_position_of_relative_change(move_tuple)
            possible_move = self.is_valid_position(possible_move)

            is_possible = (possible_move and
                           possible_move not in table.get_checker_positions())

            if is_possible:
                return True
        
        return False'''

from random import choice

class Checker:

    def __init__(self, position, color):

        self.position = position
        self.color = color
        
    def __str__(self):

        return self.color




class Table:

    LETTERS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    '''def __init__(self):
        

        self.SIZE_X = 8
        self.SIZE_Y = 8

        self.table = [[' ' for _ in range(self.SIZE_X)] for _ in range(self.SIZE_Y)]
        self.user = [Checker([0, 0], 'x')]
        self.bot = [Checker([2, 2], 'o')]

    def get_checker_positions(self):
        return [ch.position for ch in self.user + self.bot]

    def remove_checker(self, checker):
        self.user.remove(checker)
        self.bot.remove(checker)'''

    def __init__(self, size):

        if size > len(self.LETTERS):
            raise Exception
        self.SIZE = size
        self.USER_COLOR = 'o'
        self.BOT_COLOR = 'x'
        self.EMPTY_COLOR = ' '
        self.current_turn = choice([self.USER_COLOR, self.BOT_COLOR])
        self.letters = self.LETTERS[:size]
        self.armies = {self.BOT_COLOR: self.generate_army(self.SIZE, self.BOT_COLOR), self.USER_COLOR: self.generate_army(self.SIZE, self.USER_COLOR)}
        self.get_start_cell = self._get_cell('checker', self.USER_COLOR)
        self.get_end_cell = self._get_cell('move to', self.EMPTY_COLOR)
        self.warning_message = ''
        
        
    def _get_cell(self, type_, expected_cell_color):

        def return_function():

            loop_message = ''
            while True:

                captured_position = input(f'please choose {type_} cell{loop_message}: ').upper().strip()

                letter = captured_position[0]
                number = captured_position[1:]

                if (letter not in self.letters or
                    not number.isdigit()):
                    print(f'Not correct {type_} position. Try again.')
                    loop_message = '(letter and number. e.g A1 or D6)'
                    continue

                return_tuple = (int(number) - 1, self.letters.index(letter))

                if not self.is_expected_cell_color(return_tuple, expected_cell_color):
                    if expected_cell_color == self.EMPTY_COLOR:
                        print('Expected empty cell')
                    else:
                        print('You should take your checker')

                    continue
                    
                return return_tuple

        return return_function

    def generate_army(self, size, color):

        n = int((size - 2) / 2)
        army = [Checker([i, j], color) for i in range(n) for j in range(i % 2, size, 2)]

        return army

    def reverse_deck(self):
        for row in self.deck:
            row.reverse()
            
        self.deck.reverse()

    def generate_deck(self):

        self.deck = [[self.EMPTY_COLOR for _ in range(self.SIZE)] for _ in range(self.SIZE)]

        for armie in [self.armies[self.USER_COLOR], self.armies[self.BOT_COLOR]]:
            for checker in armie:

                x = checker.position[0]
                y = checker.position[1]
                self.deck[x][y] = checker

            self.reverse_deck()

        horizon = '   '+' '.join(self.letters)

        print(f'{horizon}')
        for row in reversed(list(enumerate(self.deck))):
            print(f'{row[0] + 1} |{"|".join(list([str(symb) for symb in row[1]]))}| {row[0] + 1}')

        print(f'{horizon}')

        print(self.warning_message)
        self.warning_message = ''

    def move_checker(self, st_pos, end_pos):
        self.deck[st_pos[0]][st_pos[1]].position = end_pos
        
    def is_valid_position(self, position):

        if (position[0] < 0 or
            position[1] < 0 or
            position[0] >= self.SIZE or
            position[1] >= self.SIZE):
            return False

        return position

    def move_validator(self, st_pos, end_pos):

        POSSIBLE_MOVES = [(1, -1), (1, 1)]
        end_pos = self.is_valid_position(end_pos)

        if not end_pos:

            self.warning_message = 'Wrong move!'
            return False

        relative_change = tuple(map(lambda n, m: n - m, end_pos, st_pos))

        if relative_change not in POSSIBLE_MOVES:
            self.warning_message = 'Wrong move!'
            return False

        return (st_pos, end_pos)

    def is_expected_cell_color(self, position, expected_cell_color):

        obj = self.deck[position[0]][position[1]]

        if isinstance(obj, Checker) and obj.color == expected_cell_color:
            return True
        elif obj == expected_cell_color:
            return True
        else:
            return False
        


table = Table(8)

while True:

    table.generate_deck()

    position_change = table.move_validator(table.get_start_cell(), table.get_end_cell())

    if not position_change:
        continue

    table.move_checker(*position_change)

        
