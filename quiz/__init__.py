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
    pass

for i in range(5):
    setattr(
        Player,
        'quiz' + str(i + 1) +'_patron',
        models.IntegerField(
            label = '''
            メンバーPの最終的な獲得ポイントはいくらですか？
            0～200の整数（半角数字）で解答してください。''',
            min = 0, max = 200
        )
    )
    setattr(
        Player,
        'quiz' + str(i + 1) +'_dictator',
        models.IntegerField(
            label = '''
            メンバーDの最終的な獲得ポイントはいくらですか？
            0～200の整数（半角数字）で解答してください。''',
            min = 0, max = 200
        )
    )
    setattr(
        Player,
        'quiz' + str(i + 1) +'_receiver',
        models.IntegerField(
            label = '''
            メンバーRの最終的な獲得ポイントはいくらですか？
            0～200の整数（半角数字）で解答してください。''',
            min = 0, max = 200
        )
    )
    setattr(
        Player,
        'correct' + str(i + 1) + '_patron',
        models.IntegerField()
    )
    setattr(
        Player,
        'correct' + str(i + 1) + '_dictator',
        models.IntegerField()
    )
    setattr(
        Player,
        'correct' + str(i + 1) + '_receiver',
        models.IntegerField()
    )


# FUNCTIONS
# PAGES
class Quiz1(Page):
    template_name = 'quiz/Quiz.html'

    form_model = 'player'
    form_fields = ['quiz1_patron', 'quiz1_dictator', 'quiz1_receiver']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num = 1,
            send = C.Q1_SEND,
            allocation = C.Q1_ALLOCATION
        )
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.correct1_patron = round(C.ENDOWMENT - C.Q1_SEND)
        player.correct1_dictator = round(C.ENDOWMENT - (C.Q1_ALLOCATION / 100 - 1) * C.Q1_SEND)
        player.correct1_receiver = round((C.Q1_ALLOCATION / 100) * C.Q1_SEND)
    
    @staticmethod
    def js_vars(player: Player):
        return dict(page = 1)


class Quiz2(Page):
    template_name = 'quiz/Quiz.html'
    
    form_model = 'player'
    form_fields = ['quiz2_patron', 'quiz2_dictator', 'quiz2_receiver']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num = 2,
            send = C.Q2_SEND,
            allocation = C.Q2_ALLOCATION
        )
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.correct2_patron = round(C.ENDOWMENT - C.Q2_SEND)
        player.correct2_dictator = round(C.ENDOWMENT - (C.Q2_ALLOCATION / 100 - 1) * C.Q2_SEND)
        player.correct2_receiver = round((C.Q2_ALLOCATION / 100) * C.Q2_SEND)
    
    @staticmethod
    def js_vars(player: Player):
        return dict(page = 2)

class Quiz3(Page):
    template_name = 'quiz/Quiz.html'

    form_model = 'player'
    form_fields = ['quiz3_patron', 'quiz3_dictator', 'quiz3_receiver']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num = 3,
            send = C.Q3_SEND,
            allocation = C.Q3_ALLOCATION
        )
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.correct3_patron = round(C.ENDOWMENT - C.Q3_SEND)
        player.correct3_dictator = round(C.ENDOWMENT - (C.Q3_ALLOCATION / 100 - 1) * C.Q3_SEND)
        player.correct3_receiver = round((C.Q3_ALLOCATION / 100) * C.Q3_SEND)
    
    @staticmethod
    def js_vars(player: Player):
        return dict(page = 3)

class Quiz4(Page):
    template_name = 'quiz/Quiz.html'

    form_model = 'player'
    form_fields = ['quiz4_patron', 'quiz4_dictator', 'quiz4_receiver']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num = 4,
            send = C.Q4_SEND,
            allocation = C.Q4_ALLOCATION
        )
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.correct4_patron = round(C.ENDOWMENT - C.Q4_SEND)
        player.correct4_dictator = round(C.ENDOWMENT - (C.Q4_ALLOCATION / 100 - 1) * C.Q4_SEND)
        player.correct4_receiver = round((C.Q4_ALLOCATION / 100) * C.Q4_SEND)
    
    @staticmethod
    def js_vars(player: Player):
        return dict(page = 4)

