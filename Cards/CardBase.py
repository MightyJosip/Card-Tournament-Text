from Logic.Player import Player
from math import floor, ceil


class Card:
    def __init__(self, name, position=None, player: Player = -1, cost=None, hp=None, ad=None, effect_value=None,
                 first_turn=True, attack_target: list = '', effect_target='', attack_type: list = '', effect_type='',
                 bonuses: dict = '', applying: dict = None, can_be_targeted=True):
        self.name = name
        if position is not None:
            self.position = position
        if not player == -1:
            self.player = player
        if cost is not None:
            self.cost = cost
        if hp is not None:
            self.hp = hp
        if ad is not None:
            self.ad = ad
        if effect_value is not None:
            self.effect_value = effect_value
        if applying is not None:
            self.applying = applying
        self.attack_type = attack_type
        self.attack_target = attack_target
        self.bonuses = bonuses
        self.effect_target = effect_target
        self.effect_type = effect_type
        self.first_turn = first_turn
        self.can_be_targeted = can_be_targeted

    def __repr__(self) -> str:
        text = ''
        if self.name == 'Empty':
            return 'Empty'
        text += self.name
        if hasattr(self, 'hp'):
            text += ' HP:{}'.format(self.hp)
        if hasattr(self, 'ad'):
            text += ' AD:{}'.format(self.ad)
        if self.first_turn and hasattr(self, 'ad'):
            text += ' FT'
        return text

    def find_target(self, field) -> list:
        targets = []
        enemy_player_number = get_enemy_player(self.player.number)
        if 'Same position' in self.attack_target:
            target = field.values[enemy_player_number][self.position]
            targets.append(target)
        return targets

    def attack(self, field):
        if not self.first_turn:
            targets = self.find_target(field)
            for target in targets:
                if 'Normal' in self.attack_type:
                    if target.can_be_targeted:
                        target.hp -= self.ad
                    else:
                        target.player.hp -= self.ad
                if 'Pierce' in self.attack_type:
                    if target.can_be_targeted:
                        percent = float(self.attack_type[self.attack_type.index('Pierce') + 1])
                        target.hp -= self.ad
                        target.player.hp -= percentage_calculation(self.ad, percent)
                    else:
                        target.player.hp -= self.ad
        else:
            self.first_turn = False

    def use(self):
        who = None
        note = ''
        # Target
        if self.effect_target == 'Player':
            who = self.player
        # Effect
        if self.effect_type == 'Heal':
            if who.hp < who.max_hp:
                if self.effect_value + who.hp < who.max_hp:
                    who.hp += self.effect_value
                else:
                    who.hp = who.max_hp
            else:
                note = 'The target is already at full health'
        return note


def percentage_calculation(value: int, percentage: float, floor_or_ceil='floor') -> int:
    return floor(value * percentage) if floor_or_ceil == 'floor' else ceil(value * percentage)


def get_enemy_player(my_player: int):
    return 0 if my_player else 1
