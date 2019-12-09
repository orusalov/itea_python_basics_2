from random import randint

class World:

    LIFES_ON_MAP = 3

    _world = []
    hearts_positions = [[]]
    exit_position = []
    size_y = 0
    size_x = 0

    def __init__(self, size_y, size_x):
        
        self.size_y = size_y
        self.size_x = size_x
        
        self.hearts_positions = self.generate_empty_positions(self.LIFES_ON_MAP)
        
        self.exit_position = self.generate_empty_positions()[0]
        
    
    def _set_positions(self, symbol):


        def return_function(*positions):
        
            for position in positions:
                self._world[position[0]][position[1]] = symbol

            return None


        return return_function

    
    def _occupied_positions(self):

        # If new occupied places created than this method should be updated
        return_val = self.hearts_positions.copy()
        return_val.append(self.exit_position)
        
        return return_val        

    def generate_empty_positions(self, number=1):

        positions = []
        
        i = 0
        while i < number:

            position = [randint(0, self.size_y - 1),randint(0, self.size_x - 1)]

            if (position not in positions and
                position not in self._occupied_positions()):

                positions.append(position)
                i += 1

        return positions

    def heart_check(self, position):

        if position in self.hearts_positions:
            self.hearts_positions.remove(position)
            return 1
        else:
            return 0

    def exit_check(self, position):

        if position == self.exit_position:
            return True
        else:
            return False

    def get_world(self):
        """
        function get_world() returns visual representation of world
        """

        set_heart = self._set_positions('H')
        set_exit = self._set_positions('E')

        self._world = [[' ' for _ in range(self.size_x)] for _ in range(self.size_y)]

        set_heart(*self.hearts_positions)
        set_exit(self.exit_position)
        
        return self._world
