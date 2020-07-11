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
    name_in_url = 'patron_dictator_game_fd'
    players_per_group = 3
    num_rounds = 1

    endowment = c(100)
    maximum_multiply = c(200)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    send = models.CurrencyField(
        min = 0, max = Constants.endowment
    )

    allocation = models.IntegerField(
        min = 0, max = Constants.maximum_multiply
    )

    def set_payoffs(self):
        patron = self.get_player_by_role('patron')
        dictator = self.get_player_by_role('dictator')
        receiver = self.get_player_by_role('receiver')
        patron.payoff = Constants.endowment - self.send
        dictator.payoff = Constants.endowment - (self.allocation/100 - 1) * self.send
        receiver.payoff = (self.allocation/100) * self.send


class Player(BasePlayer):
    
    def role(self):
        if self.id_in_group == 1:
            return "patron"
        if self.id_in_group == 2:
            return "dictator"
        if self.id_in_group == 3:
            return "receiver"
