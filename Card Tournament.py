from Logic import *


def do_before_running_the_program() -> None:
    """
This function is called once when the program starts and it is used to load data/setup global variables etc.
    """
    settings = SettingsBasic()
    settings.setup_variables()
    for keys in settings.values:
        SETTINGS[keys] = settings.values[keys]
    set_screen_size(SETTINGS['SCREEN_WIDTH'], SETTINGS['SCREEN_HEIGHT'])


def main() -> None:
    """
Main function of the game, first it calls do_before, and then the game starts from main menu
    """
    do_before_running_the_program()
    MainMenu()


if __name__ == '__main__':
    main()
