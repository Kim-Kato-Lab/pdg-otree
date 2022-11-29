from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    ## Socio-economic items
    SOCIOECON_STR = {
        "field": models.StringField,
        "items": {
            "academic_field": {
                "question": 'あなたの学部は以下の三つの領域のうちどれに当てはまりますか。',
                "choice": [
                    ['humanities', '人文科学系（文学・心理学・歴史学など）'],
                    ['social', '社会科学系（法学・政治学・経済学・社会学など）'],
                    ['natural', '自然科学系（物理・工学・数学・医学など）']
                ]
            }
        }
    }
    SOCIOECON_INT = {
        "field": models.IntegerField,
        "items": {
            "age": {
                "question": 'あなたの年齢をお答えください。'
            }
        }
    }
    SOCIOECON_INT_CHOICE = {
        "field": models.IntegerField,
        "items": {
            "experience": {
                'question': 'あなたはこれまで、なんらかの経済実験に参加したことはありますか。',
                "choice": [
                    [0, 'いいえ'],
                    [1, 'はい']
                ]
            },
            "male": {
                "question": 'あなたの性別をお答えください。',
                "choice": [
                    [0, '女性'],
                    [1, '男性']
                ]
            },
            "foreigner": {
                "question": 'あなたは留学生ですか。',
                "choice": [
                    [1, 'はい'],
                    [0, 'いいえ']
                ]
            },
            "academic_year": {
                "question": 'あなたの学年をお答えください。',
                "choice": [
                    [1, "学部1年"],
                    [2, "学部2年"],
                    [3, "学部3年"],
                    [4, "学部4年"],
                ]
            },
            "economist": {
                "question": '''
                あなたの学部が「社会科学系（法学・政治学・経済学・社会学など）」と回答した方にお尋ねします。
                あなたが所属する学部は経済学部ですか。''',
                "choice": [
                    [0, 'いいえ（経済学部以外）'],
                    [1, 'はい（経済学部）']
                ]
            },
            "donation": {
                "question": '''
                あなたは、この1年間に、<b>金銭による寄付</b>を何円くらいしましたか。
                <br>
                ※金銭による寄付とは、あなた自身や家族のためではなく、
                広く公共的・公益的な活動やその活動を行っている団体に対して、
                金銭を自発的に提供する行為のことを言います。''',
                "choice": [
                    [1, '0円'],
                    [2, '1円～500円未満'],
                    [3, '500円～1,000円未満'],
                    [4, '1,000円～3,000円未満'],
                    [5, '3,000円～5,000円未満'],
                    [6, '5,000円～10,000円未満'],
                    [7, '10,000円～25,000円未満'],
                    [8, '25,000円～50,000円未満'],
                    [9, '50,000円以上']
                ]
            },
            "volunteer": {
                "question": '''
                あなたは、この1年間に、<b>ボランティア活動</b>をどのくらいしましたか。
                <br>
                ※ボランティア活動とは、あなた自身や家族のためではなく、
                他人や社会のために自発的に労務を提供する行為のことを言います。
                交通費などの経費が支払われるものも含まれます。
                また、オンラインやリモートで出来るものも含まれます。''',
                "choice": [
                    [1, 'ボランティア活動をしなかった'],
                    [2, '年に1回'],
                    [3, '年に数回'],
                    [4, '月に1回'],
                    [5, '月に数回'],
                    [6, '週に1回'],
                    [7, '週に数回'],
                    [8, 'ほとんど毎日']
                ]
            }
        }
    }

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass

for k, v in C.SOCIOECON_STR["items"].items():
    setattr(
        Player,
        k,
        C.SOCIOECON_STR["field"](label = v["question"], choices = v["choice"])
    )

for k, v in C.SOCIOECON_INT["items"].items():
    setattr(
        Player,
        k,
        C.SOCIOECON_INT["field"](label = v["question"])
    )

for k, v in C.SOCIOECON_INT_CHOICE["items"].items():
    setattr(
        Player,
        k,
        C.SOCIOECON_INT_CHOICE["field"](label = v["question"], choices = v["choice"])
    )

# FUNCTIONS
# PAGES

class Demographic(Page):
    template_name = 'survey/SimpleForm.html'

    form_model = 'player'
    form_fields = [
        'male',
        'foreigner',
        'experience',
        'age',
        'academic_year',
        'academic_field'
    ]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.academic_field != "social":
            player.economist = 0

class Economist(Page):
    template_name = 'survey/SimpleForm.html'

    form_model = 'player'
    form_fields = ['economist']

    @staticmethod
    def is_displayed(player: Player):
        return player.academic_field == "social"

class Altruist(Page):
    template_name = 'survey/SimpleForm.html'

    form_model = 'player'
    form_fields = ['donation', 'volunteer']

page_sequence = [
    Demographic,
    Economist,
    Altruist
]
