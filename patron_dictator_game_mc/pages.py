from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Movement(Page):

    form_model = 'group'
    form_fields = ['movement']

    def is_displayed(self):
        return self.player.id_in_group == 2

class MovementResult(Page):

    def vars_for_template(self):
        return dict(
            choice = self.group.movement
        )
    
    def app_after_this_page(self, upcoming_apps):
        if self.group.movement:
            return "patron_dictator_game_fd"
        else:
            return "patron_dictator_game_sd"

class ResultWaitPage(WaitPage):

    pass

page_sequence = [
    Movement,
    ResultWaitPage,
    MovementResult
]
