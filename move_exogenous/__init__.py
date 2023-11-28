from otree.api import *
import random

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
    NUM_ROUNDS = 3
    GAME_ENDOWMENT = cu(100)
    BELIEF_ENDOWMENT = cu(120)
    MAXIMUM_MULTIPLY = 200
    PATRON_ROLE = "Patron"
    DICTATOR_ROLE = "Dictator"
    RECEIVER_ROLE = "Receiver"


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    subsession.group_randomly()
    config = subsession.session.config

    for g in subsession.get_groups():
        g.dictator_first = config['dictator_first']
        if not g.dictator_first:
            if config['allocation_contractible_even']:
                g.dictator_promise = False
                if subsession.round_number % 2 == 0:
                    g.contractible_s = True
                else:
                    g.contractible_s = False
            elif config['allocation_contractible_odd']:
                g.dictator_promise = False
                if subsession.round_number % 2 == 0:
                    g.contractible_s = False
                else:
                    g.contractible_s = True
            else:
                g.contractible_s = False
                g.dictator_promise = config['dictator_promise']
        else:
            g.contractible_s = False
            g.dictator_promise = False

class Group(BaseGroup):
    send = models.IntegerField(
        min=0, max=C.GAME_ENDOWMENT,
        label = """
        0から100の間の<b>整数（半角数字）</b>で以下のフォームに入力してください。
        """
    )
    allocation = models.IntegerField(
        min=0, max=C.MAXIMUM_MULTIPLY,
        label = """
        0から200の間の<b>整数（半角数字）</b>で以下のフォームに入力してください。
        """
    )
    promise = models.IntegerField(
        min=0, max=C.MAXIMUM_MULTIPLY,
        label = """
        0から200の間の<b>整数（半角数字）</b>で以下のフォームに入力してください。
        """
    )
    belief_1 = models.IntegerField(min=0, label="")
    belief_2 = models.IntegerField(min=0, label="")
    belief_r = models.IntegerField(min=0, label="")
    send_timeout = models.IntegerField()
    allocation_timeout = models.IntegerField()
    promise_timeout = models.IntegerField()
    belief_1_timeout = models.IntegerField()
    belief_2_timeout = models.IntegerField()
    belief_r_timeout = models.IntegerField()
    dictator_first = models.BooleanField()
    dictator_promise = models.BooleanField()
    contractible_s = models.BooleanField()

def belief_1_max(group: Group):
    if group.dictator_first:
        return C.GAME_ENDOWMENT
    else:
        return C.MAXIMUM_MULTIPLY

def belief_2_max(group: Group):
    if group.dictator_first:
        return C.GAME_ENDOWMENT
    else:
        return C.MAXIMUM_MULTIPLY

def belief_r_max(group: Group):
    if group.dictator_first:
        return C.GAME_ENDOWMENT
    else:
        return C.MAXIMUM_MULTIPLY

class Player(BasePlayer):
    pass

