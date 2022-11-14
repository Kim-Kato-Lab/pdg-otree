from otree.api import *


doc = """
This is a one-shot "Prisoner's Dilemma". Two players are asked separately
whether they want to cooperate or defect. Their choices directly determine the
payoffs.
"""


class C(BaseConstants):
    NAME_IN_URL = 'prisoner'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    INSTRUCTIONS_TEMPLATE = 'prisoner/instructions.html'
    # payoff if 1 player defects and the other cooperates""",
    BETRAY_PAYOFF = cu(300)
    BETRAYED_PAYOFF = cu(0)
    # payoff if both players cooperate or both defect
    BOTH_COOPERATE_PAYOFF = cu(200)
    BOTH_DEFECT_PAYOFF = cu(100)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    decision = models.StringField(
        choices=[['Cooperate', 'Cooperate'], ['Defect', 'Defect']],
        doc="""This player's decision""",
        widget=widgets.RadioSelect,
    )


# FUNCTIONS
def set_payoffs(group: Group):
    for p in group.get_players():
        p.set_payoff()


def other_player(player: Player):
    return player.get_others_in_group()[0]


def set_payoff(player: Player):
    payoff_matrix = dict(
        Cooperate=dict(
            Cooperate=C.BOTH_COOPERATE_PAYOFF,
            Defect=C.BETRAYED_PAYOFF,
        ),
        Defect=dict(Cooperate=C.BETRAY_PAYOFF, Defect=C.BOTH_DEFECT_PAYOFF),
    )
    player.payoff = payoff_matrix[player.decision][other_player(player).decision]


# PAGES
class Introduction(Page):
    timeout_seconds = 100


class Decision(Page):
    form_model = 'player'
    form_fields = ['decision']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        me = player
        opponent = me.other_player()
        return dict(
            my_decision=me.decision,
            opponent_decision=opponent.decision,
            same_choice=me.decision == opponent.decision,
        )


page_sequence = [Introduction, Decision, ResultsWaitPage, Results]
