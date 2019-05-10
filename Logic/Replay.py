from Logic.TextFunctions import *
from Logic.GetInput import *


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, new_path):
        self.newPath = os.path.expanduser(new_path)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def make_directory():
    user = os.getlogin()
    path = 'C:\\Users\\{}\\Documents\\Card Tournament'.format(user)
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(path+'\\Replays'):
        os.makedirs(path+'\\Replays')
    return path + '\\Replays'


def make_file(patch, lis=None):
    if lis is None:
        lis = []
    path = make_directory()
    with cd(path):
        x = 1
        while 1:                                                  # Find number for replay
            filename = 'Game {}.txt'.format(x)
            if os.access(os.path.join(path, filename), os.F_OK):
                x += 1
                continue
            else:
                text = ''
                text += '{}\n'.format(patch)
                for move in lis:
                    text += ','.join(move)
                    text += '\n'
                file = open(os.path.join(path, filename), 'w')
                file.write(text)
                file.close()
                break


def read_file(name):
    path = make_directory()
    with cd(path):
        file = open(os.path.join(path, name), 'r')
        string = file.readlines()
        lis = [x.strip() for x in string]
        file.close()
    return lis


def read_patch(name):
    path = make_directory()
    with cd(path):
        file = open(os.path.join(path, name), 'r')
        string = file.readline().split('\n')[0]
        file.close()
    return string


class Replay:
    def __init__(self):
        self.open = True
        self.path = make_directory()
        self.replays = None
        self.note = None
        self.return_value = None
        self.actions = dict()
        self.get_replays()

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
        if self.replays is not None:
            text += center_line('What replay would you like to watch?', width)
            text += full_line('-', width)
        if self.replays is not None:
            for i in range(len(self.replays)):
                text += '{}: {}'.format(i + 1, self.replays[i]).ljust(width)
        else:
            text += center_line('You have no saved replays, write return back to return to main menu', width)
        return text

    def get_replays(self):
        list_of_replays = list(x for x in os.listdir(self.path) if x.endswith(".txt"))
        if len(list_of_replays) > 0:
            for i in range(len(list_of_replays)):
                list_of_replays[i] = list_of_replays[i][:-4]
            self.replays = list_of_replays

    def set_available_inputs(self):
        self.actions['Exit Game'] = [['q', 'g'], ['qg'], ['exit', 'game']]
        self.actions['Return Back'] = [['r', 'b'], ['rb'], ['return', 'back']]
        self.actions['Watch Replay'] = [['w', 'r'], ['wr'], ['watch', 'replay']]

    def do(self, what_to_do, extra_info=None):
        if what_to_do == 'Exit Game':
            quit()
        if what_to_do == 'Return Back':
            self.open = False
        if what_to_do == 'Watch Replay':
            try:
                if 0 < int(extra_info) <= len(self.replays):
                    replay = 'Game {}.txt'.format(extra_info)
                    self.return_value = {'Goto': 'Game', 'Parameters': {'mode': 'Replay',
                                                                        'replay_moves': read_file(replay),
                                                                        'patch': read_patch(replay)}}
                    self.open = False
                else:
                    self.note = 'You have to write the number next to replay name to watch it'.format(len(self.replays))
            except (TypeError, ValueError):
                self.note = 'You have to write the number of replay you want to watch'
        else:
            self.note = 'You have written the unknown command! Try again!'

    def loop(self):
        while self.open:
            clear_screen()
            print(self)
            self.note = None
            input_list = get_input()
            possible_action = check_input(input_list, self.actions)
            self.do(possible_action, input_list[-1])
        return self.return_value
