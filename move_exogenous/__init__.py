from otree.api import *


author = 'Hiroki Kato'
doc = """
Strategic Relationship between Donors and Charities: Patron-Dictator Game (PDG in short).
This game is the PDG with first-moving dictator treatment.
"""


class C(BaseConstants):
    NAME_IN_URL = 'patron_dictator_game_fd'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 10
    ENDOWMENT = cu(100)
    MAXIMUM_MULTIPLY = cu(200)
    PATRON_ROLE = "Patron"
    DICTATOR_ROLE = "Dictator"
    RECEIVER_ROLE = "Receiver"


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    subsession.group_randomly()

    if 'first_moving_dictator' in subsession.session.config:
        for g in subsession.get_groups():
            g.dictator_first = subsession.session.config['first_moving_dictator']
            print('First-Moving Dictator: ', g.dictator_first)
    else:
        if 'first_half_FD' in subsession.session.config:
            if subsession.session.config['first_half_FD']:
                if subsession.round_number <= C.NUM_ROUNDS // 2:
                    for g in subsession.get_groups():
                        g.dictator_first = True
                else:
                    for g in subsession.get_groups():
                        g.dictator_first = False
            else:
                if subsession.round_number <= C.NUM_ROUNDS // 2:
                    for g in subsession.get_groups():
                        g.dictator_first = False
                else:
                    for g in subsession.get_groups():
                        g.dictator_first = True
        else:
            # Case A: numbers of groups = even & numbers of rounds = even or odd
            #   To equally random assignment, remove flow in False condition
            #   run flow in True condition every rounds (remove if condition)
            # Case B: numbers of groups = odd & numbers of rounds = even or odd
            #   To equally random assignment, keep flow in False condition
            #   If numbers of rounds = odd, not perfect equal random but best approximation
            if subsession.round_number == 1:
                import itertools as it
                first = it.cycle([True, False])
                for g in subsession.get_groups():
                    g.dictator_first = next(first)
            else:
                for g in subsession.get_groups():
                    previous_round = g.in_round(subsession.round_number - 1)
                    previous_first = previous_round.dictator_first
                    g.dictator_first = not previous_first



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

class Introduction(Page):
    @staticmethod
    def vars_for_template(player: Player):
        d = dict(first_half_fd = player.session.config['first_half_FD'])
        if player.round_number == 1: 
            d['first_half'] = True
        elif player.round_number == 1 + C.NUM_ROUNDS // 2:
            d['first_half'] = False
        return d

    @staticmethod
    def get_timeout_seconds(player: Player):
        session = player.session
        return session.config['timeout_seconds']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 or player.round_number == 1 + C.NUM_ROUNDS // 2

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
            return dict(role = 'メンバーD')
        else:
            return dict(role = 'メンバーP')
    
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
            あなたのグループのメンバーDが選択をしています。しばらくお待ちください。
            """)
        else:
            return dict(body_text = """
            あなたのグループのメンバーPが選択をしています。しばらくお待ちください。
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
                role = 'メンバーP',
                allocation = player.group.allocation
            )
        else:
            return dict(
                role = 'メンバーD',
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
            あなたのグループのメンバーPが選択をしています。しばらくお待ちください。
            """)
        else:
            return dict(body_text = """
            あなたのグループのメンバーDが選択をしています。しばらくお待ちください。
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
        
        if player.round_number == C.NUM_ROUNDS:
            selected_round = []
            first_half_end = C.NUM_ROUNDS // 2
            selected_round.append(random.randint(1, first_half_end))
            selected_round.append(random.randint(first_half_end + 1, C.NUM_ROUNDS))
            # while len(selected_round) < 2:
            #     n = random.randint(1, C.NUM_ROUNDS)
            #     if not n in selected_round:
            #         selected_round.append(n)
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
    Introduction,
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
