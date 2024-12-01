from otree.api import *
import random

author = 'Hiroki Kato'
doc = """
This is the patron-dictator game,
which reflects an asymmetric information in that
it is difficult for donors to know in advance
the extent to which their donations improve recipients' welfare.
"""


class C(BaseConstants):
    NAME_IN_URL = 'patron_dictator_game'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 15
    FEEDBACK_ROUND = 7
    PROB_AUDIT = 0.7
    BELIEF_ROUNDS = [1,2,8,9,14,15]
    GAME_ENDOWMENT = cu(100)
    BELIEF_ENDOWMENT = cu(120)
    MAXIMUM_MULTIPLY = 200
    PATRON_ROLE = "Patron"
    DICTATOR_ROLE = "Dictator"
    RECEIVER_ROLE = "Receiver"


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    config = subsession.session.config

    subsession.group_randomly(fixed_id_in_group = config['fixed_role'])

    if subsession.round_number == 1:
        if config['fixed_role']:
            group_n = len(subsession.get_groups())
            p = 0
            if 'prob_altruistic_dictator' in config:
                p = config['prob_altruistic_dictator']
            altruistic_dictator = random.choices([True, False], k = group_n, cum_weights=[p, 1])
            # altruistic_dictator = [True, False] #for debug
            i = 0
            for p in subsession.get_players():
                if p.role == 'Dictator':
                    participant = p.participant
                    participant.altruistic_dictator = altruistic_dictator[i]
                    i += 1
        else:
            for p in subsession.get_players():
                if p.role == 'Dictator':
                    participant = p.participant
                    participant.altruistic_dictator = False

        j = 1
        for p in subsession.get_players():
            pp = p.participant
            if p.role == 'Patron':
                pp.nickname = "P-{}".format(j)
            elif p.role == 'Dictator':
                pp.nickname = "D-{}".format(j)
            else:
                pp.nickname = "R-{}".format(j)
            j += 1

    for g in subsession.get_groups():
        g.feedback = config['feedback']

        p = g.get_player_by_role(C.PATRON_ROLE)
        d = g.get_player_by_role(C.DICTATOR_ROLE)
        r = g.get_player_by_role(C.RECEIVER_ROLE)

        g.dictator_altruistic = d.participant.altruistic_dictator
        g.p_label = p.participant.nickname
        g.d_label = d.participant.nickname
        g.r_label = r.participant.nickname

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

    if config['feedback'] and subsession.round_number == C.FEEDBACK_ROUND:
        group_n = len(subsession.get_groups())
        audit = random.choices([True, False], k = group_n, cum_weights=[C.PROB_AUDIT, 1])
        k = 0
        for g in subsession.get_groups():
            g.feedback_occurred = audit[k]
            k += 1
    else:
        for g in subsession.get_groups():
            g.feedback_occurred = False


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
    hope_r = models.IntegerField(
        min=0,
        label = """
        0から200の間の<b>整数（半角数字）</b>で以下のフォームに入力してください。
        """
    )
    send_timeout = models.IntegerField()
    allocation_timeout = models.IntegerField()
    promise_timeout = models.IntegerField()
    belief_1_timeout = models.IntegerField()
    belief_2_timeout = models.IntegerField()
    belief_r_timeout = models.IntegerField()
    hope_r_timeout = models.IntegerField()
    dictator_first = models.BooleanField()
    dictator_promise = models.BooleanField()
    contractible_s = models.BooleanField()
    dictator_altruistic = models.BooleanField()
    feedback = models.BooleanField()
    feedback_occurred = models.BooleanField(initial=False)
    p_label = models.StringField()
    d_label = models.StringField()
    r_label = models.StringField()

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

def hope_r_max(group: Group):
    return (C.MAXIMUM_MULTIPLY / 100) * C.GAME_ENDOWMENT

class Player(BasePlayer):
    game_payoff = models.CurrencyField()
    belief_payoff = models.CurrencyField()

class Calculator(ExtraModel):
    group = models.Link(Group)
    player = models.Link(Player)
    stage = models.StringField()
    send = models.IntegerField()
    allocation = models.IntegerField()

