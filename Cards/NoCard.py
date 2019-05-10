from Cards.CardBase import Card


class NoCard(Card):
    def __init__(self):
        super().__init__(name='Empty', can_be_targeted=False)