class Quiz5(Page):
    template_name = 'quiz/Quiz.html'

    form_model = 'player'
    form_fields = ['quiz5_patron', 'quiz5_dictator', 'quiz5_receiver']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num = 5,
            send = C.Q5_SEND,
            allocation = C.Q5_ALLOCATION
        )
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.correct5_patron = round(C.ENDOWMENT - C.Q5_SEND)
        player.correct5_dictator = round(C.ENDOWMENT - (C.Q5_ALLOCATION / 100 - 1) * C.Q5_SEND)
        player.correct5_receiver = round((C.Q5_ALLOCATION / 100) * C.Q5_SEND)
    
    @staticmethod
    def js_vars(player: Player):
        return dict(page = 5)

class Answer1(Page):
    template_name = 'quiz/Answer.html'

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num = 1,
            send = C.Q1_SEND,
            allocation = C.Q1_ALLOCATION,
            answer_patron = player.quiz1_patron,
            answer_dictator = player.quiz1_dictator,
            answer_receiver = player.quiz1_receiver,
            correct_patron = player.correct1_patron,
            correct_dictator = player.correct1_dictator,
            correct_receiver = player.correct1_receiver,
            error_patron = player.quiz1_patron != player.correct1_patron,
            error_dictator = player.quiz1_dictator != player.correct1_dictator,
            error_receiver = player.quiz1_receiver != player.correct1_receiver,
            commentary = (
                'メンバーPはメンバーDの選択に関わらず、メンバーDに'
                + str(C.Q1_SEND)
                + 'ポイントを渡すので、自身のポイントは'
                + str(player.correct1_patron)
                + 'ポイントとなります。メンバーDは受け取った'
                + str(C.Q1_SEND)
                + 'ポイントを'
                + str(C.Q1_ALLOCATION)
                + '％にしてメンバーRに渡します。すなわち、メンバーDは'
                + str(player.correct1_receiver)
                + 'ポイントをメンバーRに渡します。したがって、メンバーRに渡すポイントはメンバーPから受け取ったポイントで足りるので、メンバーDの最終的なポイントは'
                + str(player.correct1_dictator)
                + 'ポイントのままです。また、メンバーRの最終的なポイントは'
                + str(player.correct1_receiver)
                + 'ポイントです。'
            )
        )
    
    @staticmethod
    def js_vars(player: Player):
        return dict(page = 1)

class Answer2(Page):
    template_name = 'quiz/Answer.html'

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num = 2,
            send = C.Q2_SEND,
            allocation = C.Q2_ALLOCATION,
            answer_patron = player.quiz2_patron,
            answer_dictator = player.quiz2_dictator,
            answer_receiver = player.quiz2_receiver,
            correct_patron = player.correct2_patron,
            correct_dictator = player.correct2_dictator,
            correct_receiver = player.correct2_receiver,
            error_patron = player.quiz2_patron != player.correct2_patron,
            error_dictator = player.quiz2_dictator != player.correct2_dictator,
            error_receiver = player.quiz2_receiver != player.correct2_receiver,
            commentary = (
                'メンバーPはメンバーDの選択に関わらず、メンバーDに'
                + str(C.Q2_SEND)
                + 'ポイントを渡すので、自身のポイントは'
                + str(player.correct2_patron)
                + 'ポイントとなります。メンバーDは受け取った'
                + str(C.Q2_SEND)
                + 'ポイントを'
                + str(C.Q2_ALLOCATION)
                + '％にしてメンバーRに渡します。すなわち、メンバーDは'
                + str(player.correct2_receiver)
                + 'ポイントをメンバーRに渡します。メンバーRに渡すポイントはメンバーPから受け取ったポイントで足りないので、メンバーDは不足分を自身が保有するポイントで補います。したがって、メンバーDの最終的なポイントは'
                + str(player.correct2_dictator)
                + 'ポイントです。また、メンバーRの最終的なポイントは'
                + str(player.correct2_receiver)
                + 'ポイントです。'
            )
        )
    
    @staticmethod
    def js_vars(player: Player):
        return dict(page = 2)

