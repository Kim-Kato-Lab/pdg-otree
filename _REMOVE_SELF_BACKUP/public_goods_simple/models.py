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


class Constants(BaseConstants):
    name_in_url = 'public_goods_simple'
    players_per_group = 3
    num_rounds = 1

    endowment = c(100)
    multiplier = 1.8


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()

    def set_payoffs(self):
        players = self.get_players()
        contributions = [p.contribution for p in players]
        self.total_contribution = sum(contributions)
        self.individual_share = (
            self.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP
        )
        for p in players:
            p.payoff = C.ENDOWMENT - p.contribution + self.individual_share


class Player(BasePlayer):
    contribution = models.CurrencyField(min=0, max=C.ENDOWMENT)
