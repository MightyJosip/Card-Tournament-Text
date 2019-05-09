from configparser import *
from Logic.GetInput import *
from Logic.TextFunctions import *
from Logic.Constants import DEFAULT_SETTINGS, SETTINGS


def set_screen_size(width: int, height: int):
    os.system('mode con: cols={} lines={}'.format(width, height))


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, new_path):
        self.newPath = os.path.expanduser(new_path)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


class SettingsBase:
    def __init__(self):
        self.path = ''
        self.file_path = ''
        self.file = None
        self.just_made = False
        self.values = dict()
        self.config = ConfigParser()

    def make_directory(self):
        raise NotImplementedError()

    def make_file(self):
        self.make_directory()
        with cd(self.path):
            if not os.path.exists(os.path.join(self.path, 'Settings.ini')):
                self.just_made = True
            self.file_path = os.path.join(self.path, 'Settings.ini')
            self.file = open(self.file_path, 'a')

    def read_values(self):
        file_read = open(self.file_path, 'r')
        file_read.close()
        self.config.read(self.file_path)
        self.values['SCREEN_WIDTH'] = self.config.getint('Terminal', 'SCREEN_WIDTH')
        self.values['SCREEN_HEIGHT'] = self.config.getint('Terminal', 'SCREEN_HEIGHT')
        SETTINGS['SCREEN_WIDTH'] = self.config.getint('Terminal', 'SCREEN_WIDTH')
        SETTINGS['SCREEN_HEIGHT'] = self.config.getint('Terminal', 'SCREEN_HEIGHT')


