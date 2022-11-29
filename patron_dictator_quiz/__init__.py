from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'quiz'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    # initial endowment
    ENDOWMENT = 100

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

class Answer1(Page):
    template_name = 'patron_dictator_quiz/Answer.html'

    @staticmethod
    def vars_for_template(player: Player):
        cal_patron = round(C.ENDOWMENT - C.Q1_SEND)
        cal_dictator = round(C.ENDOWMENT - (C.Q1_ALLOCATION / 100 - 1) * C.Q1_SEND)
        cal_receiver = round((C.Q1_ALLOCATION / 100) * C.Q1_SEND)

        return dict(
            num = 1,
            send = C.Q1_SEND,
            allocation = C.Q1_ALLOCATION,
            answer_patron = player.quiz1_patron,
            answer_dictator = player.quiz1_dictator,
            answer_receiver = player.quiz1_receiver,
            correct_patron = cal_patron,
            correct_dictator = cal_dictator,
            correct_receiver = cal_receiver,
            commentary = (
                'メンバーPはメンバーDの選択に関わらず、メンバーDに'
                + str(C.Q1_SEND)
                + 'ポイントを渡すので、自身のポイントは'
                + str(cal_patron)
                + 'ポイントとなります。メンバーDは受け取った'
                + str(C.Q1_SEND)
                + 'ポイントを'
                + str(C.Q1_ALLOCATION)
                + '％にしてメンバーRに渡します。すなわち、メンバーDは'
                + str(cal_receiver)
                + 'ポイントをメンバーRに渡します。したがって、メンバーRに渡すポイントはメンバーPから受け取ったポイントで足りるので、メンバーDの最終的なポイントは'
                + str(cal_dictator)
                + 'ポイントのままです。また、メンバーRの最終的なポイントは'
                + str(cal_receiver)
                + 'ポイントです。'
            )
        )

class Answer2(Page):
    template_name = 'patron_dictator_quiz/Answer.html'

    @staticmethod
    def vars_for_template(player: Player):
        cal_patron = round(C.ENDOWMENT - C.Q2_SEND)
        cal_dictator = round(C.ENDOWMENT - (C.Q2_ALLOCATION / 100 - 1) * C.Q2_SEND)
        cal_receiver = round((C.Q2_ALLOCATION / 100) * C.Q2_SEND)

        return dict(
            num = 2,
            send = C.Q2_SEND,
            allocation = C.Q2_ALLOCATION,
            answer_patron = player.quiz2_patron,
            answer_dictator = player.quiz2_dictator,
            answer_receiver = player.quiz2_receiver,
            correct_patron = cal_patron,
            correct_dictator = cal_dictator,
            correct_receiver = cal_receiver,
            commentary = (
                'メンバーPはメンバーDの選択に関わらず、メンバーDに'
                + str(C.Q2_SEND)
                + 'ポイントを渡すので、自身のポイントは'
                + str(cal_patron)
                + 'ポイントとなります。メンバーDは受け取った'
                + str(C.Q2_SEND)
                + 'ポイントを'
                + str(C.Q2_ALLOCATION)
                + '％にしてメンバーRに渡します。すなわち、メンバーDは'
                + str(cal_receiver)
                + 'ポイントをメンバーRに渡します。メンバーRに渡すポイントはメンバーPから受け取ったポイントで足りないので、メンバーDは不足分を自身が保有するポイントで補います。したがって、メンバーDの最終的なポイントは'
                + str(cal_dictator)
                + 'ポイントです。また、メンバーRの最終的なポイントは'
                + str(cal_receiver)
                + 'ポイントです。'
            )
        )

