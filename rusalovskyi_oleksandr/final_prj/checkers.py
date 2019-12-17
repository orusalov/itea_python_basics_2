from random import choice
from time import sleep




class Checker:
    """
    class Checker has only two attributes: position and color.
    """
    def __init__(self, position, color):

        self.position = position
        self.color = color
        
    def __str__(self):
        return self.color




class TooBigTable(Exception):
    """
    Exception for too large table
    """
    def __init__(self, message):
        self.message = message




class TooSmallTable(Exception):
    """
    Exception for too small table
    """
    def __init__(self, message):
        self.message = message
    



class Table:

    LETTERS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    def __init__(self, size):
        """
        initiates Table instance
        :param size: size of the deck
        :type size: int
        """
        if size > len(self.LETTERS):
            raise TooBigTable(f'Too big table for checkers. Max table size is {len(self.LETTERS)}')
        elif size < 4:
            raise TooSmallTable('Too small table for checkers. Min table size is 4')
        
        self.SIZE = size
        self.USER_COLOR = 'o'
        self.BOT_COLOR = 'x'
        self.EMPTY_COLOR = ' '
        self.POSSIBLE_MOVES = [(1, -1), (1, 1)]
        self.POSSIBLE_ATTACKS = [(2, -2), (2, 2)]

        # take only SIZE letters
        self.letters = self.LETTERS[:self.SIZE]

        self.deck = [[self.EMPTY_COLOR for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        
        self.armies = {}
        self.armies[self.BOT_COLOR] = self._generate_army(self.BOT_COLOR)
        self.armies[self.USER_COLOR] = self._generate_army(self.USER_COLOR)

        self.current_turn = choice([self.USER_COLOR, self.BOT_COLOR])

        # cells
        self.get_start_cell = self._get_cell('checker', self.USER_COLOR)
        self.get_end_cell = self._get_cell('move to', self.EMPTY_COLOR)

        # possible checker moves
        self.possible_checker_regular_moves = self._get_positions_by_relative_change_and_color(self.POSSIBLE_MOVES, self.EMPTY_COLOR)
        self.possible_checker_attack_moves = self._get_positions_by_relative_change_and_color(self.POSSIBLE_ATTACKS, self.EMPTY_COLOR)

        # POSSIBLE TURN MOVES AND ATTACKS
        self.possible_turn_moves = self._possible_turn(self.possible_checker_regular_moves)
        self.possible_turn_attacks = self._possible_turn(self.possible_checker_attack)

        self.warning_message = ''
    

    def _generate_army(self, color):
        """
        generates army for game
        :param color: color for army
        :type color: str
        :return: list of checkers
        :rtype: list
        """ 
        n = int((self.SIZE - 2) / 2)
        army = [Checker([i, j], color) for i in range(n) for j in range(i % 2, self.SIZE, 2)]

        return army   
        
    def _get_cell(self, type_, expected_cell_color):
        """
        getting a function for input start and finish cell
        :param expected_cell_color: expected cell color
        :type expected_cell_color: str
        :return: fucntion for inputing positions
        :rtype: function
        """ 
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

    def _get_positions_by_relative_change_and_color(self, interested_moves, interested_color):
        """
        getting a function for serching real positions using possible move and color
        :param interested_moves: list of possible relative changes
        :param interested_color: interested deck color
        :type interested_moves: list
        :type interested_color: str
        :return: fucntion for serching real positions
        :rtype: function
        """    
        def return_func(checker):

            position = checker.position
            result_positions = []
            for relative_change in interested_moves:
                interested_position = tuple(map(lambda n, m: n + m, position, relative_change))

                if self.is_inside_table(interested_position) and self.is_expected_cell_color(interested_position, interested_color):
                    result_positions.append(interested_position)

            return result_positions

        return return_func

    '''
        POSSIBLE TURN MOVES AND ATTACKS
    '''    
    def _possible_turn(self, move_or_atack_function):
        """
        getting a function for turn moves or attacks possible
        :param move_or_atack_function: function for checker possible moves or attacks
        :type move_or_atack_function: function
        :return: fucntion for getting all possible moves or attacks
        :rtype: function
        """            
        def return_function(turn_color):

            result = {}
            for checker in self.armies[turn_color]:
                
                possible_ch_moves = move_or_atack_function(checker)
                if possible_ch_moves:
                    result[checker] = possible_ch_moves

            return result

        return return_function

    # can't be made as return function, because self.get_enemy_color() changes every move
    def nearby_enemies(self, checker):
        """
        getting positions of nearby enemy players on the deck
        :param checker: cheker for wich you searching nearby enemies
        :type checker: Checker
        :return: positions of nearby enemies
        :rtype: list
        """
        return self._get_positions_by_relative_change_and_color(self.POSSIBLE_MOVES, self.get_enemy_color())(checker)

    def get_enemy_color(self):
        """
        method get_enemy_color() returns enemy color for current turn
        :return: enemy color
        :rtype: str
        """
        if self.USER_COLOR == self.current_turn:
            return self.BOT_COLOR
        elif self.BOT_COLOR == self.current_turn:
            return self.USER_COLOR
        else:
            return ''

    '''
    DECK METHODS
    '''
    def captured_deck_object(self, position):
        """
        returns captured object from the deck by position
        :param position: position on the deck
        :type position: tuple
        :return: object from the deck
        :rtype: Checker or str
        """
        return self.deck[position[0]][position[1]]

    def reverse_deck(self):
        """
        reverses deck for bot's move
        """
        for row in self.deck:
            row.reverse()
            
        self.deck.reverse()

    def generate_deck(self):
        """
        generates deck after each move
        """
        self.deck = [[self.EMPTY_COLOR for _ in range(self.SIZE)] for _ in range(self.SIZE)]

        for armie in [self.armies[self.USER_COLOR], self.armies[self.BOT_COLOR]]:
            for checker in armie:

                x = checker.position[0]
                y = checker.position[1]
                self.deck[x][y] = checker

            self.reverse_deck()
        

    def print_deck(self):
        """
        prints deck after each move
        """
        additional_space = [' ','']
        
        horizon = f'    ' + ' '.join(self.letters)
        
        print(f'\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n{horizon}')
        for row in reversed(list(enumerate(self.deck))):
            print(f'{additional_space[bool(row[0] // 9)]}{row[0] + 1} |{"|".join(list([str(symb) for symb in row[1]]))}| {row[0] + 1}')

        print(f'{horizon}')

        print(self.warning_message)
        self.warning_message = '' # make warning message null before next turn

    def is_inside_table(self, position):
        """
        checks if position is on the deck
        :param position: position on the deck(or over the deck)
        :type position: tuple
        :return: position if it's on the deck
        :rtype: tuple
        """
        if (position[0] < 0 or
            position[1] < 0 or
            position[0] >= self.SIZE or
            position[1] >= self.SIZE):
            return ()

        return position

    def is_expected_cell_color(self, position, expected_cell_color):
        """
        checks if table position is of expected color
        :param position: position on the deck
        :param expected_cell_color: color
        :type position: tuple
        :type expected_cell_color: str
        :return: is expected cell color
        :rtype: bool
        """
        obj = self.deck[position[0]][position[1]]

        if isinstance(obj, Checker) and obj.color == expected_cell_color:
            return True
        elif obj == expected_cell_color:
            return True
        else:
            return False

    '''
        POSSIBLE CHECKER ATTACK
        possible checker move is in __init__ method
    '''
    def possible_checker_attack(self, checker):
        """
        checks if checker has attacks during this turn
        :param checker: interested checker
        :type checker: Checker
        :return: possible moves with it's beaten enemy's checker
        :rtype: dict
        """
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

    '''
        MOVE AND ATTACK
    '''    
    def move_checker(self, checker, end_pos):
        """
        updates checker position
        :param checker: interested checker
        :param end_pos: checker new position
        :type checker: Checker
        :type end_pos: tuple
        :return: changed position
        :rtype: tuple
        """
        checker.position = end_pos

        if end_pos[0] + 1 == self.SIZE:
            checker.color = checker.color.upper()

        return end_pos

    def attack(self, checker, beaten_checker_and_move):
        """
        atacks enemy's checker
        :param checker: turns checker
        :param beaten_checker_and_move: new position and beeaten checker
        :type checker: Checker
        :type beaten_checker_and_move: dict
        """
        moved_position = self.move_checker(checker, list(beaten_checker_and_move.keys())[0])

        if beaten_checker_and_move[moved_position] in self.armies[self.USER_COLOR]:
            self.armies[self.USER_COLOR].remove(beaten_checker_and_move[moved_position])
        elif beaten_checker_and_move[moved_position] in self.armies[self.BOT_COLOR]:
            self.armies[self.BOT_COLOR].remove(beaten_checker_and_move[moved_position])
        
    '''
        TURNS    
    '''
    def bot_turn(self):
        """
        logic for bot's move
        :return: True if bot has turns and False if bot doesn't have turns
        :rtype: bool
        """

        self.generate_deck()
        self.print_deck()
        self.reverse_deck()

        checkers_and_attacks = self.possible_turn_attacks(self.BOT_COLOR)
        checkers_and_moves = self.possible_turn_moves(self.BOT_COLOR)

        if checkers_and_attacks:

            bot_checker = choice(list(checkers_and_attacks.keys()))
            while bot_checker in checkers_and_attacks.keys():

                # As bot has the same starting positions he has to play on reversed deck
                # so for regenerating deck you should reverse it back
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

        # straight move
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
        """
        logic for user's move
        :return: True if user has turns and False if user doesn't have turns
        :rtype: bool
        """        
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
                        print('Wrong attack!')
                        continue

                    enemy_checker = checkers_and_attacks[checker][user_move]
                    user_move = {user_move: enemy_checker}
                    self.attack(checker, user_move)

                    self.generate_deck()
                    self.print_deck()

                    checkers_and_attacks = self.possible_turn_attacks(self.USER_COLOR)
                
            # straight move
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
