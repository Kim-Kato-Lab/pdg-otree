from otree.api import *


author = 'Hiroki Kato'
doc = """
This is the patron-dictator game,
which reflects an asymmetric information in that 
it is difficult for donors to know in advance
the extent to which their donations improve recipients' welfare.

Registration citation:
Kato, Hiroki and Youngrok Kim. 2022. "Patron-Dictator Game: Strategic Interaction between Charities and Donors."
AEA RCT Registry. December 13. https://doi.org/10.1257/rct.10594-1.0
"""


class C(BaseConstants):
    NAME_IN_URL = 'patron_dictator_game'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 10
    ENDOWMENT = cu(100)
    MAXIMUM_MULTIPLY = 200
    PATRON_ROLE = "Patron"
    DICTATOR_ROLE = "Dictator"
    RECEIVER_ROLE = "Receiver"


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    subsession.group_randomly()

    for g in subsession.get_groups():
        g.dictator_first = subsession.session.config['first_moving_dictator']
        print('First-Moving Dictator: ', g.dictator_first)

class Group(BaseGroup):
    send = models.IntegerField(min=0, max=C.ENDOWMENT)
    allocation = models.IntegerField(min=0, max=C.MAXIMUM_MULTIPLY)
    send_timeout = models.IntegerField()
    allocation_timeout = models.IntegerField()
    dictator_first = models.BooleanField()


class Player(BasePlayer):
    pass


# FUNCTIONS
def set_payoffs(group: Group):
    patron = group.get_player_by_role(C.PATRON_ROLE)
    dictator = group.get_player_by_role(C.DICTATOR_ROLE)
    receiver = group.get_player_by_role(C.RECEIVER_ROLE)
    patron.payoff = C.ENDOWMENT - group.send
    dictator.payoff = C.ENDOWMENT - (group.allocation / 100 - 1) * group.send
    receiver.payoff = (group.allocation / 100) * group.send

# PAGES
class WaitIntroduction(WaitPage):
    wait_for_all_groups = True
    
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
    あなたのグループの他の参加者が役割を確認しています。
    しばらくお待ちください。
    """

class FirstMover(Page):
    form_model = 'group'

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config['timeout_seconds']
    
    @staticmethod
    def get_form_fields(player: Player):
        group = player.group
        if group.dictator_first == True:
            return ['allocation']
        else:
            return ['send']

    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        if group.dictator_first == True:
            return player.role == C.DICTATOR_ROLE
        else:
            return player.role == C.PATRON_ROLE
    
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        if group.dictator_first == True:
            return dict(role = 'メンバーＤ')
        else:
            return dict(role = 'メンバーＰ')
    
    @staticmethod
    def js_vars(player: Player):
        return dict(
            current = player.round_number,
            max = C.NUM_ROUNDS
        )
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import random
        if player.group.dictator_first == True:
            if timeout_happened:
                player.group.allocation = random.randint(0, C.MAXIMUM_MULTIPLY)
                player.group.allocation_timeout = 1
            else:
                player.group.allocation_timeout = 0
        else:
            if timeout_happened:
                player.group.send = random.randint(0, C.ENDOWMENT)
                player.group.send_timeout = 1
            else:
                player.group.send_timeout = 0

class WaitFirstMover(WaitPage):
    template_name = 'move_exogenous/ChoiceWait.html'

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        if group.dictator_first == True:
            return dict(body_text = """
            あなたのグループのメンバーＤが選択をしています。しばらくお待ちください。
            """)
        else:
            return dict(body_text = """
            あなたのグループのメンバーＰが選択をしています。しばらくお待ちください。
            """)

class SecondMover(Page):
    form_model = 'group'

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config['timeout_seconds']

    @staticmethod
    def get_form_fields(player: Player):
        group = player.group
        if group.dictator_first == True:
            return ['send']
        else:
            return ['allocation']
    
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        if group.dictator_first == True:
            return player.role == C.PATRON_ROLE
        else:
            return player.role == C.DICTATOR_ROLE
    
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        if group.dictator_first == True:
            return dict(
                role = 'メンバーＰ',
                allocation = player.group.allocation
            )
        else:
            return dict(
                role = 'メンバーＤ',
                send = player.group.send
            )
    
    @staticmethod
    def js_vars(player: Player):
        group = player.group
        if group.dictator_first == True:
            return dict(
                x = player.group.allocation,
                current = player.round_number,
                max = C.NUM_ROUNDS
            )
        else:
            return dict(
                x = player.group.send,
                current = player.round_number,
                max = C.NUM_ROUNDS
            )
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import random
        if player.group.dictator_first == True:
            if timeout_happened:
                player.group.send = random.randint(0, C.ENDOWMENT)
                player.group.send_timeout = 1
            else:
                player.group.send_timeout = 0
        else:
            if timeout_happened:
                player.group.allocation = random.randint(0, C.MAXIMUM_MULTIPLY)
                player.group.allocation_timeout = 1
            else:
                player.group.allocation_timeout = 0

class WaitSecondMover(WaitPage):
    template_name = 'move_exogenous/ChoiceWait.html'

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        if group.dictator_first == True:
            return dict(body_text = """
            あなたのグループのメンバーＰが選択をしています。しばらくお待ちください。
            """)
        else:
            return dict(body_text = """
            あなたのグループのメンバーＤが選択をしています。しばらくお待ちください。
            """)

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

page_sequence = [
    WaitIntroduction,
    Role,
    WaitRoleCheck,
    FirstMover,
    WaitFirstMover,
    SecondMover,
    WaitSecondMover,
    ResultsWaitPage,
    Results,
    ShuffleWaitPage
]
