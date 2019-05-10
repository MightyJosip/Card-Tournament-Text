from Logic.TextFunctions import *
from Logic.GetInput import *
from Logic.Game import Game
from Logic.Settings import Settings
from Logic.Replay import Replay


class MenuBase:
    def __init__(self):
        self.running = True
        self.note = ''
        self.actions = dict()
        self.set_available_inputs()
        self.loop()

    def __repr__(self):
        text = ''
        width = SETTINGS['SCREEN_WIDTH']
        text += full_line('=', width)
        text += center_line('WELCOME TO THE CARD TOURNAMENT v{}'.format(PATCH), width)
        text += full_line('=', width)
        if self.note is not None:
            text += center_line(self.note, width)
            text += full_line('-', width)
        else:
            text += ' \n'
            text += full_line('-', width)
        text += center_line('Write one of the following options', width)
        text += full_line('-', width)
        return text

    def set_available_inputs(self):
        raise NotImplementedError("{} does not have set available inputs method".format(self.__class__.__name__))

    def do(self, what_to_do: str):
        raise NotImplementedError("{} does not have do method".format(self.__class__.__name__))

    def loop(self):
        while self.running:
            clear_screen()
            print(self)
            self.note = None  # Reset note after it has been printed
            input_list = get_input()  # Get the input
            possible_action = check_input(input_list, self.actions)
            self.do(possible_action)  # Do something according to the input
        del self


class MainMenu(MenuBase):
    def __repr__(self):
        text = super().__repr__()
        width = SETTINGS['SCREEN_WIDTH']
        text += center_line('Start Game', width)
        text += center_line('Watch Replay', width)
        text += center_line('Open Settings', width)
        text += center_line('Quit Game', width)
        return text

    def set_available_inputs(self) -> None:
        self.actions['Start Game'] = [['s', 'g'], ['sg'], ['start', 'game']]
        self.actions['Watch Replay'] = [['w', 'r'], ['wr'], ['watch', 'replay']]
        self.actions['Open Settings'] = [['o', 's'], ['os'], ['open', 'settings']]
        self.actions['Quit Game'] = [['q', 'g'], ['qg'], ['quit', 'game']]

    def do(self, what_to_do: str) -> None:
        if what_to_do == 'Start Game':
            Game()
        elif what_to_do == 'Watch Replay':
            possible_action = Replay().return_value
            if possible_action['Goto'] == 'Game':
                Game(**possible_action['Parameters'])
        elif what_to_do == 'Open Settings':
            Settings()
        elif what_to_do == 'Quit Game':
            quit()
        else:
            self.note = 'You have written the unknown command! Try again!'


class GameMenu(MenuBase):
    def __repr__(self):
        text = super().__repr__()
        width = SETTINGS['SCREEN_WIDTH']
        text += center_line('Play Single Player', width)
        text += center_line('Play Multi Player (Not implemented yet)', width)
        text += center_line('Return Back', width)
        return text

    def set_available_inputs(self) -> None:
        self.actions['Single Player'] = [['p', 's', 'p'], ['psp'], ['play', 'single', 'player']]
        self.actions['Multi Player'] = [['p', 'm', 'p'], ['pmp'], ['play', 'multi', 'player']]
        self.actions['Return Back'] = [['r', 'b'], ['rb'], ['return', 'back']]

    def do(self, what_to_do: str) -> None:
        if what_to_do == 'Single Player':
            Game()
        elif what_to_do == 'Multi Player':
            self.note = 'This is still not implemented'
        elif what_to_do == 'Return Back':
            self.running = False
        else:
            self.note = 'You have written the unknown command! Try again!'
