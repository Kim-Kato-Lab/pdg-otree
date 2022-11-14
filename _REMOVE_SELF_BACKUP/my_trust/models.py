from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'my_trust'
    players_per_group = 2
    num_rounds = 1

    endowment = c(10)
    multiplication_factor = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    
    sent_amount = models.CurrencyField(
        label = "How much do you want to send to participant B?"
    )
    sentback_amount = models.CurrencyField(
        label = "How much do you want to send back?"
    )

    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p1.payoff = C.ENDOWMENT - self.sent_amount + self.sentback_amount
        p2.payoff = self.sent_amount * C.MULTIPLICATION_FACTOR - self.sentback_amount


class Player(BasePlayer):
    
    sent_amount = models.CurrencyField()
    sentback_amount = models.CurrencyField()

    def sentback_amount_choices(self):
        return currency_range(
            c(0),
            self.sent_amount*C.MULTIPLICATION_FACTOR,
            c(1)
        )
    
