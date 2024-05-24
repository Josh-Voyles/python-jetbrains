import random

game_state = 'player'


def show_header() -> str:
    """
    Returns a header string.

    :return: A string containing a formatted header.
    """
    return ("=============================="
            "========================================")


def show_stock_size(stock_pieces) -> str:
    """
    Calculate the size of the stock.

    :param stock_pieces: The list of stock pieces.
    :return: The size of the stock.
    """
    return f'Stock size: {len(stock_pieces)}'


def show_computer_piece_count(computer_pieces) -> str:
    """
    Return the count of computer pieces.

    :param computer_pieces: The list of computer pieces.
    :return: The count of computer pieces as a formatted string.
    """
    return f'Computer pieces: {len(computer_pieces)}'


def show_player_pieces(player_pieces) -> str:
    """
    Displays each piece on a new line.

    :param player_pieces: a list of pieces owned by the player
    :return: a string representation of the player's pieces

    """
    return ('Your pieces:' +
            ''.join([f'\n{x + 1}: {piece}' for x,
            piece in enumerate(player_pieces)]))


def show_game_board(header, stock, c_pieces, snake, p_pieces):
    """
    Returns string representation of game board and state.

    :param header: The header of the game board.
    :param stock: The stockpile of dominoes.
    :param c_pieces: The computer's pieces.
    :param snake: The current snake of played dominoes.
    :param p_pieces: The player's pieces.
    :return: The formatted string representation of the game board.

    """
    return f"{header}\n {stock}\n {c_pieces}\n\n {snake}\n{p_pieces}\n"


def find_starting_piece(computer_pieces, player_pieces) -> list:
    """
    Finds the starting piece based on the highest domino between computer and
    player.

    :param computer_pieces: A list of integers representing the computer's
    pieces.
    :param player_pieces: A list of integers representing the player's pieces.
    :return: The highest value among the computer and player pieces.
    """
    global game_state
    if max(computer_pieces) > max(player_pieces):
        biggest = max(computer_pieces)
        computer_pieces.remove(biggest)
        return biggest
    else:
        biggest = max(player_pieces)
        player_pieces.remove(biggest)
        game_state = 'computer'
        return biggest


def print_snake(domino_snake) -> str:
    """
    Prints the given domino snake. If snake is over length of 6, snake
    is condensed showing first 3 and last 3 split with ...

    :param domino_snake: A list representing the domino snake.
    :return: A string representing the printed domino snake.
    """
    if len(domino_snake) < 7:
        snake = ''.join([str(x) for x in domino_snake])
        return f'{snake}'
    front = ''.join([str(x) for x in domino_snake[0:3]])
    back = ''.join(str(x) for x in domino_snake[-3:])
    return f'{front}' + '...' + f'{back}'


def process_player_input(player_pieces, domino_snake, stock_pieces,
                         number_count) -> None:
    """
    :param player_pieces: The list of dominos that the player has in their hand.
    :param domino_snake: The list representing the snake of
    dominos on the table.
    :param stock_pieces: The list of dominos in the stock.
    :param number_count: The number of dominos that each player should have at
    the start of the game.
    :return: None

    This method processes the input provided by the player. It checks if the
    selection is within the valid range of the player's pieces, and if it is a
    valid move. If the selection is valid, it updates the game state by making
    the move and returns. If the input is invalid, it displays an error message
    and prompts the player to try again.
    """
    while True:
        selection = input()
        try:
            if len(player_pieces) >= int(selection) >= -len(player_pieces):
                if validate_correct_selection(int(selection), player_pieces,
                                              domino_snake, stock_pieces):
                    process_move(player_pieces, int(selection), stock_pieces,
                                 domino_snake, number_count)
                    return
            else:
                raise ValueError
        except ValueError:
            print('Invalid input. Please try again.')
        except TypeError:
            print('Invalid input. Please try again.')


