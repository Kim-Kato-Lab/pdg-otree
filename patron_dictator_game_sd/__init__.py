from otree.api import *


author = 'Your name here'
doc = """
Your app description
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
    send = models.CurrencyField(min=0, max=C.ENDOWMENT)
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
class Investment(Page):
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
        return dict(receive_amount=player.group.send)


class WaitForPatron(WaitPage):
    pass


class WaitForDictator(WaitPage):
    pass


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            patron_investment=player.group.send,
            dictator_investment=(player.group.allocation / 100) * player.group.send,
            diff=(player.group.allocation / 100) * player.group.send - player.group.send,
            abs_diff=abs((player.group.allocation / 100) * player.group.send - player.group.send),
        )

class ShuffleWaitPage(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession: Subsession):
        subsession.group_randomly()

page_sequence = [
  WaitForDictator,
  Investment,
  WaitForPatron,
  Allocation,
  ResultsWaitPage,
  Results
]
