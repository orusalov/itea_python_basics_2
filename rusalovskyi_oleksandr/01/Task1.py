"""
Create a game - 21.
There are 10 cards representing values 2-11.
The goal is to get max points, but less then 21.
Each turn a player should decide pick a new card o pass.
Pick - value of a card should be added to player's points.
If player gets more then 21 points - he lost.
Pass - no new cards, player stays with current points.
Results should be shown only after all the players passed

Level 3 - one player + two bots.

author: Oleksandr Rusalovskyi
2019-11-20
"""
from random import randint

MIN_CARD_POINTS = 2
MAX_CARD_POINTS = 11
MAXIMUM_POINTS_THRESHOLD = 21

while True:
    choise = input('Start new game?(Y/N): ').lower()

    if choise != 'n' and choise != 'y':

        print('Wrong input!')
        continue

    elif choise == 'n':

        print('Goodbye!!!')
        break
    
    user_points = 0
    bot_1_points = 0
    bot_2_points = 0

    ##### User picks cards #####
    i = 0
    while i < 2:

        random_card = randint(MIN_CARD_POINTS,11)
        user_points += random_card
        i += 1

    print('You got ' + str(user_points - random_card) + ' and ' + str(random_card) + '. You have '
          + str(user_points) + ' points')

    while True:
        # when user have maximum points - stop his picks
        if user_points == MAXIMUM_POINTS_THRESHOLD:

            print('Congratulations! You have maximum ' + str(MAXIMUM_POINTS_THRESHOLD) + ' points')
            break

        choise = input('Will you pick new card?(Y/N): ').lower()
        # answer parsing
        if choise != 'n' and choise != 'y':

            print('Wrong input! You have ' + str(user_points) + ' points')
            continue

        elif choise == 'n':

            print('You finished with ' + str(user_points) + ' points')
            break

        random_card = randint(MIN_CARD_POINTS,MAX_CARD_POINTS)
        user_points += random_card

        print('You got ' + str(random_card) + '. You have ' + str(user_points) + ' points')

        # user lost
        if user_points > MAXIMUM_POINTS_THRESHOLD:

            print('You lost!')
            break

    input('\nPress Enter to continue ')#make a pause to understand how many points you have

    print()#new line to separate players

    ##### First bot #####

    # minimum decision threshold is when bot scares to take MAX_CARD_POINTS not to loose
    # maximum decision threshold for fearless bot
    bot_decision_threshold = randint(MAXIMUM_POINTS_THRESHOLD - MAX_CARD_POINTS + 1,MAXIMUM_POINTS_THRESHOLD)

    while bot_1_points < bot_decision_threshold:

        random_card = randint(MIN_CARD_POINTS,MAX_CARD_POINTS)
        bot_1_points += random_card
        print('Bot_1 took ' + str(random_card) + '. He has ' + str(bot_1_points) + ' points')

    if bot_1_points > MAXIMUM_POINTS_THRESHOLD:
        print('Bot_1 lost!')
    else:
        print('Bot_1 passes')

    print()#new line to separate players

    ##### Second bot #####

    # minimum decision threshold is when bot scares to take MAX_CARD_POINTS not to loose
    # maximum decision threshold for fearless bot
    bot_decision_threshold = randint(MAXIMUM_POINTS_THRESHOLD - MAX_CARD_POINTS + 1,MAXIMUM_POINTS_THRESHOLD)

    while bot_2_points < bot_decision_threshold:

        random_card = randint(MIN_CARD_POINTS,MAX_CARD_POINTS)
        bot_2_points += random_card
        print('Bot_2 took ' + str(random_card) + '. He has ' + str(bot_2_points) + ' points')

    if bot_2_points > MAXIMUM_POINTS_THRESHOLD:
        print('Bot_2 lost!')
    else:
        print('Bot_2 passes')

    print()#new line to separate results

    ##### Winner decision #####

    # print players points
    print('User points:  ' + str(user_points) +
          '\nBot_1 points: ' + str(bot_1_points) +
          '\nBot_2 points: ' + str(bot_2_points) +
          '\n')

    # Winner decision making
    if (user_points > MAXIMUM_POINTS_THRESHOLD and
        bot_1_points > MAXIMUM_POINTS_THRESHOLD and
        bot_2_points > MAXIMUM_POINTS_THRESHOLD):

        result = 'Everybody lost!'
    
    elif (user_points <= MAXIMUM_POINTS_THRESHOLD and
             (bot_1_points > MAXIMUM_POINTS_THRESHOLD and
              bot_2_points > MAXIMUM_POINTS_THRESHOLD or
                 (user_points > bot_1_points and
                     (bot_2_points > MAXIMUM_POINTS_THRESHOLD or
                      user_points > bot_2_points)) or
                 (user_points > bot_2_points and
                     (bot_1_points > MAXIMUM_POINTS_THRESHOLD or
                      user_points > bot_1_points)))):

        result = 'You won'

    elif (bot_1_points <= MAXIMUM_POINTS_THRESHOLD and
             (user_points > MAXIMUM_POINTS_THRESHOLD and
              bot_2_points > MAXIMUM_POINTS_THRESHOLD or
                 (bot_1_points > user_points and
                     (bot_2_points > MAXIMUM_POINTS_THRESHOLD or
                      bot_1_points > bot_2_points)) or
                 (bot_1_points > bot_2_points and
                     (user_points > MAXIMUM_POINTS_THRESHOLD or
                      bot_1_points > user_points)))):

        result = 'Bot_1 won'

    elif (bot_2_points <= MAXIMUM_POINTS_THRESHOLD and
             (user_points > MAXIMUM_POINTS_THRESHOLD and
              bot_1_points > MAXIMUM_POINTS_THRESHOLD or
                 (bot_2_points > user_points and
                     (bot_1_points > MAXIMUM_POINTS_THRESHOLD or
                      bot_2_points > bot_1_points)) or
                 (bot_2_points > bot_1_points and
                     (user_points > MAXIMUM_POINTS_THRESHOLD or
                      bot_2_points > user_points)))):

        result = 'Bot_2 won'

    elif (user_points <= MAXIMUM_POINTS_THRESHOLD and
          user_points == bot_1_points and
             (bot_2_points > MAXIMUM_POINTS_THRESHOLD or
              user_points > bot_2_points)):

        result = 'You and Bot_1 won'

    elif (user_points <= MAXIMUM_POINTS_THRESHOLD and
          user_points == bot_2_points and
             (bot_1_points > MAXIMUM_POINTS_THRESHOLD or
              user_points > bot_1_points)):

        result = 'You and Bot_2 won'

    elif (bot_1_points <= MAXIMUM_POINTS_THRESHOLD and
          bot_1_points == bot_2_points and
             (user_points > MAXIMUM_POINTS_THRESHOLD or
              bot_1_points > user_points)):

        result = 'Bot_1 and Bot_2 won'

    else:
        result = 'All players has equal points. Everybody won!'

    print(result+'\n')