class Answer3(Page):
    template_name = 'quiz/Answer.html'

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num = 3,
            send = C.Q3_SEND,
            allocation = C.Q3_ALLOCATION,
            answer_patron = player.quiz3_patron,
            answer_dictator = player.quiz3_dictator,
            answer_receiver = player.quiz3_receiver,
            correct_patron = player.correct3_patron,
            correct_dictator = player.correct3_dictator,
            correct_receiver = player.correct3_receiver,
            error_patron = player.quiz3_patron != player.correct3_patron,
            error_dictator = player.quiz3_dictator != player.correct3_dictator,
            error_receiver = player.quiz3_receiver != player.correct3_receiver,
            commentary = (
                'メンバーPはメンバーDの選択に関わらず、メンバーDに'
                + str(C.Q3_SEND)
                + 'ポイントを渡すので、自身のポイントは'
                + str(player.correct3_patron)
                + 'ポイントとなります。メンバーDは受け取った'
                + str(C.Q3_SEND)
                + 'ポイントを'
                + str(C.Q3_ALLOCATION)
                + '％にしてメンバーRに渡します。すなわち、メンバーDは'
                + str(player.correct3_receiver)
                + 'ポイントをメンバーRに渡します。メンバーDがメンバーPから受け取ったポイントをメンバーRに渡しても、メンバーPから受け取ったポイントに余りが生じるので、余ったポイントはメンバーDのポイントになります。したがって、メンバーDの最終的なポイントは'
                + str(player.correct3_dictator)
                + 'ポイントです。また、メンバーRの最終的なポイントは'
                + str(player.correct3_receiver)
                + 'ポイントです。'
            )
        )
    
    @staticmethod
    def js_vars(player: Player):
        return dict(page = 3)

class Answer4(Page):
    template_name = 'quiz/Answer.html'

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num = 4,
            send = C.Q4_SEND,
            allocation = C.Q4_ALLOCATION,
            answer_patron = player.quiz4_patron,
            answer_dictator = player.quiz4_dictator,
            answer_receiver = player.quiz4_receiver,
            correct_patron = player.correct4_patron,
            correct_dictator = player.correct4_dictator,
            correct_receiver = player.correct4_receiver,
            error_patron = player.quiz4_patron != player.correct4_patron,
            error_dictator = player.quiz4_dictator != player.correct4_dictator,
            error_receiver = player.quiz4_receiver != player.correct4_receiver,
            commentary = (
                'メンバーPはメンバーDの選択に関わらず、自身のポイントをメンバーDに渡さないので、自身のポイントは'
                + str(player.correct4_patron)
                + 'ポイントとなります。また、メンバーPはメンバーDにポイントを渡さないので、メンバーDとメンバーRの保有ポイントは変化しません。したがって、メンバーDの最終的なポイントは'
                + str(player.correct4_dictator)
                + 'ポイントです。また、メンバーRの最終的なポイントは'
                + str(player.correct4_receiver)
                + 'ポイントです。'
            )
        )
    
    @staticmethod
    def js_vars(player: Player):
        return dict(page = 4)

class Answer5(Page):
    template_name = 'quiz/Answer.html'

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num = 5,
            send = C.Q5_SEND,
            allocation = C.Q5_ALLOCATION,
            answer_patron = player.quiz5_patron,
            answer_dictator = player.quiz5_dictator,
            answer_receiver = player.quiz5_receiver,
            correct_patron = player.correct5_patron,
            correct_dictator = player.correct5_dictator,
            correct_receiver = player.correct5_receiver,
            error_patron = player.quiz5_patron != player.correct5_patron,
            error_dictator = player.quiz5_dictator != player.correct5_dictator,
            error_receiver = player.quiz5_receiver != player.correct5_receiver,
            commentary = (
                'メンバーPはメンバーDの選択に関わらず、メンバーDに'
                + str(C.Q5_SEND)
                + 'ポイントを渡すので、自身のポイントは'
                + str(player.correct5_patron)
                + 'ポイントとなります。メンバーDは受け取った'
                + str(C.Q5_SEND)
                + 'ポイントを'
                + str(C.Q5_ALLOCATION)
                + '％にしてメンバーRに渡します。すなわち、メンバーDは'
                + str(player.correct5_receiver)
                + 'ポイントをメンバーRに渡します。メンバーDは受け取ったポイントをメンバーRに渡さないので、メンバーPから受け取ったポイントはすべてメンバーDのポイントになります。したがって、メンバーDの最終的なポイントは'
                + str(player.correct5_dictator)
                + 'ポイントです。また、メンバーRの最終的なポイントは'
                + str(player.correct5_receiver)
                + 'ポイントです。'
            )
        )
    
    @staticmethod
    def js_vars(player: Player):
        return dict(page = 5)

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
