MOVE_DICT = {'w':[-1, 0], 's':[1, 0], 'a':[0, -1], 'd':[0, 1]}

def get_move():
    
    choise = input('\n w \nasd\nchoose direction (wasd): ').lower()
    if choise not in MOVE_DICT.keys():

        print('Wrong input!')
        return [0, 0]

    else:
        return MOVE_DICT[choise]
