from otree.api import *


doc = """
A demo of how rounds work in oTree, in the context of 'matching pennies'
"""


class C(BaseConstants):
    NAME_IN_URL = 'matching_pennies'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 4
    STAKES = cu(100)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    penny_side = models.StringField(
        choices=[['Heads', 'Heads'], ['Tails', 'Tails']], widget=widgets.RadioSelect
    )
    is_winner = models.BooleanField()


# FUNCTIONS
def creating_session(subsession: Subsession):
    import random

    if subsession.round_number == 1:
        paying_round = random.randint(1, C.NUM_ROUNDS)
        subsession.session.vars['paying_round'] = paying_round
    if subsession.round_number == 3:
        # reverse the roles
        matrix = subsession.get_group_matrix()
        for row in matrix:
            row.reverse()
        subsession.set_group_matrix(matrix)
    if subsession.round_number > 3:
        subsession.group_like_round(3)


def set_payoffs(group: Group):
    matcher = group.get_player_by_role('Matcher')
    mismatcher = group.get_player_by_role('Mismatcher')
    if matcher.penny_side == mismatcher.penny_side:
        matcher.is_winner = True
        mismatcher.is_winner = False
    else:
        matcher.is_winner = False
        mismatcher.is_winner = True
    for player in [mismatcher, matcher]:
        if group.subsession.round_number == group.session.vars['paying_round'] and player.is_winner:
            player.payoff = C.STAKES
        else:
            player.payoff = cu(0)


def role(player: Player):
    if player.id_in_group == 1:
        return 'Mismatcher'
    if player.id_in_group == 2:
        return 'Matcher'


# PAGES
class Choice(Page):
    form_model = 'player'
    form_fields = ['penny_side']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(player_in_previous_rounds=player.in_previous_rounds())


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class ResultsSummary(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        player_in_all_rounds = player.in_all_rounds()
        return dict(
            total_payoff=sum([p.payoff for p in player_in_all_rounds]),
            paying_round=player.session.vars['paying_round'],
            player_in_all_rounds=player_in_all_rounds,
        )


page_sequence = [Choice, ResultsWaitPage, ResultsSummary]
