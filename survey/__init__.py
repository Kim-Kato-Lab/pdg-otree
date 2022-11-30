from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    ## Questionnaire items
    STRING_CHOICE = {
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
    INT_RANGE = {
        "field": models.IntegerField,
        "items": {
            "age": {
                "question": 'あなたの年齢をお答えください。',
                "min": 0,
                "max": None
            },
            "donation": {
                "question": '''
                あなたは今500円を持っている状況を想像してください。
                手持ちの500円からいくらまでならその慈善団体に寄付してもよいですか。
                <br>
                寄付する金額を1円刻みで考えて、入力してください。
                寄付したくない場合は0円を入力してください。''',
                "min": 0,
                "max": 500
            }
        }
    }
    INT_CHOICE = {
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
            "past_donation": {
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
            "past_volunteer": {
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
            },
            "matching_donation": {
                "question": '''
                ここで、ある財団の協力を得て、マッチングギフトの仕組みが導入されることになりました。
                <br>
                この仕組みは「<b>あなたの選択する寄付額と同じ額を、その財団が上乗せして、2倍の額が寄付先に届けられる</b>」というものです。
                <br>
                <b>この仕組みが導入されたとき</b>、あなたは前問で回答した寄付額を変えますか。
                最も近いものを一つ選んでください。''',
                "choice": [
                    [1, '減らす'],
                    [2, '変えない'],
                    [3, '増やす']
                ]
            }
        }
    }
    LIKERT = {
        "field": models.IntegerField,
        "choice": [
            [5, 'ぴったり当てはまる'],
            [4, 'どちらかというと当てはまる'],
            [3, 'どちらともいえない'],
            [2, 'どちらかというと当てはまらない'],
            [1, '全く当てはまらない']
        ],
        "question": {
            "trust": '一般的に言って、人はだいたい信頼できる',
            "altruistic": '他の人のためになること（公園のゴミ拾いなど）をすると自分もうれしい',
            "conformity": '周りの人と同じような行動をとっていると安心だ',
            "norm": '列で並んでいるところに割り込むことは絶対にしない',
            "positive_reciprocity": '以前親切にしてくれた人には苦労をいとわず手助けをする',
            "negative_reciprocity": '誰かが私の機嫌を損ねたら、私もやり返す'
        }
    }
    INEQUALITY = {
        "field": models.IntegerField,
        "choice": [
            [0, '配分パターンA'],
            [1, '配分パターンB']
        ],
        "question": {
            "inequality1": '''
            ケース1
            <br>
            配分パターンA：あなたは10,000円、他人は10,000円もらう
            <br>
            配分パターンB：あなたは10,000円、他人は6,000円もらう''',
            "inequality2": '''
            ケース2
            <br>
            配分パターンA：あなたは10,000円、他人は10,000円もらう
            <br>
            配分パターンB：あなたは16,000円、他人は4,000円もらう''',
            "inequality3": '''
            ケース3
            <br>
            配分パターンA：あなたは10,000円、他人は10,000円もらう
            <br>
            配分パターンB：あなたは10,000円、他人は18,000円もらう''',
            "inequality4": '''
            ケース4
            <br>
            配分パターンA：あなたは10,000円、他人は10,000円もらう
            <br>
            配分パターンB：あなたは11,000円、他人は19,000円もらう'''
        }
    }

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass

for k, v in C.STRING_CHOICE["items"].items():
    setattr(
        Player,
        k,
        C.STRING_CHOICE["field"](label = v["question"], choices = v["choice"])
    )

for k, v in C.INT_RANGE["items"].items():
    setattr(
        Player,
        k,
        C.INT_RANGE["field"](label = v["question"], min = v["min"], max = v["max"])
    )

for k, v in C.INT_CHOICE["items"].items():
    setattr(
        Player,
        k,
        C.INT_CHOICE["field"](label = v["question"], choices = v["choice"])
    )

for k, v in C.LIKERT["question"].items():
    setattr(
        Player,
        k,
        C.LIKERT["field"](label = v, choices = C.LIKERT["choice"])
    )

for k, v in C.INEQUALITY["question"].items():
    setattr(
        Player,
        k,
        C.INEQUALITY["field"](label = v, choices = C.INEQUALITY["choice"])
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
    form_fields = [
        'past_donation',
        'past_volunteer'
    ]

class Likert(Page):
    form_model = 'player'
    form_fields = C.LIKERT["question"].keys()

class MatchingDonation1(Page):
    form_model = 'player'
    form_fields = ['donation']

class MatchingDonation2(Page):
    form_model = 'player'
    form_fields = ['matching_donation']

class Allocation(Page):
    form_model = 'player'
    form_fields = C.INEQUALITY["question"].keys()

page_sequence = [
    Demographic,
    Economist,
    Altruist,
    Likert,
    MatchingDonation1,
    MatchingDonation2,
    Allocation
]
