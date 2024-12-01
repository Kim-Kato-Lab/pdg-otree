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
        pp = player.participant
        payoff_list = pp.payoff_list
        belief_payoff_list = pp.belief_payoff_list
        round_with_belief = [index for index, value in enumerate(belief_payoff_list) if value is not None]
        round_without_belief = [index for index, value in enumerate(belief_payoff_list) if value is None]
        selected_round = [
            random.sample(round_with_belief, 1)[0],
            random.sample(round_without_belief, 1)[0]
        ]
        pp.selected_round = selected_round
        player.pickup_round1 = selected_round[0] + 1
        player.pickup_round2 = selected_round[1] + 1

        # realized payoff
        realized_payoff = payoff_list[selected_round[0]] + payoff_list[selected_round[1]]
        pp.payoff = realized_payoff

class PaymentInfo(Page):
    @staticmethod
    def vars_for_template(player: Player):
        pp = player.participant
        payoff_list = pp.payoff_list
        game_payoff_list = pp.game_payoff_list
        belief_payoff_list = pp.belief_payoff_list
        selected_round = pp.selected_round
        row_color = ['table-default'] * len(payoff_list)
        for i in selected_round:
            row_color[i] = 'table-danger'

        return dict(
            table_item = zip(game_payoff_list, belief_payoff_list, payoff_list, row_color),
            participation_fee = player.session.config['participation_fee'],
            realized_payoff = pp.payoff,
            p4p = pp.payoff.to_real_world_currency(player.session),
            get_money = pp.payoff_plus_participation_fee()
        )


page_sequence = [
    Introduction,
    PaymentInfo
]
