from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'quiz'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    quiz1_patron = models.IntegerField(
      label = '''
      メンバーPの最終的な獲得ポイントはいくらですか？
      0～200の整数（半角数字）で解答してください。''',
      min = 0, max = 200
    )
    quiz1_dictator = models.IntegerField(
      label = '''
      メンバーDの最終的な獲得ポイントはいくらですか？
      0～200の整数（半角数字）で解答してください。''',
      min = 0, max = 200
    )
    quiz1_receiver = models.IntegerField(
      label = '''
      メンバーRの最終的な獲得ポイントはいくらですか？
      0～200の整数（半角数字）で解答してください。''',
      min = 0, max = 200
    )


# FUNCTIONS
# PAGES
class Quiz1(Page):
    form_model = 'player'
    form_fields = ['quiz1_patron', 'quiz1_dictator', 'quiz1_receiver']

page_sequence = [
  Quiz1
]