class Answer3(Page):
    template_name = 'patron_dictator_quiz/Answer.html'

    @staticmethod
    def vars_for_template(player: Player):
        cal_patron = round(C.ENDOWMENT - C.Q3_SEND)
        cal_dictator = round(C.ENDOWMENT - (C.Q3_ALLOCATION / 100 - 1) * C.Q3_SEND)
        cal_receiver = round((C.Q3_ALLOCATION / 100) * C.Q3_SEND)

        return dict(
            num = 3,
            send = C.Q3_SEND,
            allocation = C.Q3_ALLOCATION,
            answer_patron = player.quiz3_patron,
            answer_dictator = player.quiz3_dictator,
            answer_receiver = player.quiz3_receiver,
            correct_patron = cal_patron,
            correct_dictator = cal_dictator,
            correct_receiver = cal_receiver,
            commentary = (
                'メンバーPはメンバーDの選択に関わらず、メンバーDに'
                + str(C.Q3_SEND)
                + 'ポイントを渡すので、自身のポイントは'
                + str(cal_patron)
                + 'ポイントとなります。メンバーDは受け取った'
                + str(C.Q3_SEND)
                + 'ポイントを'
                + str(C.Q3_ALLOCATION)
                + '％にしてメンバーRに渡します。すなわち、メンバーDは'
                + str(cal_receiver)
                + 'ポイントをメンバーRに渡します。メンバーDがメンバーPから受け取ったポイントをメンバーRに渡しても、メンバーPから受け取ったポイントに余りが生じるので、余ったポイントはメンバーDのポイントになります。したがって、メンバーDの最終的なポイントは'
                + str(cal_dictator)
                + 'ポイントです。また、メンバーRの最終的なポイントは'
                + str(cal_receiver)
                + 'ポイントです。'
            )
        )

class Answer4(Page):
    template_name = 'patron_dictator_quiz/Answer.html'

    @staticmethod
    def vars_for_template(player: Player):
        cal_patron = round(C.ENDOWMENT - C.Q4_SEND)
        cal_dictator = round(C.ENDOWMENT - (C.Q4_ALLOCATION / 100 - 1) * C.Q4_SEND)
        cal_receiver = round((C.Q4_ALLOCATION / 100) * C.Q4_SEND)

        return dict(
            num = 4,
            send = C.Q4_SEND,
            allocation = C.Q4_ALLOCATION,
            answer_patron = player.quiz4_patron,
            answer_dictator = player.quiz4_dictator,
            answer_receiver = player.quiz4_receiver,
            correct_patron = cal_patron,
            correct_dictator = cal_dictator,
            correct_receiver = cal_receiver,
            commentary = (
                'メンバーPはメンバーDの選択に関わらず、自身のポイントをメンバーDに渡さないので、自身のポイントは'
                + str(cal_patron)
                + 'ポイントとなります。また、メンバーPはメンバーDにポイントを渡さないので、メンバーDとメンバーRの保有ポイントは変化しません。したがって、メンバーDの最終的なポイントは'
                + str(cal_dictator)
                + 'ポイントです。また、メンバーRの最終的なポイントは'
                + str(cal_receiver)
                + 'ポイントです。'
            )
        )

class Answer5(Page):
    template_name = 'patron_dictator_quiz/Answer.html'

    @staticmethod
    def vars_for_template(player: Player):
        cal_patron = round(C.ENDOWMENT - C.Q5_SEND)
        cal_dictator = round(C.ENDOWMENT - (C.Q5_ALLOCATION / 100 - 1) * C.Q5_SEND)
        cal_receiver = round((C.Q5_ALLOCATION / 100) * C.Q5_SEND)

        return dict(
            num = 5,
            send = C.Q5_SEND,
            allocation = C.Q5_ALLOCATION,
            answer_patron = player.quiz5_patron,
            answer_dictator = player.quiz5_dictator,
            answer_receiver = player.quiz5_receiver,
            correct_patron = cal_patron,
            correct_dictator = cal_dictator,
            correct_receiver = cal_receiver,
            commentary = (
                'メンバーPはメンバーDの選択に関わらず、メンバーDに'
                + str(C.Q5_SEND)
                + 'ポイントを渡すので、自身のポイントは'
                + str(cal_patron)
                + 'ポイントとなります。メンバーDは受け取った'
                + str(C.Q5_SEND)
                + 'ポイントを'
                + str(C.Q5_ALLOCATION)
                + '％にしてメンバーRに渡します。すなわち、メンバーDは'
                + str(cal_receiver)
                + 'ポイントをメンバーRに渡します。メンバーDは受け取ったポイントをメンバーRに渡さないので、メンバーPから受け取ったポイントはすべてメンバーDのポイントになります。したがって、メンバーDの最終的なポイントは'
                + str(cal_dictator)
                + 'ポイントです。また、メンバーRの最終的なポイントは'
                + str(cal_receiver)
                + 'ポイントです。'
            )
        )

page_sequence = [
    Quiz1,
    Quiz2,
    Quiz3,
    Quiz4,
    Quiz5,
    Answer1,
    Answer2,
    Answer3,
    Answer4,
    Answer5
]
