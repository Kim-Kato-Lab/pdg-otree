from otree.api import *


author = 'Your name here'
doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'my_trust'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = cu(10)
    MULTIPLICATION_FACTOR = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    sent_amount = models.CurrencyField(label="How much do you want to send to participant B?")
    sentback_amount = models.CurrencyField(label="How much do you want to send back?")


class Player(BasePlayer):
    sent_amount = models.CurrencyField()
    sentback_amount = models.CurrencyField()


# FUNCTIONS
def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.payoff = C.ENDOWMENT - group.sent_amount + group.sentback_amount
    p2.payoff = group.sent_amount * C.MULTIPLICATION_FACTOR - group.sentback_amount


def sentback_amount_choices(player: Player):
    return currency_range(cu(0), player.sent_amount * C.MULTIPLICATION_FACTOR, cu(1))


# PAGES
class Send(Page):
    form_model = 'group'
    form_fields = ['sent_amount']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class Sendback(Page):
    form_model = 'group'
    form_fields = ['sentback_amount']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

    @staticmethod
    def vars_for_template(player: Player):
        return dict(tripled_amount=player.group.sent_amount * C.MULTIPLICATION_FACTOR)


class Results(Page):
    pass


class WaitForP1(WaitPage):
    pass


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


page_sequence = [Send, WaitForP1, Sendback, ResultsWaitPage, Results]
