from otree.api import *


doc = """
One player decides how to divide a certain amount between himself and the other
player.
See: Kahneman, Daniel, Jack L. Knetsch, and Richard H. Thaler. "Fairness
and the assumptions of economics." Journal of business (1986):
S285-S300.
"""


class C(BaseConstants):
    NAME_IN_URL = 'dictator'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 2
    ENDOWMENT = cu(100)
    PATRON_ROLE = "Patron"
    RECEIVER_ROLE = "Receiver"


class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
    subsession.group_randomly()

class Group(BaseGroup):
    send = models.IntegerField(min=0, max=C.ENDOWMENT)


class Player(BasePlayer):
    pass


# FUNCTIONS
def set_payoffs(group: Group):
    patron = group.get_player_by_role(C.PATRON_ROLE)
    receiver = group.get_player_by_role(C.RECEIVER_ROLE)
    patron.payoff = C.ENDOWMENT - group.send
    receiver.payoff = group.send


# PAGES
class Role(Page):
    @staticmethod
    def js_vars(player: Player):
        return dict(
            current = player.round_number,
            max = C.NUM_ROUNDS
        )

class WaitRoleCheck(WaitPage):
    body_text = """
    あなたのグループのメンバーが役割を確認しています。
    しばらくお待ちください。
    """
class Send(Page):
    form_model = 'group'
    form_fields = ['send']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.PATRON_ROLE
    
    @staticmethod
    def js_vars(player: Player):
        return dict(
            current = player.round_number,
            max = C.NUM_ROUNDS
        )

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'

class Results(Page):

    @staticmethod
    def js_vars(player: Player):
        return dict(
            current = player.round_number,
            max = C.NUM_ROUNDS
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import random
        participant = player.participant
        
        if player.round_number == C.NUM_ROUNDS:
            selected_round = []
            while len(selected_round) < 2:
                n = random.randint(1, C.NUM_ROUNDS)
                if not n in selected_round:
                    selected_round.append(n)
            participant.selected_round = selected_round
            each_realized_payoff = [float(player.in_round(n).payoff) for n in selected_round]
            realized_payoff = sum(each_realized_payoff)
            participant.payoff = realized_payoff

class ShuffleWaitPage(WaitPage):
    body_text = """
    他のグループのゲームの終了を待っています。
    しばらくお待ちください。
    """

    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession: Subsession):
        subsession.group_randomly()

page_sequence = [
    Role,
    WaitRoleCheck,
    Send,
    ResultsWaitPage,
    Results,
    ShuffleWaitPage
]
