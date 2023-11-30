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
    check1 = models.IntegerField(initial=0)
    check2 = models.IntegerField(initial=0)
    check3 = models.IntegerField(initial=0)
    check4 = models.IntegerField(initial=0)

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

class Answer(Page):
    @staticmethod
    def live_method(player: Player, data):
        if data == "q1":
            if player.check1 == 0:
                player.check1 = 1
        elif data == "q2":
            if player.check2 == 0:
                player.check2 = 1
        elif data == "q3":
            if player.check3 == 0:
                player.check3 = 1
        elif data == "q4":
            if player.check4 == 0:
                player.check4 = 1
        
        check = player.check1 + player.check2 + player.check3 + player.check4
        if check == 4:
            return {player.id_in_group: 'go'}
        else:
            return {player.id_in_group: 'stop'}

    @staticmethod
    def vars_for_template(player: Player):
        setup1 = C.SETUP['case 1']
        setup2 = C.SETUP['case 2']
        correct1 = correct_cal(setup1["endowment"], setup1["send"], setup1["allocation"])
        correct2 = correct_cal(setup2["endowment"], setup2["send"], setup2["allocation"])

        return dict(
            endowment1 = setup1["endowment"],
            send1 = setup1["send"],
            allocation1 = setup1["allocation"],
            endowment2 = setup2["endowment"],
            send2 = setup2["send"],
            allocation2 = setup2["allocation"],
            correct_q1 = correct1["patron"],
            correct_q2 = correct1["dictator"],
            correct_q3 = correct1["receiver"],
            correct_q4 = correct2["receiver"],
            change_d_1 = correct1["receiver"] - setup1["send"],
            change_d_2 = setup2["send"] - correct2["receiver"],
            correct2 = correct2
        )

class Finish(Page):
    pass
    # @staticmethod
    # def app_after_this_page(player: Player, upcoming_apps):
    #     return upcoming_apps[0]


page_sequence = [
    Introduction,
    Quiz,
    Answer,
    Finish
]
