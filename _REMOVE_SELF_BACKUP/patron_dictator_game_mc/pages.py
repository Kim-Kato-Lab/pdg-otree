from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Movement(Page):

    form_model = 'group'
    form_fields = ['movement']

    def is_displayed(self):
        return self.player.id_in_group == 2

class InvestmentF(Page):

    form_model = 'group'
    form_fields = ['send']

    def is_displayed(self):
        return self.player.id_in_group == 1 and self.group.movement
    
    def vars_for_template(self):
        return dict(
            dictator_rule = self.group.allocation
        )
    
    def js_vars(self):
        return dict(
            x = self.group.allocation
        )

class InvestmentS(Page):
    
    form_model = 'group'
    form_fields = ['send']

    def is_displayed(self):
        return self.player.id_in_group == 1 and not self.group.movement

class AllocationF(Page):

    form_model = 'group'
    form_fields = ['allocation']

    def is_displayed(self):
        return self.player.id_in_group == 2 and self.group.movement
class AllocationS(Page):
    
    form_model = 'group'
    form_fields = ['allocation']

    def is_displayed(self):
        return self.player.id_in_group == 2 and not self.group.movement
    
    def js_vars(self):
        return dict(
            x = self.group.send
        )
    
    def vars_for_template(self):
        return dict(
            receive_amount = self.group.send
        )

class MovementResults(Page):

    def vars_for_template(self):
        return dict(
            choice = self.group.movement
        )

class Results(Page):
    
    def vars_for_template(self):
        return dict(
            patron_investment = self.group.send,
            dictator_investment = (self.group.allocation/100) * self.group.send,
            diff = (self.group.allocation/100) * self.group.send - self.group.send,
            abs_diff = abs((self.group.allocation/100) * self.group.send - self.group.send)
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
    Results
]
