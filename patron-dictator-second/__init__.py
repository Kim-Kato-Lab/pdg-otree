from otree.api import *


author = 'Hiroki Kato'
doc = """
Strategic Relationship between Donors and Charities: Patron-Dictator Game (PDG in short).
This game is the PDG with second-moving dictator treatment.
"""

class C(BaseConstants):
    NAME_IN_URL = 'patron_dictator_game_sd'
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

class Send(Page):
    form_model = 'group'
    form_fields = ['send']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.PATRON_ROLE


class Allocation(Page):
    form_model = 'group'
    form_fields = ['allocation']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.DICTATOR_ROLE

    @staticmethod
    def js_vars(player: Player):
        return dict(x=player.group.send)

    @staticmethod
    def vars_for_template(player: Player):
        return dict(send=player.group.send)


class WaitForPatron(WaitPage):
    body_text = """
    あなたのグループのメンバーPが選択をしています。
    しばらくお待ちください。
    """


class WaitForDictator(WaitPage):
    body_text = """
    あなたのグループのメンバーDが選択をしています。
    しばらくお待ちください。
    """


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    pass

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
  WaitForPatron,
  Allocation,
  WaitForDictator,
  ResultsWaitPage,
  Results,
  ShuffleWaitPage
]
