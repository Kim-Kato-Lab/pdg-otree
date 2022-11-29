from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'quiz'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    # Situation of Quiz1
    Q1_SEND = 50
    Q1_ALLOCATION = 100

    # Situation of Quiz2
    Q2_SEND = 50
    Q2_ALLOCATION = 200

    # Situation of Quiz3
    Q3_SEND = 50
    Q3_ALLOCATION = 0

    # Situation of Quiz4
    Q4_SEND = 0
    Q4_ALLOCATION = 200

    # Situation of Quiz5
    Q5_SEND = 100
    Q5_ALLOCATION = 0


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Quiz1
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

    # Quiz2
    quiz2_patron = models.IntegerField(
        label = '''
        メンバーPの最終的な獲得ポイントはいくらですか？
        0～200の整数（半角数字）で解答してください。''',
        min = 0, max = 200
    )
    quiz2_dictator = models.IntegerField(
        label = '''
        メンバーDの最終的な獲得ポイントはいくらですか？
        0～200の整数（半角数字）で解答してください。''',
        min = 0, max = 200
    )
    quiz2_receiver = models.IntegerField(
        label = '''
        メンバーRの最終的な獲得ポイントはいくらですか？
        0～200の整数（半角数字）で解答してください。''',
        min = 0, max = 200
    )

    # Quiz3
    quiz3_patron = models.IntegerField(
        label = '''
        メンバーPの最終的な獲得ポイントはいくらですか？
        0～200の整数（半角数字）で解答してください。''',
        min = 0, max = 200
    )
    quiz3_dictator = models.IntegerField(
        label = '''
        メンバーDの最終的な獲得ポイントはいくらですか？
        0～200の整数（半角数字）で解答してください。''',
        min = 0, max = 200
    )
    quiz3_receiver = models.IntegerField(
        label = '''
        メンバーRの最終的な獲得ポイントはいくらですか？
        0～200の整数（半角数字）で解答してください。''',
        min = 0, max = 200
    )

    # Quiz4
    quiz4_patron = models.IntegerField(
        label = '''
        メンバーPの最終的な獲得ポイントはいくらですか？
        0～200の整数（半角数字）で解答してください。''',
        min = 0, max = 200
    )
    quiz4_dictator = models.IntegerField(
        label = '''
        メンバーDの最終的な獲得ポイントはいくらですか？
        0～200の整数（半角数字）で解答してください。''',
        min = 0, max = 200
    )
    quiz4_receiver = models.IntegerField(
        label = '''
        メンバーRの最終的な獲得ポイントはいくらですか？
        0～200の整数（半角数字）で解答してください。''',
        min = 0, max = 200
    )

    # Quiz5
    quiz5_patron = models.IntegerField(
        label = '''
        メンバーPの最終的な獲得ポイントはいくらですか？
        0～200の整数（半角数字）で解答してください。''',
        min = 0, max = 200
    )
    quiz5_dictator = models.IntegerField(
        label = '''
        メンバーDの最終的な獲得ポイントはいくらですか？
        0～200の整数（半角数字）で解答してください。''',
        min = 0, max = 200
    )
    quiz5_receiver = models.IntegerField(
        label = '''
        メンバーRの最終的な獲得ポイントはいくらですか？
        0～200の整数（半角数字）で解答してください。''',
        min = 0, max = 200
    )


# FUNCTIONS
# PAGES
class Quiz1(Page):
    template_name = 'patron_dictator_quiz/Quiz.html'

    form_model = 'player'
    form_fields = ['quiz1_patron', 'quiz1_dictator', 'quiz1_receiver']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num = 1,
            send = C.Q1_SEND,
            allocation = C.Q1_ALLOCATION
        )

class Quiz2(Page):
    template_name = 'patron_dictator_quiz/Quiz.html'
    
    form_model = 'player'
    form_fields = ['quiz2_patron', 'quiz2_dictator', 'quiz2_receiver']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num = 2,
            send = C.Q2_SEND,
            allocation = C.Q2_ALLOCATION
        )

class Quiz3(Page):
    template_name = 'patron_dictator_quiz/Quiz.html'

    form_model = 'player'
    form_fields = ['quiz3_patron', 'quiz3_dictator', 'quiz3_receiver']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num = 3,
            send = C.Q3_SEND,
            allocation = C.Q3_ALLOCATION
        )

class Quiz4(Page):
    template_name = 'patron_dictator_quiz/Quiz.html'

    form_model = 'player'
    form_fields = ['quiz4_patron', 'quiz4_dictator', 'quiz4_receiver']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num = 4,
            send = C.Q4_SEND,
            allocation = C.Q4_ALLOCATION
        )

class Quiz5(Page):
    template_name = 'patron_dictator_quiz/Quiz.html'

    form_model = 'player'
    form_fields = ['quiz5_patron', 'quiz5_dictator', 'quiz5_receiver']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num = 5,
            send = C.Q5_SEND,
            allocation = C.Q5_ALLOCATION
        )

page_sequence = [
    Quiz1,
    Quiz2,
    Quiz3,
    Quiz4,
    Quiz5
]
