from random import randint

class Gamer:

    life = 3
    character = 'X'
    position = []
    world = []

    end_of_game = {'Game over' : 'You died!', 'Exit' : 'You won! You found exit!'}

    def __init__(self, world):
        self.world = world
        self.position = self.world.generate_empty_positions()[0]

    def update_user_position(self, move):

        if self.life == 0:
            return 'Game over'
        
        new_position = list(map(lambda n, m: n + m, self.position, move))
        if (new_position[0] < 0 or new_position[1] < 0 or
            new_position[0] >= len(self.world.get_world()) or new_position[1] >= len(self.world.get_world()[0])):
            return 'Wrong move!'

        self.position = new_position

        self.life += self.world.heart_check(self.position)

        if self.world.exit_check(self.position):
            return 'Exit'

        # decrease life in random
        if not randint(0,3):
            self.life -= 1

        if self.life == 0:
            self.character = 'O'
            return 'Game over'

        return ' '
