from random import choice
from time import sleep

class Checker:

    def __init__(self, position, color):

        self.position = position
        self.color = color
        
    def __str__(self):

        return self.color




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
        self.deck = [[self.EMPTY_COLOR for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.current_turn = choice([self.USER_COLOR, self.BOT_COLOR]) # 
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
        
        print(f'\n\n\n\n\n\n\n\n\n\n\n\n{horizon}')
        for row in reversed(list(enumerate(self.deck))):
            print(f'{row[0] + 1} |{"|".join(list([str(symb) for symb in row[1]]))}| {row[0] + 1}')

        print(f'{horizon}')

        print(self.warning_message)
        self.warning_message = ''

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
    
    def possible_checker_attack(self, checker):

        near_enemies = self.nearby_enemies(checker)
        attack_moves = set(self.possible_checker_attack_moves(checker))
        return_moves = {}
        for enemie_position in near_enemies:

            relative_attack_direction = list(map(lambda n, m: 2 * (n - m), enemie_position, checker.position))
            attack_position = set()
            attack_position.add(tuple(map(lambda n, m: n + m, checker.position, relative_attack_direction)))

            move = attack_moves & attack_position
            if move:
                return_moves[tuple(move)[0]] = self.captured_deck_object(enemie_position)

        return return_moves

    def move_checker(self, checker, end_pos):
        checker.position = end_pos
        return end_pos

    def attack(self, checker, beaten_checker_and_move):

        moved_position = self.move_checker(checker, list(beaten_checker_and_move.keys())[0])

        if beaten_checker_and_move[moved_position] in self.armies[self.USER_COLOR]:
            self.armies[self.USER_COLOR].remove(beaten_checker_and_move[moved_position])
        elif beaten_checker_and_move[moved_position] in self.armies[self.BOT_COLOR]:
            self.armies[self.BOT_COLOR].remove(beaten_checker_and_move[moved_position])
        
    def bot_turn(self):

        self.generate_deck()
        self.print_deck()
        self.reverse_deck()

        checkers_and_attacks = self.possible_turn_attacks(self.BOT_COLOR)
        checkers_and_moves = self.possible_turn_moves(self.BOT_COLOR)

        if checkers_and_attacks:

            bot_checker = choice(list(checkers_and_attacks.keys()))
            while bot_checker in checkers_and_attacks.keys():

                self.reverse_deck()
                self.generate_deck()
                self.print_deck()
                sleep(1)
                self.reverse_deck()

                bot_move = choice(list(checkers_and_attacks[bot_checker].keys()))
                enemy_checker = checkers_and_attacks[bot_checker][bot_move]

                bot_move = {bot_move: enemy_checker}

                self.attack(bot_checker, bot_move)

                checkers_and_attacks = self.possible_turn_attacks(self.BOT_COLOR)

                self.reverse_deck()

        elif checkers_and_moves:

            sleep(1)

            bot_checker = choice(list(checkers_and_moves.keys()))

            bot_move = choice(checkers_and_moves[bot_checker])

            self.move_checker(bot_checker, bot_move)

            
        else:
            return False # Path to exit programm

        self.reverse_deck()
        return True
    
    def user_turn(self):
        
        while True:

            self.generate_deck()
            self.print_deck()

            checkers_and_attacks = self.possible_turn_attacks(self.USER_COLOR)
            checkers_and_moves = self.possible_turn_moves(self.USER_COLOR)

            # Attacking loop
            if checkers_and_attacks:

                checker = self.captured_deck_object(self.get_start_cell())

                if checker not in checkers_and_attacks.keys():

                    self.warning_message = 'Choose checker to attack!'
                    continue

                while checker in checkers_and_attacks.keys():

                    user_move = self.get_end_cell()

                    if user_move not in checkers_and_attacks[checker].keys():

                        self.warning_message = 'Wrong attack!'
                        continue

                    enemy_checker = checkers_and_attacks[checker][user_move]
                    user_move = {user_move: enemy_checker}
                    self.attack(checker, user_move)

                    checkers_and_attacks = self.possible_turn_attacks(self.USER_COLOR)
                
            elif checkers_and_moves:
                
                checker = self.captured_deck_object(self.get_start_cell())

                if checker not in checkers_and_moves.keys():

                    self.warning_message = 'This checker can''t make a move!'
                    continue
                
                user_move = self.get_end_cell()

                if user_move not in checkers_and_moves[checker]:

                    self.warning_message = 'Wrong move!'
                    continue

                self.move_checker(checker, user_move)

            else:
                return False # Path to exit programm

            break

        return True
