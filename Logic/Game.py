from Logic.Constants import SETTINGS, PATCH, CARDS
from Logic.Player import Player
from Logic.Field import Field
from Cards import *
from Logic.TextFunctions import clear_screen, center_line, full_line
from Logic.GetInput import get_input, check_input
from Logic.Replay import make_file
from Logic.Patch import get_patch_info


class Game:
    def __init__(self, mode='Play', replay_moves=None, patch=PATCH):
        """ Set up players, variables, and start the game! """
        # Make objects
        player1_name = '1'
        player2_name = '2'
        self.player1 = Player(0, player1_name)  # Make first player, parameter is the name of the player
        self.player2 = Player(1, player2_name)  # Make second player
        self.field = Field()                    # Make field

        # Place for variables
        self.mode = mode
        self.patch = patch
        if self.patch != PATCH:
            self.patch_info = dict()
            self.fill_patch_info()
        else:
            self.patch_info = CARDS
        self.active_player = self.player1
        if mode == 'Play':
            self.moves = list()                 # Make list to store all played moves for replay
        self.actions = dict()                   # Make dictionary for all available commands
        self.actions_replay = dict()
        self.playing = True
        self.open = True
        self.note = None                        # Variable for message sent to user
        if replay_moves is not None:
            self.replay_moves = replay_moves
            self.line = 1

        # Initialization functions
        self.set_available_inputs()             # Set all commands
        self.set_field_player()                 # Connect field to the correct player

        # Game loop
        self.loop()                             # Start the game

    def __repr__(self) -> str:
        """ This method prints the field to the cmd. At the top it outputs note if there is one, then it goes through
            all lanes on the field and outputs cards on it. This method doesn't contain any stdout so you have to print
            it somewhere """
        text = ''
        width = SETTINGS['SCREEN_WIDTH']
        text += full_line('=', width)
        if self.note is not None:
            if self.note != 'Success':
                text += center_line(self.note, width)
                text += full_line('-', width)
            else:
                text += ' \n'
                text += full_line('-', width)
        else:
            text += ' \n'
            text += full_line('-', width)
        text += center_line('Player {} is on the turn'.format(self.active_player.name), width)
        text += full_line('-', width)
        text += str(self.player1) + str(self.player2).rjust(width - len(str(self.player1)))
        text += full_line('-', width)
        text += str(self.field)
        return text

    def set_field_player(self):
        for i in self.field.values[0]:
            i.player = self.player1
            i.position = self.field.values[0].index(i)
        for i in self.field.values[1]:
            i.player = self.player2
            i.position = self.field.values[1].index(i)

    def loop(self) -> None:
        """ Play the game; first refresh the screen, then get input and do something according to it """
        while self.open:
            clear_screen()
            print(self)
            self.note = None
            if self.mode == 'Play':
                input_list = get_input()
                possible_action = check_input(input_list, self.actions)
                self.do(possible_action, input_list[-1])
            if self.mode == 'Replay':
                try:
                    in_replay = self.replay_moves[self.line].split(',')
                    self.line += 1
                    input_list = get_input()
                    possible_action = check_input(input_list, self.actions_replay)
                    self.do_replay(possible_action, in_replay)
                except IndexError:
                    self.check_win_condition()

    def set_available_inputs(self) -> None:
        """ Put every command and inputs for it in a dictionary. The keys for dictionary is a description of the command
            and the value of the key is the list of lists off all available inputs for one command. this method doesn't
            have much use; it is only used in method called inputs where you use keys in this dictionary as the argument
            for the check input """
        self.actions['Quit Game'] = [['q', 'g'], ['qg'], ['quit', 'game']]
        self.actions['End Turn'] = [['e', 't'], ['et'], ['end', 'turn']]
        self.actions['Spawn Swordsman'] = [['s', 's'], ['ss'], ['spawn', 'swordsman']]

        self.actions_replay['Quit Game'] = [['q', 'g'], ['qg'], ['quit', 'game']]
        self.actions_replay['Quit Replay'] = [['q', 'r'], ['qr'], ['quit', 'replay']]
        self.actions_replay['Next Move'] = [['n', 'm'], ['nm'], ['next', 'move']]

    def do(self, what_to_do: str, extra_info=None) -> None:
        if what_to_do == 'Quit Game':
            quit()
        elif what_to_do == 'End Turn':
            if self.mode == 'Play':
                self.moves.append([what_to_do, extra_info])
            self.end_turn()
        elif what_to_do == 'Spawn Swordsman':
            try:
                self.note = self.field.spawn(Swordsman(self.patch_info['SWORDSMAN']), self.active_player,
                                             int(extra_info[0]) - 1)
            except (ValueError, IndexError):
                self.note = 'You have to write the number of the lane for the {}'.format(Swordsman(self.patch_info).
                                                                                         name)
        elif what_to_do == 'Spawn Archer':
            pass
        elif what_to_do == 'Spawn Wall':
            pass
        elif what_to_do == 'Use Heal':
            pass
        else:
            self.note = 'You have written the unknown command! Try again!'
        if self.note == 'Success' and self.mode == 'Play':
            self.moves.append([what_to_do, extra_info])

    def do_replay(self, what_to_do: str, extra_info=None) -> None:
        if what_to_do == 'Quit Game':
            quit()
        elif what_to_do == 'Quit Replay':
            self.open = False
        elif what_to_do == 'Next Move':
            self.do(extra_info[0], extra_info[1])
        else:
            self.line -= 1
            self.note = 'You have written the unknown command! Try again!'

    def end_turn(self) -> None:
        self.field.attack(self.active_player.number)
        self.check_win_condition()                    # Here we check if player has 0 hp
        self.active_player.gold_income()
        self.change_active_player()                   # This has to be at the end of the function

    def change_active_player(self) -> None:
        if self.active_player == self.player1:
            self.active_player = self.player2
        else:
            self.active_player = self.player1

    def check_win_condition(self):
        if self.player1.hp <= 0:
            self.what_to_do_if_victory(self.player2.name)
        elif self.player2.hp <= 0:
            self.what_to_do_if_victory(self.player1.name)

    def what_to_do_if_victory(self, who_won):
        if self.mode == 'Play':
            save_list = []
            for i in self.moves:
                save_list.append([i[0], ''.join(i[1])])
            make_file(self.patch, save_list)
            gg = EndGame(who_won)
            if gg.return_value == 'Main Menu':
                self.open = False
            elif gg.return_value == 'Play Again':
                self.restart_instance()
        elif self.mode == 'Replay':
            gg = EndGame(who_won, 'Replay')
            if gg.return_value == 'Main Menu':
                self.open = False
            elif gg.return_value == 'Restart Replay':
                self.restart_instance()

    def restart_instance(self):
        if self.mode == 'Play':
            self.__init__()
        if self.mode == 'Replay':
            self.__init__(mode='Replay', replay_moves=self.replay_moves, patch=self.patch)

    def fill_patch_info(self):
        self.patch_info = get_patch_info(self.patch)


