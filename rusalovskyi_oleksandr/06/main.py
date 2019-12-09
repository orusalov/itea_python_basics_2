import gamer
import world
from move_guy import get_move


def print_world(gamer):
    
    matrix = gamer.world.get_world()

    matrix[gamer.position[0]][gamer.position[1]] = gamer.character
    
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

    print('--' * len(matrix[0]))

    for row in matrix:
        print('|{}|'.format(' '.join(row)))

    print('--' * len(matrix[0]))

    print('life: ' + str(gamer.life))


def main():

    #input map size
    SIZE_X, SIZE_Y = int(input('X: ')), int(input('Y: '))
    #initialize world
    w = world.World(SIZE_X, SIZE_Y)

    #initialize gamer using world. Gamer live in already created world
    g = gamer.Gamer(w)

    print_world(g)

    while True:

        # update gamer position
        proceed = g.update_user_position(get_move())

        print_world(g)

        if proceed in g.end_of_game.keys():
            print(g.end_of_game[proceed])
            print('\n\n')
            break
        else:
            print(proceed)


if __name__ == '__main__':
    # start new game
    while True:

        start = input('Start new game?(Y/N) ').lower()
        if start not in list('yn'):

            print('Wrong answer!')
            continue

        elif start == 'n':

            print('Goodbuy')
            break

        else:
            main()
