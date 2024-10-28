"""
Module Name: file-manager
Author: Josh Voyles
Created: 23 Oct 24

Description:
A simple file manager that allows you to perform CLI functions in a loop
"""

import os
import shutil
import re

# run the user's program in our generated folders
os.chdir("module/root_folder")
AVAILABLE_COMMANDS = ["pwd", "cd", "ls", "rm", "mv", "mkdir", "cp", "quit"]
EXTENSION_ONLY = re.compile("^\....$")


def human_size(b, units=None):
    """Returns a human-readable string representation of bytes"""
    if units is None:
        units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    return str(b) + units[0] if b < 1024 else human_size(b >> 10, units[1:])


def get_full_path() -> str:
    """returns full file path as a string"""
    return os.getcwd()


def change_directory(commands) -> str:
    """changes current directory"""
    try:
        os.chdir(commands[1])
        return os.path.basename(os.getcwd())
    except FileNotFoundError:
        return "Invalid path."


def list_directory(commands) -> list:
    """returns a list of files in directory, sorted by file type and alphabet"""
    files = os.listdir()
    files.sort()
    files.sort(key=os.path.isfile)
    if len(commands) > 1:
        match commands[1]:
            case "-l":
                return [f"{file} {os.stat(file).st_size}" for file in files]
            case "-lh":
                return [f"{file} {human_size(os.stat(file).st_size)}" for file in files]
    return files


def remove_all_files(commands) -> str:
    """if only extension provided, removes all files of type, else remove_file_directory"""
    if len(commands) == 1:
        return "Specify the file or directory"
    if not EXTENSION_ONLY.match(commands[1]):
        return remove_file_directory(commands)
    files = os.listdir()
    if not file_type_exists(files, commands[1]):
        return f"File extension {commands[1]} not found in this directory."
    for file in files:
        if file.endswith(commands[1]):
            remove_file_directory(["rm", file])
    return ""


def remove_file_directory(commands) -> str:
    """removes file or directory in current folder, returns empty string or error message"""
    try:
        if os.path.isfile(*commands[1:]):
            os.remove(*commands[1:])
        else:
            shutil.rmtree(*commands[1:])
        return ""
    except FileNotFoundError:
        return "No such file or directory"


def move_all_files(commands) -> str:
    """if only extension provided, moves all files of type to specified folder, else rename_file_directory"""
    if len(commands) != 3:
        return "Specify the current name of the file or directory and the new location and/or name"
    if not EXTENSION_ONLY.match(commands[1]):
        return rename_file_directory(commands)
    files = os.listdir()
    if not file_type_exists(files, commands[1]):
        return f"File extension {commands[1]} not found in this directory."
    new_location = os.listdir(commands[2])
    for file in files:
        if file.endswith(commands[1]):
            if file in new_location:
                if confirm_copy_over(file):
                    remove_file_directory(["rm", f"{commands[2]}/{file}"])
                    rename_file_directory(["mv", file, commands[2]])
            else:
                rename_file_directory(["mv", file, commands[2]])
    return ""


def rename_file_directory(commands) -> str:
    """renames files only in current folder or moves to another folder, returns empty string or error message"""
    try:
        if os.path.isfile(commands[2]):
            raise FileExistsError
        shutil.move(commands[1], commands[2])
        return ""
    except FileNotFoundError:
        return "No such file or directory"
    except FileExistsError:
        return "The file or directory already exists"


def copy_all_files(commands) -> str:
    """if only extension provided, copies all files of type to specified folder, else copy_file_to_directory"""
    if len(commands) == 1:
        return "Specify the file"
    if not EXTENSION_ONLY.match(commands[1]):
        return copy_file_to_directory(commands)
    files = os.listdir()
    if not file_type_exists(files, commands[1]):
        return f"File extension {commands[1]} not found in this directory."
    new_location = os.listdir(commands[2])
    for file in files:
        if file.endswith(commands[1]):
            if file in new_location:
                if confirm_copy_over(file):
                    remove_file_directory(["rm", f"{commands[2]}/{file}"])
                    copy_file_to_directory(["cp", file, commands[2]])
            else:
                copy_file_to_directory(["cp", file, commands[2]])
    return ""


def copy_file_to_directory(commands) -> str:
    """copies file in current folder, moves to new folder, returns empty string or error message"""
    if len(commands) != 3:
        return "Specify the current name of the file or directory and the new location and/or name"
    try:
        if not os.path.isfile(commands[2]):
            shutil.copy2(commands[1], commands[2])
        elif commands[1] in list_directory("ls"):
            raise FileExistsError
        shutil.move(commands[1], commands[2])
        return ""
    except FileNotFoundError:
        return "No such file or directory"
    except shutil.Error:
        return f"{commands[1]} already exists in this directory"


def confirm_copy_over(file) -> str:
    """confirmation copy or move files to new directory when file exists in new dir"""
    while True:
        print(f"{file} already exists in this directory. Replace? (y/n)")
        answer = input()
        if answer.lower() in ["y", "n"]:
            if answer.lower() == "y":
                return "yes"
            return ""


def make_directory(commands) -> str:
    """makes specified directory in current folder and returns empty string or error message"""
    if len(commands) != 2:
        return "Specify the name of the directory to be made"
    try:
        os.mkdir(commands[1])
        return ""
    except FileExistsError:
        return "The directory already exists"


def file_type_exists(files, file_ext) -> bool:
    """checks folder to verify that file type exists"""
    if any(file.endswith(file_ext) for file in files):
        return True
    return False


def main():
    print("Input the command\n")
    while True:
        command = input().strip()
        if command.startswith(tuple(AVAILABLE_COMMANDS)):
            if command.startswith("pwd"):
                print(get_full_path())
            elif command.startswith("cd"):
                print(change_directory(command.split(" ")))
            elif command.startswith("ls"):
                print(*list_directory(command.split(" ")), sep="\n")
            elif command.startswith("rm"):
                error = remove_all_files(command.split(" "))
                if error:
                    print(error)
            elif command.startswith("mv"):
                error = move_all_files(command.split(" "))
                if error:
                    print(error)
            elif command.startswith("mkdir"):
                error = make_directory(command.split(" "))
                if error:
                    print(error)
            elif command.startswith("cp"):
                error = copy_all_files(command.split(" "))
                if error:
                    print(error)
            elif command.startswith("quit"):
                exit()
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