# FUNCTIONS
def set_payoffs(subsession: Subsession):
    for g in subsession.get_groups():
        p = g.get_player_by_role(C.PATRON_ROLE)
        d = g.get_player_by_role(C.DICTATOR_ROLE)
        r = g.get_player_by_role(C.RECEIVER_ROLE)
        p.payoff = C.GAME_ENDOWMENT - g.send
        d.payoff = C.GAME_ENDOWMENT - (g.allocation / 100 - 1) * g.send
        r.payoff = (g.allocation / 100) * g.send

        # set participant field
        if g.round_number == 1:
            p.participant.payoff_list = [p.payoff]
            d.participant.payoff_list = [d.payoff]
            r.participant.payoff_list = [r.payoff]
        else:
            p.participant.payoff_list.append(p.payoff)
            d.participant.payoff_list.append(d.payoff)
            r.participant.payoff_list.append(r.payoff)
        
        print(p.participant.payoff_list)

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
    あなたのグループの他の参加者が役割を確認しています。
    しばらくお待ちください。
    """

class Promise(Page):
    form_model = 'group'
    form_fields = ['promise']

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config['timeout_seconds']

    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        if not group.dictator_first and group.dictator_promise:
            return player.role == C.DICTATOR_ROLE
        else:
            return False
    
    @staticmethod
    def js_vars(player: Player):
        return dict(
            current = player.round_number,
            max = C.NUM_ROUNDS
        )
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.group.promise = random.randint(0, C.MAXIMUM_MULTIPLY)
            player.group.promise_timeout = 1
        else:
            player.group.promise_timeout = 0

class WaitPromise(WaitPage):
    body_test = """
    あなたのグループのメンバーＤが選択をしています。
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
        elif group.contractible_s:
            return ['send', 'allocation']
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
        if player.group.dictator_first == True:
            if timeout_happened:
                player.group.allocation = random.randint(0, C.MAXIMUM_MULTIPLY)
                player.group.allocation_timeout = 1
            else:
                player.group.allocation_timeout = 0
        else:
            if timeout_happened:
                player.group.send = random.randint(0, C.GAME_ENDOWMENT)
                player.group.send_timeout = 1
                if player.group.contractible_s:
                    player.group.allocation = random.randint(0, C.MAXIMUM_MULTIPLY)
                    player.group.allocation_timeout = 1
            else:
                player.group.send_timeout = 0
                if player.group.contractible_s:
                    player.group.allocation_timeout = 0

class FirstBelief(Page):
    form_model = 'group'
    form_fields = ['belief_1']

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config['timeout_seconds']

    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        if group.dictator_first == True:
            return player.role == C.DICTATOR_ROLE
        else:
            if not group.contractible_s:
                return player.role == C.PATRON_ROLE
    
    @staticmethod
    def js_vars(player: Player):
        return dict(
            current = player.round_number,
            max = C.NUM_ROUNDS
        )
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        g = player.group
        if timeout_happened:
            g.belief_1_timeout = 1
            if g.dictator_first:
                g.belief_1 = random.randint(0, C.GAME_ENDOWMENT)
            else:
                g.belief_1 = random.randint(0, C.MAXIMUM_MULTIPLY)
        else:
            g.belief_1_timeout = 0

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
    def error_message(player, values):
        group = player.group
        if not group.dictator_first and group.contractible_s:
            if values['allocation'] != group.allocation:
                return '<b>入力エラー!!!</b> メンバーＰが選択した値を指定してください'
    
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
        if player.group.dictator_first == True:
            if timeout_happened:
                player.group.send = random.randint(0, C.GAME_ENDOWMENT)
                player.group.send_timeout = 1
            else:
                player.group.send_timeout = 0
        else:
            if timeout_happened:
                player.group.allocation_timeout = 1
                if not player.group.contractible_s:
                    player.group.allocation = random.randint(0, C.MAXIMUM_MULTIPLY)
            else:
                player.group.allocation_timeout = 0

class SecondBelief(Page):
    form_model='group'
    form_fields=['belief_2']

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config['timeout_seconds']

    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        if group.dictator_first == True:
            return player.role == C.PATRON_ROLE
        else:
            if not group.contractible_s:
                return player.role == C.DICTATOR_ROLE
    
    @staticmethod
    def js_vars(player: Player):
        return dict(
            current = player.round_number,
            max = C.NUM_ROUNDS
        )
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        g = player.group
        if timeout_happened:
            g.belief_2_timeout = 1
            if g.dictator_first:
                g.belief_2 = random.randint(0, C.GAME_ENDOWMENT)
            else:
                g.belief_2 = random.randint(0, C.MAXIMUM_MULTIPLY)
        else:
            g.belief_2_timeout = 0

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

class ShuffleWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'

    body_text = """
    他のグループのゲームの終了を待っています。
    しばらくお待ちください。
    """

    wait_for_all_groups = True

page_sequence = [
    WaitIntroduction,
    Introduction,
    Role,
    WaitRoleCheck,
    Promise,
    WaitPromise,
    FirstMover,
    FirstBelief,
    WaitFirstMover,
    SecondMover,
    SecondBelief,
    WaitSecondMover,
    ShuffleWaitPage
]