def process_computer_move(computer_pieces, number_count, domino_snake,
                          stock_pieces) -> None:
    """
    :param computer_pieces: List of domino pieces held by the computer.
    :param number_count: Dictionary representing the count of each number
    on the board.
    :param domino_snake: List representing the domino snake on the board.
    :param stock_pieces: List of domino pieces available in the stock.
    :return: None

    This method processes the computer's move in a game of dominoes. It
    selects the domino with the highest frequency of occurrence. The
    selected piece is then validated against the current board state to
    ensure it can be played. If a valid piece is found, the process_move()
    method is called with the appropriate parameters. If no valid pieces
    are found, the  continues choosing until a valid piece is chosen.
    If no piece can be chosen, the computer draws from the stock.
    """
    # copying lets us remove numbers for each loop to find second highest
    numbers = number_count.copy()

    while True:
        if len(numbers) == 0:
            process_move(computer_pieces, 0, stock_pieces, domino_snake,
                         number_count)
            return
        max_value = max(numbers)
        for count, x in enumerate(computer_pieces):
            total = sum(x)
            #  total = frequency of occurrence
            if total > 7:
                total = 12 - total

            if total == max_value:
                if validate_correct_selection(count + 1, computer_pieces,
                                              domino_snake, stock_pieces):
                    process_move(computer_pieces, count + 1, stock_pieces,
                                 domino_snake, number_count)
                    return
                elif validate_correct_selection(-count - 1, computer_pieces,
                                                domino_snake, stock_pieces):
                    process_move(computer_pieces, -count - 1, stock_pieces,
                                 domino_snake, number_count)
                    return
        numbers.remove(max_value)


def process_move(pieces, move, stock_pieces, domino_snake,
                 number_count) -> None:
    """

    This method processes a move in a domino game. Insert the piece to the front
    or back of snake depending on move.

    :param pieces: A list of domino pieces held by a player.
    :param move: An integer representing the move to be made.
    Positive values indicate playing a piece from the player's hand,
    negative values indicate drawing a piece from the stock, and zero
    indicates passing the turn.
    :param stock_pieces: A list of domino pieces remaining in the stock.
    :param domino_snake: A list representing the domino snake on the table.
    :param number_count: A dictionary keeping track of the count of each number
     on the domino snake.
    :return: None

    """
    if move > 0:
        piece = pieces[move - 1]
        add_count(number_count, piece)
        if domino_snake[-1][1] != piece[0]:
            domino_snake.append(rotate_domino(piece))
        else:
            domino_snake.append(piece)
        pieces.remove(pieces[move - 1])
    elif move < 0:
        piece = pieces[abs(move) - 1]
        add_count(number_count, piece)
        if domino_snake[0][0] != piece[1]:
            domino_snake.insert(0, rotate_domino(piece))
        else:
            domino_snake.insert(0, piece)
        pieces.remove(pieces[abs(move) - 1])
    else:
        piece = stock_pieces.pop()
        add_count(number_count, piece)
        pieces.append(piece)


def rotate_domino(piece) -> list:
    """
    Rotate a domino piece.

    :param piece: A list representing a domino piece with two values.
    :return: A list representing the rotated domino piece with the first and
    second values switched.
    """
    return [piece[1], piece[0]]


def check_ends(domino_snake) -> bool:
    """
    Check if the domino snake satisfies certain conditions regarding its ends.

    :param domino_snake: A list representing the domino snake. Each element
    in the list is a tuple containing two numbers representing a domino
    piece. :return: A boolean value indicating whether the domino snake meets
    the specified conditions.

    This function counts the occurrence of a particular number if the first
    and last number in the snake are equal. If the total is 8, the game is a
    draw because the game cannot continue.
    """
    count = 0
    if domino_snake[0][0] == domino_snake[-1][1]:
        key = domino_snake[0][0]
        for x in domino_snake:
            if x[0] == key and x[1] == key:
                count += 2
            elif x[0] == key or x[1] == key:
                count += 1
        if count >= 8:
            return True
    return False


