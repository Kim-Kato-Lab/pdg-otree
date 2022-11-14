from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Investment(Page):
    
    form_model = 'group'
    form_fields = ['send']

    def is_displayed(self):
        return self.player.id_in_group == 1
    
    def vars_for_template(self):
        return dict(
            dictator_rule = self.group.allocation
        )
    
    def js_vars(self):
        return dict(
            x = self.group.allocation
        )

class Allocation(Page):
    
    form_model = 'group'
    form_fields = ['allocation']

    def is_displayed(self):
        return self.player.id_in_group == 2

class ShuffleWaitPage(WaitPage):
    
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession):
        subsession.group_randomly()

class WaitForPatron(WaitPage):
    pass

class WaitForDictator(WaitPage):
    pass

class ResultsWaitPage(WaitPage):
    
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    
    def vars_for_template(self):
        return dict(
            patron_investment = self.group.send,
            dictator_investment = (self.group.allocation/100) * self.group.send,
            diff = (self.group.allocation/100) * self.group.send - self.group.send,
            abs_diff = abs((self.group.allocation/100) * self.group.send - self.group.send)
        )


page_sequence = [
    WaitForPatron,
    Allocation,
    WaitForDictator,
    Investment,
    ResultsWaitPage, 
    Results,
    ShuffleWaitPage
]
