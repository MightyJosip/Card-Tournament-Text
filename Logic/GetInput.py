from typing import List, Dict
from Logic.Constants import *


def get_input() -> List[str]:
    print('-' * SETTINGS['SCREEN_WIDTH'])
    string = input('Your input: ')
    list_of_strings = [word.lower() for word in string.split()]
    return list_of_strings


def check_input(input_list: List[str], dict_of_actions: Dict[str, List[List[str]]]) -> str:
    result = None
    for action, commands in dict_of_actions.items():
        if result is None:
            for command in commands:
                command_true = True
                for word_index in range(len(command)):
                    if not command[word_index] == input_list[word_index]:
                        command_true = False
                        break
                if command_true:
                    result = action
                    break
        else:
            break
    return result
