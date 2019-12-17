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

    '''def __hash__(self):
        return hash(tuple(self.position))+hash(self.color)

    def __eq__(self, other):
        if isinstance(other, Checker) and self.position == other.position and self.color == other.color:
            return True
        else:
            return False'''




class Table:

    LETTERS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    def __init__(self, size):

        if size > len(self.LETTERS):
            raise Exception
        self.SIZE = size
        self.USER_COLOR = 'o'
        self.BOT_COLOR = 'x'
        self.EMPTY_COLOR = ' '
        self.POSSIBLE_MOVES = [(1, -1), (1, 1)]
        self.POSSIBLE_ATTACKS = [(2, -2), (2, 2)]
        self.current_turn = choice([self.USER_COLOR, self.BOT_COLOR])
        self.letters = self.LETTERS[:size]
        self.armies = {self.BOT_COLOR: self._generate_army(self.SIZE, self.BOT_COLOR), self.USER_COLOR: self._generate_army(self.SIZE, self.USER_COLOR)}
        self.get_start_cell = self._get_cell('checker', self.USER_COLOR)
        self.get_end_cell = self._get_cell('move to', self.EMPTY_COLOR)
        self.possible_checker_regular_moves = self._get_interested_positions_by_relative_change_and_color(self.POSSIBLE_MOVES, self.EMPTY_COLOR)
        self.possible_checker_attack_moves = self._get_interested_positions_by_relative_change_and_color(self.POSSIBLE_ATTACKS, self.EMPTY_COLOR)
        self.warning_message = ''
    

    def _generate_army(self, size, color):

        n = int((size - 2) / 2)
        army = [Checker([i, j], color) for i in range(n) for j in range(i % 2, size, 2)]

        return army   
        
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
                        print('Choose empty cell')
                    else:
                        print('You should take your checker')

                    continue
                    
                return return_tuple

        return return_function

    def _get_interested_positions_by_relative_change_and_color(self, interested_moves, interested_color):
    
        def return_func(checker):

            position = checker.position
            result_positions = []
            for relative_change in interested_moves:
                interested_position = tuple(map(lambda n, m: n + m, position, relative_change))

                if self.is_inside_table(interested_position) and self.is_expected_cell_color(interested_position, interested_color):
                    result_positions.append(interested_position)

            return result_positions

        return return_func

    def nearby_enemies(self, checker):
        return self._get_interested_positions_by_relative_change_and_color(self.POSSIBLE_MOVES, self.get_enemy_color())(checker)

    def get_enemy_color(self):

        if self.USER_COLOR == self.current_turn:
            return self.BOT_COLOR
        elif self.BOT_COLOR == self.current_turn:
            return self.USER_COLOR
        else:
            return False

    def captured_deck_object(self, position):
        return self.deck[position[0]][position[1]]

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
        

    def print_deck(self):

        horizon = '   '+' '.join(self.letters)
        
        print(f'{horizon}')
        for row in reversed(list(enumerate(self.deck))):
            print(f'{row[0] + 1} |{"|".join(list([str(symb) for symb in row[1]]))}| {row[0] + 1}')

        print(f'{horizon}')

        print(self.warning_message)
        self.warning_message = ''

    def move_checker(self, checker, end_pos):
        checker.position = end_pos

    def attack(self, checker, beaten_checker_and_move):

        if beaten_checker_and_move[0] in self.armies[self.USER_COLOR]:
            self.armies[self.USER_COLOR].remove(beaten_checker_and_move[0])
        elif beaten_checker_and_move[0] in self.armies[self.BOT_COLOR]:
            self.armies[self.BOT_COLOR].remove(beaten_checker_and_move[0])

        self.move_checker(checker, beaten_checker_and_move[1])
        
    def is_inside_table(self, position):

        if (position[0] < 0 or
            position[1] < 0 or
            position[0] >= self.SIZE or
            position[1] >= self.SIZE):
            return False

        return position

    def is_expected_cell_color(self, position, expected_cell_color):

        obj = self.deck[position[0]][position[1]]

        if isinstance(obj, Checker) and obj.color == expected_cell_color:
            return True
        elif obj == expected_cell_color:
            return True
        else:
            return False

    def possible_turn_moves(self, turn_color):

        result = {}
        for checker in self.armies[turn_color]:
            
            possible_ch_moves = self.possible_checker_regular_moves(checker)
            if possible_ch_moves:
                result[checker] = possible_ch_moves

        return result

    def possible_turn_attacks(self, turn_color):

        result = {}
        for checker in self.armies[turn_color]:
            
            possible_ch_atacks = self.possible_checker_attack(checker)
            if possible_ch_atacks:
                result[checker] = possible_ch_atacks

        return result

    def bot_turn(self):

        turn = self.move_checker

        checkers_and_attacks = self.possible_turn_attacks(self.BOT_COLOR)
        if checkers_and_attacks:
            checkers_and_moves = checkers_and_attacks
            turn = self.attack
        else:
            checkers_and_moves = self.possible_turn_moves(self.BOT_COLOR)
            
        bot_checker = choice(list(checkers_and_moves.keys()))
        bot_move = choice(checkers_and_moves[bot_checker])
        turn(bot_checker, bot_move)

    def possible_checker_attack(self, checker):

        near_enemies = self.nearby_enemies(checker)
        attack_moves = set(self.possible_checker_attack_moves(checker))
        return_moves = []
        for enemie_position in near_enemies:

            relative_attack_direction = list(map(lambda n, m: 2 * (n - m), enemie_position, checker.position))
            attack_position = set()
            attack_position.add(tuple(map(lambda n, m: n + m, checker.position, relative_attack_direction)))

            move = attack_moves & attack_position
            if move:
                return_move = (self.captured_deck_object(enemie_position), tuple(move)[0])
                return_moves.append(return_move)

        return return_moves

    def user_turn(self):
        
        while True:

            self.generate_deck()
            self.print_deck()

            turn = self.move_checker
            
            checkers_and_attacks = self.possible_turn_attacks(self.USER_COLOR)
            if checkers_and_attacks:
                possible_checkers_and_moves = checkers_and_attacks
                turn = self.attack
            else:
                possible_checkers_and_moves = self.possible_turn_moves(self.USER_COLOR)
                
            checker = self.captured_deck_object(self.get_start_cell())

            if checker not in possible_checkers_and_moves.keys():
                self.warning_message = 'This checker can''t make a move!'
                continue
            
            user_move = self.get_end_cell()

            print(possible_checkers_and_moves[checker])#######################
            print(user_move)##################################################
            if not turn == self.move_checker:
                print(turn == self.attack, user_move not in possible_checkers_and_moves[checker][0][1])##################################################
            if ((turn == self.move_checker and user_move not in possible_checkers_and_moves[checker]) or
                (turn == self.attack and user_move not in possible_checkers_and_moves[checker][0][1])):
                self.warning_message = 'Wrong move!'
                continue

            if turn == self.attack:
                user_move = possible_checkers_and_moves[checker][0][1]
                
            print(user_move)##################################################

            turn(checker, user_move)

            break


table = Table(8)

while True:
    try:
        if table.current_turn == table.USER_COLOR:
            table.user_turn()

            table.current_turn = table.get_enemy_color()
            
        table.generate_deck()
        table.reverse_deck()
        table.bot_turn()
        table.reverse_deck()
        
        table.current_turn = table.get_enemy_color()
        
    except KeyboardInterrupt:
        print('Goodbye!')
        break