class EndGame:
    def __init__(self, name, mode='Play'):
        self.actions = dict()
        self.mode = mode
        self.note = ''
        self.name_of_victory_player = name
        self.open = True
        self.actions = dict()
        self.return_value = ''

        self.set_available_inputs()
        self.loop()

    def __repr__(self):
        text = ''
        width = SETTINGS['SCREEN_WIDTH']
        text += full_line('=', width)
        if self.note is not None:
            text += center_line(self.note, width)
            text += full_line('-', width)
        else:
            text += ' \n'
            text += full_line('-', width)
        text += center_line('Player {} is victorious.'.format(self.name_of_victory_player), width)
        text += full_line('-', width)
        if self.mode == 'Play':
            text += center_line('Do you want to play again, return to main menu or quit game', width)
        else:
            text += center_line('Replay has ended. Write restart replay to watch replay again or exit replay', width)
        text += full_line('-', width)
        return text

    def set_available_inputs(self) -> None:
        """ Put every command and inputs for it in a dictionary. The keys for dictionary is a description of the command
            and the value of the key is the list of lists off all available inputs for one command. this method doesn't
            have much use; it is only used in method called inputs where you use keys in this dictionary as the argument
            for the check input """
        self.actions['Quit Game'] = [['q', 'g'], ['qg'], ['quit', 'game']]
        self.actions['Main Menu'] = [['m', 'm'], ['mm'], ['main', 'menu'], ['return', 'to', 'main', 'menu']]
        self.actions['Play Again'] = [['p', 'a'], ['pa'], ['play', 'again']]
        self.actions['Exit Replay'] = [['e', 'r'], ['er'], ['exit', 'replay']]
        self.actions['Restart Replay'] = [['r', 'r'], ['rr'], ['restart', 'replay']]

    def do(self, what_to_do: str) -> str:
        return_for_game = ''
        if self.mode == 'Play':
            if what_to_do == 'Quit Game':
                quit()
            elif what_to_do == 'Main Menu':
                return_for_game = 'Main Menu'
                self.open = False
            elif what_to_do == 'Play Again':
                return_for_game = 'Play Again'
                self.open = False
            else:
                self.note = 'You have written the unknown command! Try again!'
        if self.mode == 'Replay':
            if what_to_do == 'Quit Game':
                quit()
            if what_to_do == 'Exit Replay':
                return_for_game = 'Main Menu'
                self.open = False
            elif what_to_do == 'Restart Replay':
                return_for_game = 'Restart Replay'
                self.open = False
            else:
                self.note = 'You have written the unknown command! Try again!'
        return return_for_game

    def loop(self):
        return_value = ''
        while self.open:
            clear_screen()
            print(self)
            self.note = None                                         # Reset note after it has been printed
            input_list = get_input()                                 # Get the input
            possible_action = check_input(input_list, self.actions)  # Check if input given does something
            return_value = self.do(possible_action)                  # Do something according to the input
        self.return_value = return_value
