from otree.api import Currency as cu, currency_range, expect
from . import *
from otree.api import Bot



class PlayerBot(Bot):
    def play_round(self):
        yield Introduction
        yield Decision, dict(decision='Cooperate')
        expect('Both of you chose to Cooperate', 'in', self.html)
        expect(self.player.payoff, C.BOTH_COOPERATE_PAYOFF)
        yield Results
