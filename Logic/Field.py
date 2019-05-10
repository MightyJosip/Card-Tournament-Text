from Logic.Constants import SETTINGS
from Logic.Player import Player
from Cards.NoCard import NoCard, Card


class Field:
    def __init__(self, field_size: int = 5):
        self.field_size = field_size
        self.values = list()
        self.make_empty_field()

    def __repr__(self):
        text = ''
        for i in range(self.field_size):
            text += str(self.values[0][i]) + str(self.values[1][i]).rjust(SETTINGS['SCREEN_WIDTH'] -
                                                                          len(str(self.values[0][i])))
        return text

    def make_empty_field(self) -> None:
        self.values = [[NoCard() for i in range(self.field_size)] for j in range(2)]

    def spawn(self, card: Card, player: Player, position: int):
        if check_if_number_is_between_two_numbers(position, 0, self.field_size - 1):
            if isinstance(self.values[player.number][position], NoCard):
                if player.gold >= card.cost:
                    card.position = position
                    card.player = player
                    self.values[player.number][position] = card
                    player.gold -= card.cost
                    note = 'Success'
                else:
                    note = 'You must have {} gold to spawn {}, but you have {}'.format(card.cost, card.name,
                                                                                       player.gold)
            else:
                note = 'There is already a {} placed on that position'.format(self.values[player.number][position].name)
        else:
            note = 'You have to write the number between 1 and {} and you wrote {}!'.format(self.field_size,
                                                                                            position + 1)
        return note

    def use(self, card: Card, player: Player, position: int = None):
        if player.gold >= card.cost:
            card.player = player
            note = card.use()
            if note == '':
                player.gold -= card.cost
        else:
            note = 'You must have {} gold to use {}, but you have {}'.format(card.cost, card.name, player.gold)
        return note

    def attack(self, what_side_should_attack: int, who_attacks=-1):
        """ Who attacks is the parameter for deciding is the entire side of the board attacking or only specific card;
            -1 means that entire side is attacking or otherwise you have to write specific card for attack. """
        if who_attacks == -1:
            for i in self.values[what_side_should_attack]:
                i.attack(self)
                self.check_deaths()

    def check_deaths(self):
        for i in self.values:
            for j in i:
                try:
                    if j.hp <= 0:
                        new_empty_card = NoCard()
                        new_empty_card.player = j.player
                        new_empty_card.position = j.position
                        del j
                        self.values[new_empty_card.player.number][new_empty_card.position] = new_empty_card
                except AttributeError:
                    continue


def check_if_number_is_between_two_numbers(check_number: int, first_number: int, second_number: int) -> bool:
    if first_number < second_number:
        if first_number <= check_number <= second_number:
            return True
    else:
        if second_number <= check_number <= first_number:
            return True
    return False
