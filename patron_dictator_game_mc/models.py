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
    name_in_url = 'patron_dictator_game_mc'
    players_per_group = 3
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    movement = models.BooleanField(
        choices = [
            [False, "Second"],
            [True, "First"]
        ]
    )

class Player(BasePlayer):
    
    def role(self):
        if self.id_in_group == 1:
            return "patron"
        if self.id_in_group == 2:
            return "dictator"
        if self.id_in_group == 3:
            return "receiver"
