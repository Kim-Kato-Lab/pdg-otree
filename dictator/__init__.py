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
    NUM_ROUNDS = 10
    ENDOWMENT = cu(100)
    PATRON_ROLE = "Patron"
    RECEIVER_ROLE = "Receiver"


class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
    subsession.group_randomly()

class Group(BaseGroup):
    send = models.IntegerField(min=0, max=C.ENDOWMENT)
    send_timeout = models.IntegerField()


class Player(BasePlayer):
    pass


# FUNCTIONS
def set_payoffs(group: Group):
    patron = group.get_player_by_role(C.PATRON_ROLE)
    receiver = group.get_player_by_role(C.RECEIVER_ROLE)
    patron.payoff = C.ENDOWMENT - group.send
    receiver.payoff = group.send


# PAGES
class WaitIntroduction(WaitPage):
    wait_for_all_groups = True
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class Introduction(Page):
    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config['timeout_seconds']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class Role(Page):
    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config['timeout_seconds']

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
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config['timeout_seconds']
    
    @staticmethod
    def js_vars(player: Player):
        return dict(
            current = player.round_number,
            max = C.NUM_ROUNDS
        )
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import random
        if timeout_happened:
            player.group.send = random.randint(0, C.ENDOWMENT)
            player.group.send_timeout = 1
        else:
            player.group.send_timeout = 0

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'

class Results(Page):

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config['timeout_seconds']

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
        round_list = list(range(1, C.NUM_ROUNDS + 1))
        
        if player.round_number == C.NUM_ROUNDS:
            selected_round = random.sample(round_list, 2)
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
    WaitIntroduction,
    Introduction,
    Role,
    WaitRoleCheck,
    Send,
    ResultsWaitPage,
    Results,
    ShuffleWaitPage
]
