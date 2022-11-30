from otree.api import *


author = 'Your name here'
doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'patron_dictator_game_mc'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1
    ENDOWMENT = cu(100)
    MAXIMUM_MULTIPLY = cu(200)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    movement = models.BooleanField(choices=[[False, "Second"], [True, "First"]])
    send = models.CurrencyField(min=0, max=C.ENDOWMENT)
    allocation = models.IntegerField(min=0, max=C.MAXIMUM_MULTIPLY)


class Player(BasePlayer):
    pass


# FUNCTIONS
def set_payoffs(group: Group):
    patron = group.get_player_by_role('patron')
    dictator = group.get_player_by_role('dictator')
    receiver = group.get_player_by_role('receiver')
    patron.payoff = C.ENDOWMENT - group.send
    dictator.payoff = C.ENDOWMENT - (group.allocation / 100 - 1) * group.send
    receiver.payoff = (group.allocation / 100) * group.send


def role(player: Player):
    if player.id_in_group == 1:
        return "patron"
    if player.id_in_group == 2:
        return "dictator"
    if player.id_in_group == 3:
        return "receiver"


# PAGES
class Movement(Page):
    form_model = 'group'
    form_fields = ['movement']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2


class InvestmentF(Page):
    form_model = 'group'
    form_fields = ['send']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1 and player.group.movement

    @staticmethod
    def vars_for_template(player: Player):
        return dict(dictator_rule=player.group.allocation)

    @staticmethod
    def js_vars(player: Player):
        return dict(x=player.group.allocation)


class InvestmentS(Page):
    form_model = 'group'
    form_fields = ['send']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1 and not player.group.movement


class AllocationF(Page):
    form_model = 'group'
    form_fields = ['allocation']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2 and player.group.movement


class AllocationS(Page):
    form_model = 'group'
    form_fields = ['allocation']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2 and not player.group.movement

    @staticmethod
    def js_vars(player: Player):
        return dict(x=player.group.send)

    @staticmethod
    def vars_for_template(player: Player):
        return dict(receive_amount=player.group.send)


class MovementResults(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(choice=player.group.movement)


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            patron_investment=player.group.send,
            dictator_investment=(player.group.allocation / 100) * player.group.send,
            diff=(player.group.allocation / 100) * player.group.send - player.group.send,
            abs_diff=abs((player.group.allocation / 100) * player.group.send - player.group.send),
        )


class ResultWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class WaitForDictator(WaitPage):
    pass


class WaitForPatron(WaitPage):
    pass


page_sequence = [
    Movement,
    WaitForDictator,
    MovementResults,
    AllocationF,
    WaitForDictator,
    InvestmentF,
    WaitForPatron,
    InvestmentS,
    WaitForPatron,
    AllocationS,
    WaitForDictator,
    ResultWaitPage,
    Results,
]
