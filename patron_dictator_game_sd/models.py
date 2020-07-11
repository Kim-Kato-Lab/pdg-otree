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
    name_in_url = 'patron_dictator_game'
    players_per_group = 3
    num_rounds = 1

    endowment = c(100)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    send = models.CurrencyField(
        min = 0, max = Constants.endowment
    )

    allocation = models.CurrencyField(
        min = 0
    )

    def allocation_max(self):
        return 2*self.send

    def set_payoffs(self):
        patron = self.get_player_by_role('patron')
        dictator = self.get_player_by_role('dictator')
        receiver = self.get_player_by_role('receiver')
        patron.payoff = Constants.endowment - self.send
        dictator.payoff = Constants.endowment - (self.allocation - self.send)
        receiver.payoff = self.allocation


class Player(BasePlayer):
    
    def role(self):
        if self.id_in_group == 1:
            return "patron"
        if self.id_in_group == 2:
            return "dictator"
        if self.id_in_group == 3:
            return "receiver"
