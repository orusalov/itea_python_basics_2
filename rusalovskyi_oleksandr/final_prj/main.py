from checkers import Table


def main():

    table_size = int(input('Input checkers table size: ').strip())
    table = Table(table_size)

    while True:
        try:
            if table.current_turn == table.USER_COLOR:

                if not table.user_turn():
                    print('User lost!')
                    break                

                table.current_turn = table.get_enemy_color()
                
            
            if not table.bot_turn():
                print('Bot lost!')
                break
            
            table.current_turn = table.get_enemy_color()
            
        except KeyboardInterrupt:
            print('Goodbye!')
            break


if __name__ == '__main__':
    main()
