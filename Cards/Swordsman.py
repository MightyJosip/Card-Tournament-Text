from Cards.CardBase import Card


class Swordsman(Card):
    def __init__(self, stats):
        super().__init__(name='Swordsman')
        for attribute in stats:
            setattr(self, attribute, stats[attribute])  # Set all attributes from the dictionary
