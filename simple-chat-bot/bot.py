def greet(bot_name, birth_year) -> None:
    """
    Demonstrates print with concatenating function parameters
    :param bot_name: programmer defined bot name
    :param birth_year: programmer defined bot birthdate
    :return:
    """
    print('Hello! My name is ' + bot_name + '.')
    print('I was created in ' + birth_year + '.')


def remind_name() -> None:
    """
    Demonstrate concatenate with input()
    :return: no return value
    """
    print('Please, remind me your name.')
    print('What a great name you have, ' + input() + '!')


def guess_age() -> None:
    """
    Demonstrates some math and casting
    :return: no return value
    """
    print('Let me guess your age.')
    print('Enter remainders of dividing your age by 3, 5 and 7.')

    # remainders entered on each line
    rem3 = int(input())
    rem5 = int(input())
    rem7 = int(input())
    age = (rem3 * 70 + rem5 * 21 + rem7 * 15) % 105

    # cast int to String
    print("Your age is " + str(age) + "; that's a good time to start programming!")


def count() -> None:
    """
    Demonstrates casting to int and while loop
    :return: no return value
    """
    print('Now I will prove to you that I can count to any number you want.')

    num = int(input())  # will throw exception if number is not entered. Unchecked.
    curr = 0
    while curr <= num:
        print(curr, '!')
        curr = curr + 1


def test() -> None:
    """
    Demonstrates text blocks, boolean, returning values
    :return:
    """
    print("Let's test your programming knowledge.\n"  # contains new line character
          "What type of parameter can you NOT pass in a Java method?")

    # text block
    print("""
1. Object
2. char
3. Integer
4. Pointer
    """)

    # assigning boolean value false
    proceed = False

    # confirming we want "false" value with not keyword
    while not proceed:
        proceed = check_answer(input())


def check_answer(answer) -> bool:
    """
    Demonstrates proper if statement and return values
    :param answer: users quiz answer as string
    :return: false if answer is incorrect, otherwise true
    """
    if answer != "4":
        print("Please, try again.")
        return False
    return True


def end() -> None:
    """
    Simple exit message
    :return: no return values
    """
    print('Congratulations, have a nice day!')


def main() -> None:
    """
    Main method takes you through the game.
    :return: No return value
    """

    greet('Josh', '1842')  # greeting with two String parameters
    remind_name()  # enter name, have robot spit it back
    guess_age()  # guess age using fancy math
    count()  # enter number you want robot to count to
    test()  # Java quiz
    end()  # final congrats


if __name__ == '__main__':
    main()
