import random  # import example, we will use random module to generate pseudo-random number


def main():
    friend_dict = {}  # init dictionary of friends (friend name : share of bill)

    print("How many people will be joining?")

    num_of_people = int(input())  # test cases will only be zero or less

    if num_of_people <= 0:  # for this exercise, we only have to check for integers zero or less
        print("No one is joining for the party")
        exit()  # simple exit game

    print("Enter the name of every friend (including you), each on a new line:")

    friends = [input() for _ in range(num_of_people)]  # list comprehension example

    print("Enter the total bill value:")

    bill = float(input())  # bill as a float w/o error checking

    print("Do you want to use the \"Who is lucky?\" feature? Write Yes/No:")

    if input().lower() != 'yes':  # account for any case yes answer with .lower()
        print("No one is going to be lucky")
        for friend in friends:  # for loop example
            friend_dict[friend] = round((bill / num_of_people), 2)  # divide bill between all party members
        print(friend_dict)  # print friends with their respective bill totals
        exit()  # simple exit game

    lucky_friend = friends[random.randint(0, num_of_people - 1)]  # randomly selects friend list index

    for friend in friends:  # for loop example
        if friend != lucky_friend:  # if you're not lucky, you're paying more
            friend_dict[friend] = round((bill / (num_of_people - 1)), 2)  # divide bill between remaining friends
        else:
            friend_dict[friend] = 0  # lucky friend gets free meal

    print(f"{lucky_friend} is the lucky one!")  # f-string example

    print(friend_dict)  # print friends with their respective bill totals


if __name__ == '__main__':
    main()
