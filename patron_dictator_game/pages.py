from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Investment(Page):
    
    form_model = 'group'
    form_fields = ['send']

    def is_displayed(self):
        return self.player.id_in_group == 1

class Allocation(Page):
    
    form_model = 'group'
    form_fields = ['allocation']

    def is_displayed(self):
        return self.player.id_in_group == 2
    
    def vars_for_template(self):
        return dict(
            send_amount = self.group.send
        )

class WaitForPatron(WaitPage):
    pass

class WaitForDictator(WaitPage):
    pass

class ResultsWaitPage(WaitPage):
    
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    pass


page_sequence = [
    WaitForDictator,
    Investment,
    WaitForPatron,
    Allocation,
    ResultsWaitPage, 
    Results
]
