from otree.api import *
import random

doc = """
This application provides a webpage instructing participants how to get paid.
Examples are given for the lab and Amazon Mechanical Turk (AMT).
"""


class C(BaseConstants):
    NAME_IN_URL = 'payment_info'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pickup_round1 = models.IntegerField()
    pickup_round2 = models.IntegerField()


# FUNCTIONS
# PAGES
class Introduction(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # select rounds for calculating payoff
        participant = player.participant
        payoff_list = participant.payoff_list
        round_list = list(range(len(payoff_list)))
        selected_round = random.sample(round_list, 2)
        participant.selected_round = selected_round
        player.pickup_round1 = selected_round[0] + 1
        player.pickup_round2 = selected_round[1] + 1

        # realized payoff
        each_realized_payoff = [float(payoff_list[n]) for n in selected_round]
        realized_payoff = sum(each_realized_payoff)
        participant.payoff = realized_payoff

class PaymentInfo(Page):
    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        payoff_list = participant.payoff_list
        selected_round = participant.selected_round
        row_color = ['table-default'] * len(payoff_list)
        for i in selected_round:
            row_color[i] = 'table-danger'

        return dict(
            table_item = zip(payoff_list, row_color),
            participation_fee = player.session.config['participation_fee'],
            realized_payoff = participant.payoff,
            p4p = participant.payoff.to_real_world_currency(player.session),
            get_money = participant.payoff_plus_participation_fee()
        )


page_sequence = [
    Introduction,
    PaymentInfo
]
