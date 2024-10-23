"""
Module Name: rock-paper-scissors
Author: Josh Voyles
Created: 23 Oct 24

Description:
This project takes you through the steps of building a simple rock-paper-scissors game.
The game either runs normally with an empty string as move choices, or allows player to select their own moves.
The algorithm is as follows:
The next (half the length of list) moves beat the previous moves.

The game requires creating a rating.txt in root directory file to run.
"""

import random

RATING_FILE = "rating.txt"
REGULAR_CONDITIONS = {"rock": "paper", "paper": "scissors", "scissors": "rock"}


def get_player_input(player_choice, game_options) -> str:
    """Error checks players input and returns choice, !exit, or error"""
    if player_choice in game_options or player_choice in ["!exit", "!rating"]:
        return player_choice
    return "error"


def parse_game(player_choice, computer_choice, game_options) -> bool:
    """Will compare win conditions normally for regular options, otherwise use algorithm"""
    if len(game_options) == 3:
        return REGULAR_CONDITIONS[player_choice] != computer_choice
    count = 0
    for move in game_options:
        if move == player_choice:
            count += 1
            for _ in range(len(game_options) // 2):
                if count > len(game_options) - 1:
                    count = 0
                if computer_choice == game_options[count]:
                    return False
                count += 1
        count += 1
    return True


def get_computer_choice(game_options) -> str:
    """returns random key from game_options as computer choice"""
    return game_options[random.randint(0, len(game_options) - 1)]


def show_win(player_choice, computer_choice, result) -> str:
    """
    Compares player v computer choice against WIN_CONDITIONS
    Returns string notifying player of result
    """
    return (
        f"There is a draw ({player_choice})"
        if result == "draw"
        else (
            f"Well done. The computer chose {computer_choice} and failed"
            if result == "win"
            else f"Sorry, but the computer chose {computer_choice}"
        )
    )


def parse_match_score(player, player_choice, computer_choice, game_options) -> str:
    """checks win condition then calls a change of score"""
    if player_choice == computer_choice:
        change_score(player, 50)
        return "draw"
    else:
        if parse_game(player_choice, computer_choice, game_options):
            change_score(player, 100)
            return "win"
    return "loose"


def change_score(player, amount) -> None:
    """Updates player score"""
    with open(RATING_FILE, "r") as file:
        lines = file.readlines()

    for num, line in enumerate(lines):
        if line.startswith(player):
            score = int(line.split(" ")[1])
            score += amount
            lines[num] = f"{player} {score}\n"

    with open(RATING_FILE, "w") as file:
        file.writelines(lines)


def get_score(player) -> str:
    """Returns current player score"""
    rating = ""
    with open(RATING_FILE, "r") as file:
        for line in file:
            if line.startswith(player):
                rating = line.split(" ")[1]
    return f"Your rating: {rating}"


def create_new_player(player, file) -> str:
    """Adds player name and default score to rating file and returns entry"""
    entry = f"{player} 0\n"
    file.write(entry)
    return entry


def get_player(name) -> str:
    """Triggers creation of new player if player not found in rating file"""
    with open("rating.txt", "r+") as file:
        for line in file:
            if line.startswith(name):
                return line.strip()
        return create_new_player(name, file)


def main() -> None:
    """rock-paper-scissors game"""

    name = input("Enter your name: ")
    print(f"Hello, {name}")
    _ = get_player(name)  # creates players if missing
    game_options = list(input().split(","))
    if len(game_options) < 3:
        game_options = ["rock", "paper", "scissors"]
    print("okay, let's start.")
    while True:
        player_choice = get_player_input(input(), game_options)
        match player_choice:
            case "error":
                print("Invalid input")
            case "!rating":
                print(get_score(name))
            case "!exit":
                break
            case _:
                computer_choice = get_computer_choice(game_options)
                result = parse_match_score(
                    name, player_choice, computer_choice, game_options
                )
                print(show_win(player_choice, computer_choice, result))
    print("Bye!")


if __name__ == "__main__":
    main()