class SettingsBasic(SettingsBase):
    def __init__(self):
        super().__init__()
        # Methods
        self.setup_variables()

    def make_directory(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
            self.just_made = True

    def make_file(self):
        self.make_directory()
        with cd(self.path):
            if not os.path.exists(os.path.join(self.path, 'Settings.ini')):
                self.just_made = True
            self.file_path = os.path.join(self.path, 'Settings.ini')
            self.file = open(self.file_path, 'a')

    def setup_variables(self):
        user = os.getlogin()
        self.path = 'C:\\Users\\{}\\Documents\\Card Tournament'.format(user)
        if not os.path.exists(os.path.join(self.path, 'Settings.ini')):
            self.just_made = True
        if self.just_made:
            self.values = DEFAULT_SETTINGS
        else:
            self.file_path = os.path.join(self.path, 'Settings.ini')
            self.read_values()


class Settings(SettingsBase):
    def __init__(self):
        super().__init__()
        # Attributes
        self.open = True
        self.note = None
        self.values = dict()
        self.new_values = dict()
        self.actions = dict()
        self.return_mode = False
        # Methods
        self.setup()
        self.set_available_inputs()
        # Run
        self.loop()

    def __repr__(self):
        text = ''
        width = self.values['SCREEN_WIDTH']
        text += full_line('=', width)
        if self.note is not None:
            text += center_line(self.note, width)
            text += full_line('-', width)
        else:
            text += ' \n'
            text += full_line('-', width)
        text += center_line('SETTINGS', width)
        text += full_line('-', width)
        for key in self.values:
            if self.new_values[key] is None:
                text += '{}: {}'.format(key.replace('_', ' ').ljust(len(max(self.values.keys(), key=len)) + 1),
                                        self.values[key]).ljust(self.values['SCREEN_WIDTH'])
            else:
                text += '{}: {} * CHANGED (OLD {})'.format(key.replace('_', ' ')
                                                           .ljust(len(max(self.values.keys(), key=len)) + 1),
                                                           self.new_values[key],
                                                           self.values[key]).ljust(self.values['SCREEN_WIDTH'])
        text += full_line('-', width)
        text += center_line('Write modify setting + name of setting + new value to change setting', width)
        text += center_line('Write save changes to save changes', width)
        text += center_line('Write return to discard changes', width)
        text += center_line('Write exit game to exit the game', width)
        return text

    def loop(self):
        while self.open:
            clear_screen()
            print(self)
            self.note = None
            input_list = get_input()
            possible_action = check_input(input_list, self.actions)
            self.do(possible_action, input_list[-1])  # Do something according to the input

    def set_available_inputs(self):
        self.actions['Modify Setting Width'] = [['m', 's', 'w'], ['msw'], ['modify', 'settings', 'width']]
        self.actions['Modify Setting Height'] = [['m', 's', 'h'], ['msh'], ['modify', 'settings', 'height']]
        self.actions['Save Changes'] = [['s', 'c'], ['sc'], ['save', 'changes']]
        self.actions['Return'] = [['r'], ['return']]
        self.actions['Return Save'] = [['y'], ['yes']]
        self.actions['Return No Save'] = [['n'], ['no']]
        self.actions['Exit Game'] = [['eg'], ['exit']]

    def do(self, what_to_do, extra_info=None):
        if what_to_do == 'Exit game':
            self.open = False
            quit()
        if not self.return_mode:
            if what_to_do == 'Modify Setting Width':
                try:
                    if 80 <= int(extra_info) <= 200:
                        if int(extra_info) != self.values['SCREEN_WIDTH']:
                            self.new_values['SCREEN_WIDTH'] = int(extra_info)
                        elif int(extra_info) == self.values['SCREEN_WIDTH'] and self.new_values['SCREEN_WIDTH'] is not None:
                            self.new_values['SCREEN_WIDTH'] = None
                    else:
                        self.note = 'You have to write a number between 80 and 200 for width'
                except ValueError:
                    self.note = 'You have to write a number for screen width'
            elif what_to_do == 'Modify Setting Height':
                try:
                    if 20 <= int(extra_info) <= 80:
                        if int(extra_info) != self.values['SCREEN_HEIGHT']:
                            self.new_values['SCREEN_HEIGHT'] = int(extra_info)
                        elif int(extra_info) == self.values['SCREEN_HEIGHT'] and self.new_values['SCREEN_HEIGHT'] is not\
                                None:
                            self.new_values['SCREEN_HEIGHT'] = None
                    else:
                        self.note = 'You have to write a number between 20 and 80 for height'
                except ValueError:
                    self.note = 'You have to write a number for screen height'
            elif what_to_do == 'Save Changes':
                self.save_changes()
                self.setup_variables()
            elif what_to_do == 'Return':
                changed = False
                for values in list(self.new_values.values()):
                    if values is not None:
                        changed = True
                if not changed:
                    self.open = False
                else:
                    self.note = 'Write y to save changes or n to discard changes'
                    self.return_mode = True
            else:
                self.note = 'You have written the unknown command! Try again!'
        else:
            if what_to_do == 'Return Save':
                self.save_changes()
                self.open = False
            elif what_to_do == 'Return No Save':
                self.open = False
            else:
                self.note = 'You wrote unknown command. Write y to save changes or n to discard changes'

    def make_directory(self):
        user = os.getlogin()
        self.path = 'C:\\Users\\{}\\Documents\\Card Tournament'.format(user)
        if not os.path.exists(self.path):
            os.makedirs(self.path)
            self.just_made = True

    def setup_variables(self):
        for key in DEFAULT_SETTINGS:
            self.new_values[key] = None
        if self.just_made:
            self.values = DEFAULT_SETTINGS
            self.save_to_file()
        else:
            self.read_values()
        set_screen_size(self.values['SCREEN_WIDTH'], self.values['SCREEN_HEIGHT'])

    def setup(self):
        self.make_directory()
        self.make_file()
        self.setup_variables()

    def change_value(self, section, option, value):
        self.config.read(self.file_path)
        self.config.set(section, option, value)
        with open(self.file_path, 'w') as configfile:
            self.config.write(configfile)

    def save_changes(self):
        for key in self.new_values:
            if self.new_values[key] is not None:
                self.change_value('Terminal', key, str(self.new_values[key]))

    def save_to_file(self):
        self.config.read(self.file_path)
        for key in self.values:
            try:
                self.config.set('Terminal', key, str(self.values[key]))
            except NoSectionError:
                self.config.add_section('Terminal')
                self.config.set('Terminal', key, str(self.values[key]))
        with self.file as configfile:
            self.config.write(configfile)

