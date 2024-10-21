"""
This project has you build a basic regex engine.
Module Name: Regex Engine
Author: Josh Voyles
Created: 17 Oct 24

Description:
This project has you build a basic regex engine to understand how regex expressions work.
I used a recursive approach for most of the project.
"""


def parse_question(regex, string):
    """checks for optional character, strips regex or both"""
    if regex[0] in [string[0], "."]:
        return compare_strings(regex[2:], string[1:])
    return compare_strings(regex[2:], string)


def parse_asterisk(regex, string):
    """
    Regular expression pattern * for zero or more of preceding character.
    """
    if string and regex[0] in [string[0], "."]:
        return parse_asterisk(regex, string[1:])
    # if we eat the entire string because of "." wildcard
    if not string:
        return True
    return compare_strings(regex[2:], string)


def parse_plus(regex, string):
    """validates at least one instance of character, then parses as asterisk"""
    if regex[0] not in [string[0], "."]:
        return False
    regex = regex[:1] + "*" + regex[2:]
    return parse_asterisk(regex, string)


def compare_character(regex, string, period_literal=False):
    """Indicates if the first character of the string matches the given regular expression."""
    if period_literal:
        if regex[0] in [string[0]]:
            return compare_strings(regex[1:], string[1:])
    elif regex[0] in [string[0], "."]:
        return compare_strings(regex[1:], string[1:])
    return False


def is_match(regex, string):
    """Determines front, back, or general regex vs string match"""
    is_front_match = True
    is_back_match = True

    # empty values edge case
    if not regex:
        return True
    if not string:
        return False

    # note: project test cases don't account for ^ and $ meta characters as literals so they are stripped
    if regex[0] == "^":
        regex1 = regex.replace("^", "").replace("$", "")
        string1 = string
        is_front_match = compare_strings(regex1, string1)
    if regex[-1] == "$":
        regex2 = reverse_regex(regex.replace("^", "").replace("$", ""))
        is_back_match = compare_strings(regex2, string[::-1])

    if not is_front_match or not is_back_match:
        return False

    # general string vs regex matching
    regex = regex.replace("^", "").replace("$", "")
    matching = False

    while string and not matching:
        matching = compare_strings(regex, string)
        string = string[1:]
    return matching


def reverse_regex(regex):
    """Reverses order of regex input preserving wildcards for $ comparison."""
    reversed_regex = ""
    held_char = ""
    for char in regex[::-1]:
        if char in ["*", "+", "?", "\\"] and held_char != "\\":
            held_char = char
        elif held_char:
            reversed_regex += char + held_char
            held_char = ""
        else:
            reversed_regex += char
    return reversed_regex


def compare_strings(regex, string):
    """Matches regular expression against a string factoring wildcards."""
    if not regex:
        return True

    # factors espcape character
    if regex[0] == "\\":
        regex = regex[1:]
        if regex[0] == ".":
            return compare_character(regex, string, True)
        return compare_character(regex, string)

    if len(regex) > 1:
        match regex[1]:
            case "?":
                return parse_question(regex, string)
            case "*":
                return parse_asterisk(regex, string)
            case "+":
                return parse_plus(regex, string)
    return compare_character(regex, string)


def main():
    """Takes input from console regex|string and print T/F if match"""
    compare = input().split("|")
    regex = compare[0]
    string = compare[1]
    print(is_match(regex, string))


if __name__ == "__main__":
    main()
