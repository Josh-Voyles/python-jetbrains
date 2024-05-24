"""
Jet Brains Academy Game
Code by: Josh Voyles
"""
import random

# programmer defined player names, must be 'John' and 'Jack' for exercise
PLAYER_ONE = 'John'
PLAYER_TWO = 'Jack'


def get_pencils() -> int:
    """
    Gets user input for number of pencils to take from in game
    :return: number of 'pencils' as int for game mechanic
    """
    pencils = 0
    while pencils == 0:
        try:
            pencils = int(input())
            if pencils > 0:
                return pencils
            else:
                print("The number of pencils should be positive")
        except ValueError:
            print("The number of pencils should be numeric")
        pencils = 0


def get_player(possible_names) -> str:
    """
    Lets player choose starting player based on list of names
    :param possible_names: used to validate user entry
    :return: player name as string to assign as current player
    """
    while True:
        p1 = input()
        if p1 not in possible_names:
            print(f"Choose between {PLAYER_ONE} and {PLAYER_TWO}")
        else:
            return p1


def bot_move(number_of_pencils) -> int:
    """
    Bot mechanic: leans to win, selects amount for wining strategy; explained below
    :param number_of_pencils: current number of pencils based on game state
    :return: bots number selection as int
    """
    if number_of_pencils == 1:  # if only 1 pencil, we choose 1 and loose
        return 1
    elif number_of_pencils % 4 == 1:  # if pencils # is high and already wining; choose random
        return random.randint(1, 3)
    else:
        return (number_of_pencils - 1) % 4  # returns 1, 2 or 3 for the win


def player_move(num_of_pencils, possible_values) -> int:
    """
    Player must take 1, 2 or 3 pencils
    Validates selection and ensures you cannot take more pencils than there are available
    :param num_of_pencils: current quality of pencils remaining
    :param possible_values: list of possible pencil numbers to choose
    :return: players choice for # of pencils to take
    """
    take = 0
    while take == 0:
        try:
            take = int(input())
            if take not in possible_values:
                print("Possible values: '1', '2' or '3'")
            elif num_of_pencils - take < 0:
                print("Too many pencils were taken")
            else:
                return take
        except ValueError:
            print("Possible values: '1', '2' or '3'")
        take = 0


def game(num_of_pencils, active_player, possible_values) -> None:
    """
    game loop will alternate players allowing each to take 1-3 pencils
    loop ends when a player (or bot) takes the last pencil
    :param num_of_pencils: quantity of pencils remaining
    :param active_player: current player
    :param possible_values: 1-3
    :return: no return value
    """

    while num_of_pencils > 0:
        print("".join(_ for _ in ("|" for _ in range(num_of_pencils))))
        if active_player == 'John':
            print(f"{active_player}'s turn!")
        else:
            print(f"{active_player}'s turn:")

        if active_player == 'Jack':
            take = bot_move(num_of_pencils)
            print(take)
        else:
            take = player_move(num_of_pencils, possible_values)

        num_of_pencils = num_of_pencils - take

        if active_player == PLAYER_ONE:
            active_player = PLAYER_TWO
        else:
            active_player = PLAYER_ONE

        if num_of_pencils == 0:
            print(f'{active_player} won!')


def main() -> None:
    """
    Assigns game variables, assigns starting pencil quality, determines first player, starts game loop
    :return: no return value
    """
    possible_values = [1, 2, 3]
    possible_names = [PLAYER_ONE, PLAYER_TWO]
    print("How many pencils would you like to use:")
    num_of_pencils = get_pencils()
    print(f"Who will be the first ({PLAYER_ONE}, {PLAYER_TWO}):")
    active_player = get_player(possible_names)
    game(num_of_pencils, active_player, possible_values)


if __name__ == '__main__':
    main()
