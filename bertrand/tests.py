from otree.api import Currency as cu, currency_range, expect
from . import *
from otree.api import Bot



class PlayerBot(Bot):
    def play_round(self):
        # compete price
        yield Introduction
        yield Decide, dict(price=cu(30))
        yield Results