def validate_correct_selection(move, pieces, domino_snake, stock_pieces) \
        -> bool:
    """
    If the move is equal to 0 and there are remaining pieces in the stock,
    the method returns True indicating that the move is valid.

    If the move is greater than 0, it checks if the piece at the end of the
    domino snake is present in the list of pieces at index (move - 1). If it
    is present, the method returns True indicating that the move is valid.

    If the move is less than 0, it checks if the first number of the first
    piece in the domino snake is present in the list of pieces at index (abs(
    move) - 1). If it is present, the method returns True indicating that
    the move is valid.

    If the game state is 'player', meaning it's the player's turn, it prints
    a message indicating an illegal move and returns False.

    If none of the above conditions are met, the method returns False
    indicating that the move is not valid.

    :param move: An integer representing the move to be validated.
    :param pieces: A list containing the pieces held by the player or ai.
    :param domino_snake: A list representing the domino snake.
    :param stock_pieces: A list containing the remaining pieces in the stock.
    :return: A boolean value indicating whether the move is valid or not.
    """
    global game_state
    if move == 0 and len(stock_pieces) != 0:
        return True
    elif move > 0:
        if domino_snake[-1][1] in pieces[move - 1]:
            return True
    elif move < 0:
        if domino_snake[0][0] in pieces[abs(move) - 1]:
            return True
    if game_state == 'player':  # because we don't need to tell AI
        print('Illegal move. Please try again.')
    return False


def init_count(number_count, computer_pieces, domino_snake) -> None:
    """
    Initializes the count of numbers in the computers hand and the starting
    domino snake.

    :param number_count:count of specific numbers in snake and ai hand
    :param computer_pieces: the ai's current hand
    :param domino_snake: the domino snake
    :return: None
    """
    for x in computer_pieces:
        num1 = x[0]
        num2 = x[1]
        number_count[num1] += 1
        number_count[num2] += 1
    number_count[domino_snake[0][0]] += 1
    number_count[domino_snake[0][1]] += 1


def add_count(number_count, piece) -> None:
    """
    Modifies number_count list by adding occurrences of the player or computer
    move.
    """
    number_count[piece[0]] += 1
    number_count[piece[1]] += 1


def main() -> None:
    # store ai hand and snake number counts
    number_count = [0, 0, 0, 0, 0, 0, 0]
    global game_state

    # builds initial state of game
    stock_pieces = [[x, y + x] for x in range(7) for y in range(7 - x)]
    random.shuffle(stock_pieces)
    computer_pieces = [stock_pieces.pop() for _ in range(7)]
    player_pieces = [stock_pieces.pop() for _ in range(7)]
    domino_snake = [find_starting_piece(computer_pieces, player_pieces)]
    init_count(number_count, computer_pieces, domino_snake)

    # loops until win condition test breaks loop
    while True:
        #  print game state
        print(show_game_board(show_header(), show_stock_size(stock_pieces),
                              show_computer_piece_count(computer_pieces),
                              print_snake(domino_snake),
                              show_player_pieces(player_pieces)))

        # check for win condition
        if len(player_pieces) == 0:
            print('Status: The game is over. You won!')
            break
        elif len(computer_pieces) == 0:
            print('Status. The game is over. The computer won!')
            break
        elif check_ends(domino_snake) or len(stock_pieces) == 0:
            print('Status: The game is over. It\'s a draw!')
            break

        # tailored messaging depending on player
        if game_state == 'player':
            print('Status: It\'s your turn to make a move. Enter your command.')
        else:
            print('Status: Computer is about to make a move. Press Enter to '
                  'continue...')

        # process move and switch players
        if game_state == 'player':
            process_player_input(player_pieces, domino_snake, stock_pieces,
                                 number_count)
            game_state = 'computer'
        else:
            input()  # press enter move, does nothing except continue
            process_computer_move(computer_pieces, number_count, domino_snake,
                                  stock_pieces)
            game_state = 'player'


if __name__ == '__main__':
    main()