# FUNCTIONS
def set_payoffs(subsession: Subsession):
    for g in subsession.get_groups():
        p = g.get_player_by_role(C.PATRON_ROLE)
        d = g.get_player_by_role(C.DICTATOR_ROLE)
        r = g.get_player_by_role(C.RECEIVER_ROLE)

        p.game_payoff = C.GAME_ENDOWMENT - g.send
        r.game_payoff = (g.allocation / 100) * g.send
        if g.dictator_altruistic:
            d.game_payoff = r.game_payoff
        else:
            d.game_payoff = C.GAME_ENDOWMENT - (g.allocation / 100 - 1) * g.send

        if g.field_maybe_none('belief_1') is not None:
            if g.dictator_first:
                d.belief_payoff = C.BELIEF_ENDOWMENT - 120 * ((g.send - g.belief_1)/100) ** 2
                p.belief_payoff = C.BELIEF_ENDOWMENT - 120 * ((g.belief_1 - g.belief_2)/100) ** 2
                r.belief_payoff = C.BELIEF_ENDOWMENT - 120 * ((g.send - g.belief_r)/100) ** 2
            else:
                p.belief_payoff = C.BELIEF_ENDOWMENT - 30 * ((g.allocation - g.belief_1)/100) ** 2
                d.belief_payoff = C.BELIEF_ENDOWMENT - 30 * ((g.belief_1 - g.belief_2)/100) ** 2
                r.belief_payoff = C.BELIEF_ENDOWMENT - 30 * ((g.allocation - g.belief_r)/100) ** 2

        p.payoff = p.game_payoff + (p.field_maybe_none('belief_payoff') or 0)
        d.payoff = d.game_payoff + (d.field_maybe_none('belief_payoff') or 0)
        r.payoff = r.game_payoff + (r.field_maybe_none('belief_payoff') or 0)

    # set participant field
    if subsession.round_number == C.NUM_ROUNDS:
        rounds = range(1, C.NUM_ROUNDS + 1)
        for p in subsession.get_players():
            pp = p.participant
            pp.payoff_list = [p.in_round(i).payoff for i in rounds]
            pp.game_payoff_list = [p.in_round(i).game_payoff for i in rounds]
            pp.belief_payoff_list = [p.in_round(i).field_maybe_none('belief_payoff') for i in rounds]

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

    @staticmethod
    def vars_for_template(player: Player):
        config = player.subsession.session.config
        all_p = player.subsession.get_players()
        n = 0
        n_alt = 0
        for p in all_p:
            if p.role == C.DICTATOR_ROLE:
                n += 1
                if p.participant.altruistic_dictator:
                    n_alt += 1

        return dict(
            n_dictator = n,
            n_selfish_dictator = n - n_alt,
            prior = 100 - 100 * config['prob_altruistic_dictator']
        )


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
    def live_method(player: Player, data):
        group = player.group
        Calculator.create(
            group=group,
            player=player,
            stage="promise",
            send=data["x"],
            allocation=data["s"]
        )

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
    def live_method(player: Player, data):
        group = player.group
        Calculator.create(
            group=group,
            player=player,
            stage="first mover",
            send=data["x"],
            allocation=data["s"]
        )

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
        if group.round_number in C.BELIEF_ROUNDS:
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

class ReceiverBelief(Page):
    form_model = 'group'
    form_fields = ['belief_r']

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config['timeout_seconds']

    @staticmethod
    def is_displayed(player: Player):
        g = player.group
        if g.round_number in C.BELIEF_ROUNDS:
            if not g.contractible_s:
                return player.role == C.RECEIVER_ROLE

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
            g.belief_r_timeout = 1
            if g.dictator_first:
                g.belief_r = random.randint(0, C.GAME_ENDOWMENT)
            else:
                g.belief_r = random.randint(0, C.MAXIMUM_MULTIPLY)
        else:
            g.belief_r_timeout = 0

class WaitFirstMover(WaitPage):
    template_name = 'move_exogenous/ChoiceWait.html'
    body_text = """
    他のグループのメンバーが意思決定をしています。
    しばらくお待ちください。
    """

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
                type2 = player.group.dictator_altruistic,
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
        if group.round_number in C.BELIEF_ROUNDS:
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

class ReceiverHope(Page):
    form_model = 'group'
    form_fields = ['hope_r']

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config['timeout_seconds']

    @staticmethod
    def is_displayed(player: Player):
        if player.round_number in C.BELIEF_ROUNDS:
            return player.role == C.RECEIVER_ROLE
    
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
            g.hope_r_timeout = 1
            g.hope_r = random.randint(0, (C.MAXIMUM_MULTIPLY / 100) * C.GAME_ENDOWMENT)
        else:
            g.hope_r_timeout = 0

class WaitSecondMover(WaitPage):
    template_name = 'move_exogenous/ChoiceWait.html'
    body_text = """
    他のグループのメンバーが意思決定をしています。
    しばらくお待ちください。
    """

class Feedback(Page):
    @staticmethod
    def is_displayed(player: Player):
        g = player.group
        return g.feedback_occurred

    @staticmethod
    def vars_for_template(player: Player):
        p = player
        rounds = range(1, C.FEEDBACK_ROUND + 1)
        p_label = [p.in_round(i).group.p_label for i in rounds]
        d_label = [p.in_round(i).group.d_label for i in rounds]
        send = [p.in_round(i).group.send for i in rounds]
        allocation = [p.in_round(i).group.allocation for i in rounds]
        promise = [p.in_round(i).group.field_maybe_none('promise') for i in rounds]

        return dict(
            table_item = zip(p_label, d_label, send, allocation, promise)
        )

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
    ReceiverBelief,
    WaitFirstMover,
    SecondMover,
    SecondBelief,
    # ReceiverHope,
    WaitSecondMover,
    Feedback,
    ShuffleWaitPage
]
