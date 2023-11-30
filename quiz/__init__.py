from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'quiz'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    SETUP = {
        "case 1": {
            "endowment": 100,
            "send": 50,
            "allocation": 200
        },
        "case 2": {
            "endowment": 100,
            "send": 50,
            "allocation": 50
        }
    }
class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    q1 = models.IntegerField(
        min=0, max=200,
        label = '''
        メンバーＰの最終的な獲得トークンはいくらですか？
        0～200の整数（半角数字）で解答してください。'''
    )
    q2 = models.IntegerField(
        min=0, max=200,
        label = '''
        メンバーＤの最終的な獲得トークンはいくらですか？
        0～200の整数（半角数字）で解答してください。'''
    )
    q3 = models.IntegerField(
        min=0, max=200,
        label = '''
        メンバーＲの最終的な獲得トークンはいくらですか？
        0～200の整数（半角数字）で解答してください。'''
    )
    q4 = models.IntegerField(
        min=0, max=200,
        label = '''
        メンバーＲの最終的な獲得トークンはいくらですか？
        0～200の整数（半角数字）で解答してください。'''
    )
    err1 = models.IntegerField()
    err2 = models.IntegerField()
    err3 = models.IntegerField()
    err4 = models.IntegerField()

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

class Quiz(Page):
    template_name = 'quiz/Quiz.html'

    form_model = 'player'
    form_fields = ['q1', 'q2', 'q3', 'q4']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            endowment1 = C.SETUP['case 1']["endowment"],
            send1 = C.SETUP['case 1']["send"],
            allocation1 = C.SETUP['case 1']["allocation"],
            endowment2 = C.SETUP['case 2']["endowment"],
            send2 = C.SETUP['case 2']["send"],
            allocation2 = C.SETUP['case 2']["allocation"]
        )
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        setup1 = C.SETUP['case 1']
        setup2 = C.SETUP['case 2']
        correct1 = correct_cal(setup1["endowment"], setup1["send"], setup1["allocation"])
        correct2 = correct_cal(setup2["endowment"], setup2["send"], setup2["allocation"])
        player.err1 = correct1["patron"] - player.q1
        player.err2 = correct1["dictator"] - player.q2
        player.err3 = correct1["receiver"] - player.q3
        player.err4 = correct2["receiver"] - player.q4

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
    Quiz,
    Answer1,
    Answer2,
    Answer3,
    Finish
]
