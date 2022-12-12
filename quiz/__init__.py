from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'quiz'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 10

    NUMBER_Q = 3
    SETUP = {
        1: {
            "endowment": 100,
            "send": 50,
            "allocation": 100
        },
        2: {
            "endowment": 100,
            "send": 50,
            "allocation": 200
        },
        3: {
            "endowment": 100,
            "send": 50,
            "allocation": 0
        }
    }
class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass

for k in C.SETUP.keys():
    setattr(
        Player,
        'quiz' + str(k) +'_patron',
        models.IntegerField(
            label = '''
            メンバーPの最終的な獲得トークンはいくらですか？
            0～200の整数（半角数字）で解答してください。''',
            min = 0, max = 200
        )
    )
    setattr(
        Player,
        'quiz' + str(k) +'_dictator',
        models.IntegerField(
            label = '''
            メンバーDの最終的な獲得トークンはいくらですか？
            0～200の整数（半角数字）で解答してください。''',
            min = 0, max = 200
        )
    )
    setattr(
        Player,
        'quiz' + str(k) +'_receiver',
        models.IntegerField(
            label = '''
            メンバーRの最終的な獲得トークンはいくらですか？
            0～200の整数（半角数字）で解答してください。''',
            min = 0, max = 200
        )
    )
    setattr(
        Player,
        'error' + str(k) + '_patron',
        models.IntegerField()
    )
    setattr(
        Player,
        'error' + str(k) + '_dictator',
        models.IntegerField()
    )
    setattr(
        Player,
        'error' + str(k) + '_receiver',
        models.IntegerField()
    )


# FUNCTIONS
def correct_cal(endowment, send, allocation):
    return dict(
        patron = round(endowment - send),
        dictator = round(endowment - (allocation / 100 - 1) * send),
        receiver = round((allocation / 100) * send)
    )

# PAGES
class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class Quiz1(Page):
    template_name = 'quiz/Quiz.html'

    form_model = 'player'
    form_fields = ['quiz1_patron', 'quiz1_dictator', 'quiz1_receiver']

    @staticmethod
    def is_displayed(player: Player):
        if player.round_number == 1:
            return True
        else:
            previous = player.in_round(player.round_number - 1)
            check = [
                previous.field_maybe_none('error1_patron'),
                previous.field_maybe_none('error1_dictator'),
                previous.field_maybe_none('error1_receiver')
            ]

            count = 0
            for x in check:
                if x == 0 or x is None:
                    count += 1
            return count != 3

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num = 1,
            endowment = C.SETUP[1]["endowment"],
            send = C.SETUP[1]["send"],
            allocation = C.SETUP[1]["allocation"]
        )
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        setup = C.SETUP[1]
        correct = correct_cal(setup["endowment"], setup["send"], setup["allocation"])
        player.error1_patron = correct["patron"] - player.quiz1_patron
        player.error1_dictator = correct["dictator"] - player.quiz1_dictator
        player.error1_receiver = correct["receiver"] - player.quiz1_receiver
    
    @staticmethod
    def js_vars(player: Player):
        return dict(page = 1)


class Quiz2(Page):
    template_name = 'quiz/Quiz.html'
    
    form_model = 'player'
    form_fields = ['quiz2_patron', 'quiz2_dictator', 'quiz2_receiver']

    @staticmethod
    def is_displayed(player: Player):
        if player.round_number == 1:
            return True
        else:
            previous = player.in_round(player.round_number - 1)
            check = [
                previous.field_maybe_none('error2_patron'),
                previous.field_maybe_none('error2_dictator'),
                previous.field_maybe_none('error2_receiver')
            ]

            count = 0
            for x in check:
                if x == 0 or x is None:
                    count += 1
            return count != 3

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num = 2,
            endowment = C.SETUP[2]["endowment"],
            send = C.SETUP[2]["send"],
            allocation = C.SETUP[2]["allocation"]
        )
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        setup = C.SETUP[2]
        correct = correct_cal(setup["endowment"], setup["send"], setup["allocation"])
        player.error2_patron = correct["patron"] - player.quiz2_patron
        player.error2_dictator = correct["dictator"] - player.quiz2_dictator
        player.error2_receiver = correct["receiver"] - player.quiz2_receiver
    
    @staticmethod
    def js_vars(player: Player):
        return dict(page = 2)

