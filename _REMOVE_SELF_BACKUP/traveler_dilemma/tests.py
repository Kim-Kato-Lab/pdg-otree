from otree.api import Currency as c, currency_range, expect
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    cases = ['both_min', 'both_max', 'p1_lower']

    def play_round(self):
        case = self.case

        # start game
        yield pages.Introduction

        if case == 'both_min':
            yield pages.Claim, dict(claim=C.MIN_AMOUNT)
            expect(self.player.payoff, C.MIN_AMOUNT)
        elif case == 'both_max':
            yield pages.Claim, dict(claim=C.MAX_AMOUNT)
            expect(self.player.payoff, C.MAX_AMOUNT)
        else:
            if self.player.id_in_group == 1:
                yield pages.Claim, dict(claim=C.MIN_AMOUNT)
                expect(self.player.payoff, C.MIN_AMOUNT + 2)
            else:
                yield pages.Claim, dict(claim=C.MIN_AMOUNT + 1)
                expect(self.player.payoff, C.MIN_AMOUNT - 2)

        yield pages.Results
