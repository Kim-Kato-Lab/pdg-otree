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
    maximum_allocate = c(2)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    send = models.CurrencyField(
        label = "Send money to Dictator",
        min = 0, max = Constants.endowment
    )

    allocation = models.FloatField(
        label = "Allocation rule determined by Dictator",
        min = 0, max = Constants.maximum_allocate
    )

    def set_payoffs(self):
        patron = self.get_player_by_role('patron')
        dictator = self.get_player_by_role('dictator')
        receiver = self.get_player_by_role('receiver')
        patron.payoff = Constants.endowment - self.send
        dictator.payoff = Constants.endowment - (1 - self.allocation) * self.send
        receiver.payoff = self.send * self.allocation


class Player(BasePlayer):

    send = models.CurrencyField()
    allocation = models.FloatField()
    
    def role(self):
        if self.id_in_group == 1:
            return "patron"
        if self.id_in_group == 2:
            return "dictator"
        if self.id_in_group == 3:
            return "receiver"