class Quiz3(Page):
    template_name = 'quiz/Quiz.html'

    form_model = 'player'
    form_fields = ['quiz3_patron', 'quiz3_dictator', 'quiz3_receiver']

    @staticmethod
    def is_displayed(player: Player):
        if player.round_number == 1:
            return True
        else:
            previous = player.in_round(player.round_number - 1)
            check = [
                previous.field_maybe_none('error3_patron'),
                previous.field_maybe_none('error3_dictator'),
                previous.field_maybe_none('error3_receiver')
            ]

            count = 0
            for x in check:
                if x == 0 or x is None:
                    count += 1
            return count != 3

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num = 3,
            endowment = C.SETUP[3]["endowment"],
            send = C.SETUP[3]["send"],
            allocation = C.SETUP[3]["allocation"]
        )
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        setup = C.SETUP[3]
        correct = correct_cal(setup["endowment"], setup["send"], setup["allocation"])
        player.error3_patron = correct["patron"] - player.quiz3_patron
        player.error3_dictator = correct["dictator"] - player.quiz3_dictator
        player.error3_receiver = correct["receiver"] - player.quiz3_receiver
    
    @staticmethod
    def js_vars(player: Player):
        return dict(page = 3)

class Answer1(Page):
    template_name = 'quiz/Answer.html'

    @staticmethod
    def is_displayed(player: Player):
        if player.round_number == 1:
            return True
        else:
            previous = player.in_round(player.round_number - 1)
            check = [
                previous.field_maybe_none('error1_patron'),
                previous.field_maybe_none('error1_dictator'),
                previous.field_maybe_none('error1_receiver')
            ]

            count = 0
            for x in check:
                if x == 0 or x is None:
                    count += 1
            return count != 3

    @staticmethod
    def vars_for_template(player: Player):
        setup = C.SETUP[1]
        correct = correct_cal(setup["endowment"], setup["send"], setup["allocation"])
        return dict(
            num = 1,
            endowment = C.SETUP[1]["endowment"],
            send = C.SETUP[1]["send"],
            allocation = C.SETUP[1]["allocation"],
            answer_patron = player.quiz1_patron,
            answer_dictator = player.quiz1_dictator,
            answer_receiver = player.quiz1_receiver,
            correct_patron = correct["patron"],
            correct_dictator = correct["dictator"],
            correct_receiver = correct["receiver"],
            error_patron = player.error1_patron != 0,
            error_dictator = player.error1_dictator != 0,
            error_receiver = player.error1_receiver != 0,
            commentary = (
                'メンバーPはメンバーDの選択に関わらず、メンバーDに'
                + str(C.SETUP[1]["send"])
                + 'トークンを渡すので、自身のトークンは'
                + str(correct["patron"])
                + 'トークンとなります。メンバーDは受け取った'
                + str(C.SETUP[1]["send"])
                + 'トークンを'
                + str(C.SETUP[1]["allocation"])
                + '％にしてメンバーRに渡します。すなわち、メンバーDは'
                + str(correct["receiver"])
                + 'トークンをメンバーRに渡します。したがって、メンバーRに渡すトークンはメンバーPから受け取ったトークンで足りるので、メンバーDの最終的なトークンは'
                + str(correct["dictator"])
                + 'トークンのままです。また、メンバーRの最終的なトークンは'
                + str(correct["receiver"])
                + 'トークンです。'
            )
        )
    
    @staticmethod
    def js_vars(player: Player):
        return dict(page = 1)

