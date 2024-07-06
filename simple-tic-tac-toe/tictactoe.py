"""
Jet Brains Academy Tic-Tac-Toe project
Code by: Josh Voyles
"""

import re


def horizontal_scan(play_field) -> tuple:
    """
    Scans the given play field horizontally to match 3 X or O.

    :param play_field: he 3x3 play field grid.
    :type play_field: list of lists

    :return: A tuple with two boolean values indicating whether 'X' wins and
    whether 'O' wins.
    :rtype: tuple[bool, bool]
    """
    x_wins = False
    o_wins = False
    for line in play_field:
        if ''.join(line) == '|XXX|':
            x_wins = True
        elif ''.join(line) == '|OOO|':
            o_wins = True
    return x_wins, o_wins


def vertical_scan(play_field) -> tuple:
    """
    Perform a vertical scan of each column.

    :param play_field: The 3x3 play field grid.
    :type play_field: list of lists
    :return: A tuple containing the results of the vertical scan.
             First element is a boolean indicating if 'X' has won vertically.
             Second element is a boolean indicating if 'O' has won vertically.
             Third element is a boolean indicating if there are no remaining _.
    :rtype: tuple
    """
    finished = True
    # scan of each row in play_field (start index 1, move 3)
    for x in range(1, 4, 1):
        # set counts to 0 for vertical scan
        x_count = 0
        o_count = 0
        # vertical scan
        for y in range(1, 4, 1):
            if play_field[y][x] == 'X':
                x_count += 1
            elif play_field[y][x] == 'O':
                o_count += 1
            elif play_field[y][x] == '_':
                finished = False
        x_wins, o_wins = match_three(x_count, o_count)
        if x_wins or o_wins:
            return x_wins, o_wins, finished
    return False, False, finished


def diagonal_scan_lr(play_field) -> tuple:
    """
    Find matches for diagonal scanning from left to right.

    :param play_field: The 3x3 play field grid.
    :return: A tuple (x_wins, o_wins) indicating whether 'X' or 'O' has won.

    """
    x_count = 0
    o_count = 0
    i = 1
    for x in range(1, 4, 1):
        if play_field[x][i] == 'X':
            x_count += 1
        elif play_field[x][i] == 'O':
            o_count += 1
        i += 1
    x_wins, o_wins = match_three(x_count, o_count)
    return x_wins, o_wins


def diagonal_scan_rl(play_field) -> tuple:
    """
    Examine the diagonal from the top right to bottom left of the play field.

    :param play_field: The 3x3 play field grid.
    :return: A tuple containing two boolean values indicating if 'X' wins
    and if 'O' wins, respectively.

    """
    x_count = 0
    o_count = 0
    i = 1
    for x in range(3, 0, -1):
        if play_field[x][i] == 'X':
            x_count += 1
        elif play_field[x][i] == 'O':
            o_count += 1
        i += 1
    x_wins, o_wins = match_three(x_count, o_count)

    return x_wins, o_wins


def analyze_game_state(play_field) -> str:
    """
    Analyzes the current state of the game based on the given play field.

    :param play_field: The current play field of the game.
    :return: A string representing the result of the game
    (e.g. "X wins", "O wins", "Draw").
    """
    finished = True
    x_wins, o_wins = horizontal_scan(play_field)
    if not x_wins and not o_wins:
        x_wins, o_wins, finished = vertical_scan(play_field)
    if not x_wins and not o_wins:
        x_wins, o_wins = diagonal_scan_lr(play_field)
    if not x_wins and not o_wins:
        x_wins, o_wins = diagonal_scan_rl(play_field)

    return check_win(x_wins, o_wins, finished)


def match_three(x_count, y_count) -> tuple:
    """
    Check if either player X or player O has won the match.

    :param x_count: The count of matches won by player X.
    :type x_count: int
    :param y_count: The count of matches won by player O.
    :type y_count: int
    :return: A tuple containing two boolean values
    indicating if player X or player O has won.
    :rtype: tuple
    """
    x_wins = False
    o_wins = False
    if x_count == 3:
        x_wins = True
    if y_count == 3:
        o_wins = True
    return x_wins, o_wins


def check_win(x_wins, o_wins, finished) -> str:
    """
    Determines the result of a Tic Tac Toe game.

    :param x_wins: True if X has won, False otherwise.
    :param o_wins: True if O has won, False otherwise.
    :param finished: True if no remaining underscores.
    :return: The result of the current state.
    Possible values are 'Draw', 'X wins', 'O wins', and 'Continue'.
    """
    if not x_wins and not o_wins and finished:
        return 'Draw'
    elif x_wins:
        return "X wins"
    elif o_wins:
        return "O wins"
    else:
        return "Continue"


def switch_player(player) -> str:
    """
    Switches the player in a game.

    :param player: The current player ('X' or 'O').
    :return: The opposite player ('O' if 'X' is given, 'X' otherwise').
    """
    if player == 'X':
        return 'O'
    return 'X'


def main() -> None:
    """
    Main method for playing Tic Tac Toe game.
    Includes input validation.

    :return: None
    """
    current_player = 'X'  # starting player

    # default play field
    play_field = [['---------'],
                  ['|', '_', '_', '_', '|'],
                  ['|', '_', '_', '_', '|'],
                  ['|', '_', '_', '_', '|'],
                  ['---------']]

    while True:
        # print play field
        for line in play_field:
            print(*line)

        selection = input()  # get user coordinates
        coordinates = selection.split(" ")  # split into list

        # validate numbers
        if not re.match(r'\d \d\b', selection):
            print("You should enter numbers!")
        # validate range (1-3)
        elif not re.match(r'[1-3] [1-3]', selection):
            print("Coordinates should be from 1 to 3!")
        # validate empty cell
        elif play_field[int(coordinates[0])][int(coordinates[1])] != '_':
            print("This cell is occupied! Choose another one!")
        # check win condition if everything is valid
        else:
            # input X or O into play field
            play_field[int(coordinates[0])][
                int(coordinates[1])] = current_player
            game_state = analyze_game_state(play_field)  # check for win
            # if anything but Continue we keep playing
            if game_state != 'Continue':
                for line in play_field:
                    print(*line)
                print(game_state)
                exit()

        current_player = switch_player(current_player)


if __name__ == '__main__':
    main()
