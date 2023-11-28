from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'quiz'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
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
        'q' + str(k) +'_p',
        models.IntegerField(
            label = '''
            メンバーPの最終的な獲得トークンはいくらですか？
            0～200の整数（半角数字）で解答してください。''',
            min = 0, max = 200
        )
    )
    setattr(
        Player,
        'q' + str(k) +'_d',
        models.IntegerField(
            label = '''
            メンバーDの最終的な獲得トークンはいくらですか？
            0～200の整数（半角数字）で解答してください。''',
            min = 0, max = 200
        )
    )
    setattr(
        Player,
        'q' + str(k) +'_r',
        models.IntegerField(
            label = '''
            メンバーRの最終的な獲得トークンはいくらですか？
            0～200の整数（半角数字）で解答してください。''',
            min = 0, max = 200
        )
    )
    setattr(
        Player,
        'err' + str(k) + '_p',
        models.IntegerField()
    )
    setattr(
        Player,
        'err' + str(k) + '_d',
        models.IntegerField()
    )
    setattr(
        Player,
        'err' + str(k) + '_r',
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
    pass

class Quiz1(Page):
    template_name = 'quiz/Quiz.html'

    form_model = 'player'
    form_fields = ['q1_p', 'q1_d', 'q1_r']

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
        player.err1_p = correct["patron"] - player.q1_p
        player.err1_d = correct["dictator"] - player.q1_d
        player.err1_r = correct["receiver"] - player.q1_r
    
    @staticmethod
    def js_vars(player: Player):
        return dict(page = 1)


class Quiz2(Page):
    template_name = 'quiz/Quiz.html'
    
    form_model = 'player'
    form_fields = ['q2_p', 'q2_d', 'q2_r']

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
        player.err2_p = correct["patron"] - player.q2_p
        player.err2_d = correct["dictator"] - player.q2_d
        player.err2_r = correct["receiver"] - player.q2_r
    
    @staticmethod
    def js_vars(player: Player):
        return dict(page = 2)

class Quiz3(Page):
    template_name = 'quiz/Quiz.html'

    form_model = 'player'
    form_fields = ['q3_p', 'q3_d', 'q3_r']

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
        player.err3_p = correct["patron"] - player.q3_p
        player.err3_d = correct["dictator"] - player.q3_d
        player.err3_r = correct["receiver"] - player.q3_r
    
    @staticmethod
    def js_vars(player: Player):
        return dict(page = 3)

class Answer1(Page):
    template_name = 'quiz/Answer.html'

    @staticmethod
    def vars_for_template(player: Player):
        setup = C.SETUP[1]
        correct = correct_cal(setup["endowment"], setup["send"], setup["allocation"])
        return dict(
            num = 1,
            endowment = C.SETUP[1]["endowment"],
            send = C.SETUP[1]["send"],
            allocation = C.SETUP[1]["allocation"],
            answer_patron = player.q1_p,
            answer_dictator = player.q1_d,
            answer_receiver = player.q1_r,
            correct_patron = correct["patron"],
            correct_dictator = correct["dictator"],
            correct_receiver = correct["receiver"],
            error_patron = player.err1_p != 0,
            error_dictator = player.err1_d != 0,
            error_receiver = player.err1_r != 0,
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
    def vars_for_template(player: Player):
        setup = C.SETUP[2]
        correct = correct_cal(setup["endowment"], setup["send"], setup["allocation"])
        return dict(
            num = 2,
            endowment = C.SETUP[2]["endowment"],
            send = C.SETUP[2]["send"],
            allocation = C.SETUP[2]["allocation"],
            answer_patron = player.q2_p,
            answer_dictator = player.q2_d,
            answer_receiver = player.q2_r,
            correct_patron = correct["patron"],
            correct_dictator = correct["dictator"],
            correct_receiver = correct["receiver"],
            error_patron = player.err2_p != 0,
            error_dictator = player.err2_d != 0,
            error_receiver = player.err2_r != 0,
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
    def vars_for_template(player: Player):
        setup = C.SETUP[3]
        correct = correct_cal(setup["endowment"], setup["send"], setup["allocation"])
        return dict(
            num = 3,
            endowment = C.SETUP[3]["endowment"],
            send = C.SETUP[3]["send"],
            allocation = C.SETUP[3]["allocation"],
            answer_patron = player.q3_p,
            answer_dictator = player.q3_d,
            answer_receiver = player.q3_r,
            correct_patron = correct["patron"],
            correct_dictator = correct["dictator"],
            correct_receiver = correct["receiver"],
            error_patron = player.err3_p != 0,
            error_dictator = player.err3_d != 0,
            error_receiver = player.err3_r != 0,
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
    pass
    # @staticmethod
    # def app_after_this_page(player: Player, upcoming_apps):
    #     return upcoming_apps[0]


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