class Answer2(Page):
    template_name = 'quiz/Answer.html'

    @staticmethod
    def is_displayed(player: Player):
        if player.round_number == 1:
            return True
        else:
            previous = player.in_round(player.round_number - 1)
            check = [
                previous.field_maybe_none('error2_patron'),
                previous.field_maybe_none('error2_dictator'),
                previous.field_maybe_none('error2_receiver')
            ]

            count = 0
            for x in check:
                if x == 0 or x is None:
                    count += 1
            return count != 3

    @staticmethod
    def vars_for_template(player: Player):
        setup = C.SETUP[2]
        correct = correct_cal(setup["endowment"], setup["send"], setup["allocation"])
        return dict(
            num = 2,
            endowment = C.SETUP[2]["endowment"],
            send = C.SETUP[2]["send"],
            allocation = C.SETUP[2]["allocation"],
            answer_patron = player.quiz2_patron,
            answer_dictator = player.quiz2_dictator,
            answer_receiver = player.quiz2_receiver,
            correct_patron = correct["patron"],
            correct_dictator = correct["dictator"],
            correct_receiver = correct["receiver"],
            error_patron = player.error2_patron != 0,
            error_dictator = player.error2_dictator != 0,
            error_receiver = player.error2_receiver != 0,
            commentary = (
                'メンバーPはメンバーDの選択に関わらず、メンバーDに'
                + str(C.SETUP[2]["send"])
                + 'トークンを渡すので、自身のトークンは'
                + str(correct["patron"])
                + 'トークンとなります。メンバーDは受け取った'
                + str(C.SETUP[2]["send"])
                + 'トークンを'
                + str(C.SETUP[2]["allocation"])
                + '％にしてメンバーRに渡します。すなわち、メンバーDは'
                + str(correct["receiver"])
                + 'トークンをメンバーRに渡します。メンバーRに渡すトークンはメンバーPから受け取ったトークンで足りないので、メンバーDは不足分を自身が保有するトークンで補います。したがって、メンバーDの最終的なトークンは'
                + str(correct["dictator"])
                + 'トークンです。また、メンバーRの最終的なトークンは'
                + str(correct["receiver"])
                + 'トークンです。'
            )
        )
    
    @staticmethod
    def js_vars(player: Player):
        return dict(page = 2)

class Answer3(Page):
    template_name = 'quiz/Answer.html'

    @staticmethod
    def is_displayed(player: Player):
        if player.round_number == 1:
            return True
        else:
            previous = player.in_round(player.round_number - 1)
            check = [
                previous.field_maybe_none('error3_patron'),
                previous.field_maybe_none('error3_dictator'),
                previous.field_maybe_none('error3_receiver')
            ]

            count = 0
            for x in check:
                if x == 0 or x is None:
                    count += 1
            return count != 3

    @staticmethod
    def vars_for_template(player: Player):
        setup = C.SETUP[3]
        correct = correct_cal(setup["endowment"], setup["send"], setup["allocation"])
        return dict(
            num = 3,
            endowment = C.SETUP[3]["endowment"],
            send = C.SETUP[3]["send"],
            allocation = C.SETUP[3]["allocation"],
            answer_patron = player.quiz3_patron,
            answer_dictator = player.quiz3_dictator,
            answer_receiver = player.quiz3_receiver,
            correct_patron = correct["patron"],
            correct_dictator = correct["dictator"],
            correct_receiver = correct["receiver"],
            error_patron = player.error3_patron != 0,
            error_dictator = player.error3_dictator != 0,
            error_receiver = player.error3_receiver != 0,
            commentary = (
                'メンバーPはメンバーDの選択に関わらず、メンバーDに'
                + str(C.SETUP[3]["send"])
                + 'トークンを渡すので、自身のトークンは'
                + str(correct["patron"])
                + 'トークンとなります。メンバーDは受け取った'
                + str(C.SETUP[3]["send"])
                + 'トークンを'
                + str(C.SETUP[3]["allocation"])
                + '％にしてメンバーRに渡します。すなわち、メンバーDは'
                + str(correct["receiver"])
                + 'トークンをメンバーRに渡します。メンバーDがメンバーPから受け取ったトークンをメンバーRに渡しても、メンバーPから受け取ったトークンに余りが生じるので、余ったトークンはメンバーDのトークンになります。したがって、メンバーDの最終的なトークンは'
                + str(correct["dictator"])
                + 'トークンです。また、メンバーRの最終的なトークンは'
                + str(correct["receiver"])
                + 'トークンです。'
            )
        )
    
    @staticmethod
    def js_vars(player: Player):
        return dict(page = 3)

class Finish(Page):
    @staticmethod
    def is_displayed(player: Player):
        check = [
            player.field_maybe_none('error1_patron'),
            player.field_maybe_none('error2_patron'),
            player.field_maybe_none('error3_patron'),
            player.field_maybe_none('error1_dictator'),
            player.field_maybe_none('error2_dictator'),
            player.field_maybe_none('error3_dictator'),
            player.field_maybe_none('error1_receiver'),
            player.field_maybe_none('error2_receiver'),
            player.field_maybe_none('error3_receiver')
        ]

        count = 0
        for x in check:
            if x == 0 or x is None:
                count += 1
        
        return count == C.NUMBER_Q * 3
    
    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return upcoming_apps[0]


page_sequence = [
    Introduction,
    Quiz1,
    Quiz2,
    Quiz3,
    Answer1,
    Answer2,
    Answer3,
    Finish
]
