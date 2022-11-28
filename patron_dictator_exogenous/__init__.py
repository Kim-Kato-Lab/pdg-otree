from otree.api import *


author = 'Hiroki Kato'
doc = """
Strategic Relationship between Donors and Charities: Patron-Dictator Game (PDG in short).
This game is the PDG with first-moving dictator treatment.
"""


class C(BaseConstants):
    NAME_IN_URL = 'patron_dictator_game_fd'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 2
    ENDOWMENT = cu(100)
    MAXIMUM_MULTIPLY = cu(200)
    PATRON_ROLE = "Patron"
    DICTATOR_ROLE = "Dictator"
    RECEIVER_ROLE = "Receiver"


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    subsession.group_randomly()
    
    for player in subsession.get_players():
        participant = player.participant
        participant.first_dictator = subsession.session.config['first_dictator']
        print("First Dictator Movement", participant.first_dictator)


class Group(BaseGroup):
    send = models.IntegerField(min=0, max=C.ENDOWMENT)
    allocation = models.IntegerField(min=0, max=C.MAXIMUM_MULTIPLY)


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
class Role(Page):
    pass

class WaitRoleCheck(WaitPage):
    body_text = """
    あなたのグループのメンバーが役割を確認しています。
    しばらくお待ちください。
    """

class FirstMover(Page):
    form_model = 'group'

    @staticmethod
    def get_form_fields(player: Player):
        participant = player.participant

        if participant.first_dictator == True:
            return ['allocation']
        else:
            return ['send']

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if participant.first_dictator == True:
            return player.role == C.DICTATOR_ROLE
        else:
            return player.role == C.PATRON_ROLE
    
    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        if participant.first_dictator == True:
            return dict(role = 'メンバーD')
        else:
            return dict(role = 'メンバーP')

class WaitFirstMover(WaitPage):
    template_name = 'patron_dictator_exogenous/ChoiceWait.html'

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        if participant.first_dictator == True:
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
    def get_form_fields(player: Player):
        participant = player.participant
        if participant.first_dictator == True:
            return ['send']
        else:
            return ['allocation']
    
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        if participant.first_dictator == True:
            return player.role == C.PATRON_ROLE
        else:
            return player.role == C.DICTATOR_ROLE
    
    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        if participant.first_dictator == True:
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
        participant = player.participant
        if participant.first_dictator == True:
            return dict(x = player.group.allocation)
        else:
            return dict(x = player.group.send)

class WaitSecondMover(WaitPage):
    template_name = 'patron_dictator_exogenous/ChoiceWait.html'

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        if participant.first_dictator == True:
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
    FirstMover,
    WaitFirstMover,
    SecondMover,
    WaitSecondMover,
    ResultsWaitPage,
    Results,
    ShuffleWaitPage
]
