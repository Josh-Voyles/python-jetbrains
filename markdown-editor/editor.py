"""
Module Name: Markdown Editor
Author: Josh Voyles
Created: 12 Oct 24

Description:
    A simple text editor that allows the user to format their text in markdown.
    This project is part of the Jet Brains Academy Python OOP Course Track.
"""


def show_formatters() -> str:
    """
    :return: A string listing the available text formatters, delimited by spaces.
    """
    return (
        "Available formatters: plain bold italic header "
        "link ordered-list unordered-list inline-code new-line"
    )


def show_commands() -> str:
    """
    :return: A string containing special commands '!help' and '!done'.
    """
    return "Special commands: !help !done"


def parse_command(command, text) -> str:
    """
    :return: If the command is "!help", it returns available commands.
             If the command is "!done", it returns "False" to trigger program exit.
             Return unknown or unrecognized commands.
    """
    match command:
        case "!help":
            return show_formatters() + "\n" + show_commands()
        case "!done":
            save_file(text)
            return "False"
        case _:
            return "Unknown formatting type or command"


def process_plain() -> str:
    """
    :return: The text input provided by the user.
    """
    return input("Text: ")


def process_bold() -> str:
    """
    :return: The input text wrapped in markdown bold format.
    """
    text = input("Text: ")
    return f"**{text}**"


def process_italic() -> str:
    """
    :return: A string with the input text enclosed in markdown asterisks.
    """
    text = input("Text: ")
    return f"*{text}*"


def process_header() -> str:
    """
    :return: Formatted header string with the specified level.
    """
    level = 0
    while level not in range(1, 6):
        level = int(input("Level: "))
        if level not in range(1, 6):
            print("The level should be within the range of 1 to 6")
    text = input("Text: ")
    return "#" * level + " " + text + "\n"


def process_link() -> str:
    """
    :return: A string containing the markdown-formatted link.
    """
    label = input("Label: ")
    url = input("URL: ")
    return f"[{label}]({url})"


def process_ordered_list() -> str:
    """
    :return: A formatted string representing a markdown ordered list.
    """
    rows = 0
    block = ""
    while not rows > 0:
        rows = int(input("Number of rows: "))
        if not rows > 0:
            print("The number of rows should be greater than zero")
    for i in range(rows):
        block += f"{i + 1}. " + input(f"Row #{i + 1}: ") + "\n"
    return block


def process_unordered_list() -> str:
    """
    :return: A string formatted as a markdown unordered list.
    """
    rows = 0
    block = ""
    while not rows > 0:
        rows = int(input("Number of rows: "))
        if not rows > 0:
            print("The number of rows should be greater than zero")
    for i in range(rows):
        block += "* " + input(f"Row #{i + 1}: ") + "\n"
    return block


def process_inline_code() -> str:
    """
    :return: The input text wrapped in inline code markdown formatting.
    """
    text = input("Text: ")
    return f"`{text}`"


def process_new_line() -> str:
    """
    :return: A string containing a newline character.
    """
    return "\n"


def save_file(text) -> None:
    """
    :param text: The text content to be written to the file.
    """
    with open("output.md", "w", encoding="utf-8") as file:
        file.write(text)
    file.close()


VALID_FORMAT = {
    "plain": process_plain,
    "bold": process_bold,
    "italic": process_italic,
    "header": process_header,
    "link": process_link,
    "inline-code": process_inline_code,
    "ordered-list": process_ordered_list,
    "unordered-list": process_unordered_list,
    "new-line": process_new_line,
}


def main() -> None:
    """
    Continuously prompts the user to choose a formatter or enter a command until the user chooses to exit the application.
    Processes and prints the formatted text or the results of the entered command.
    """
    sentence = ""
    proceed = "True"
    while proceed == "True":
        command = input("Choose a formatter: ")
        if command in VALID_FORMAT.keys():
            formatter = VALID_FORMAT[command]
            parse = formatter()
            if sentence != "" and sentence[-1] != "\n" and parse[0] == "#":
                sentence += "\n" + parse
            else:
                sentence += parse
            print(sentence)
        else:
            parse = parse_command(command, sentence)
            if not parse == "False":
                print(parse)
            else:
                proceed = parse


if __name__ == "__main__":
    main()
