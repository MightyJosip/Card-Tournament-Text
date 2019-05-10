from Logic.Constants import PLAYER


class Player:
    def __init__(self, number: int, name: str):
        self.number = number
        self.name = name
        self.max_hp = PLAYER['HP']
        self.hp = self.max_hp
        self.gold = PLAYER['GOLD']
        self.income = PLAYER['INCOME']
        self.current_income = self.income

    def __repr__(self) -> str:
        text = ''
        text += 'Player {}: HP: {} GOLD: {}'.format(self.name, self.hp, self.gold)
        return text

    def gold_income(self):
        self.gold += self.current_income
