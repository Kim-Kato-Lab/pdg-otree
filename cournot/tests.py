from otree.api import Currency as cu, currency_range, expect
from . import *
from otree.api import Bot



class PlayerBot(Bot):

    cases = ['min', 'max']

    def play_round(self):
        yield Introduction

        if self.case == 'min':
            yield Decide, dict(units=0)
            # if player produces 0, nothing is sold and they make 0
            expect(self.player.payoff, cu(0))

        if self.case == 'max':
            yield Decide, dict(units=C.MAX_UNITS_PER_PLAYER)
            # if everyone produces max, price is driven to 0
            expect(self.player.payoff, cu(0))

        yield Results
