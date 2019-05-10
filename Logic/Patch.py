import os
import numpy as np


def patch_info():
    patches = {'1.0.0': {'SWORDSMAN': {'cost': 2, 'hp': 8, 'ad': 2, 'attack_type': 'Normal',
                                       'attack_target': 'Same position'},
                         'ARCHER': {'cost': 5, 'hp': 10, 'ad': 4, 'attack_type': ['Pierce', 0.5],
                                    'attack_target': 'Same position'},
                         'HEAL': {'cost': 5, 'effect_value': 4, 'effect_type': 'Heal', 'effect_target': 'Player'}
                         }
               }
    return patches


def make_directory():
    user = os.getlogin()
    path = 'C:\\Users\\{}\\Documents\\Card Tournament\\Old Patch Info'.format(user)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def save_patch_info(patch, info):
    user = os.getlogin()
    patch = patch.replace('.', '_')
    path = 'C:\\Users\\{}\\Documents\\Card Tournament\\Old Patch Info\\Patch {}'.format(user, patch)
    try:
        np.save(path, info)
    except FileNotFoundError:
        make_directory()
        np.save(path, info)


def save_everything(dict_of_patches):
    user = os.getlogin()
    for key in dict_of_patches:
        patch = key.replace('.', '_')
        path = 'C:\\Users\\{}\\Documents\\Card Tournament\\Old Patch Info\\Patch {}'.format(user, patch)
        if not os.path.isfile(path):
            save_patch_info(key, dict_of_patches[key])


def capitalize_keys(dictionary: dict) -> dict:
    result = dict()
    for key in dictionary:
        upper_key = key.upper()
        result[upper_key] = dictionary[key]
    return result


def get_patch_info(patch):
    save_everything(patch_info())
    user = os.getlogin()
    patch = patch.replace('.', '_')
    path = 'C:\\Users\\{}\\Documents\\Card Tournament\\Old Patch Info\\Patch {}'.format(user, patch)
    info = np.load('{}.npy'.format(path)).item()
    # noinspection PyTypeChecker
    info = capitalize_keys(info)
    return info
