from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    male = models.BooleanField(
        label = 'あなたの性別をお答えください。',
        choices = [
            [False, '女性'],
            [True, '男性']
        ],
        widget = widgets.RadioSelect
    )
    age = models.IntegerField(
        label = 'あなたの年齢をお答えください。',
        min = 18
    )
    academic_year = models.IntegerField(
        label = 'あなたの学年をお答えください。',
        choices = [
            [1, '学部1年'],
            [2, '学部2年'],
            [3, '学部3年'],
            [4, '学部4年']
        ]
    )
    academic_field = models.IntegerField(
        label = '''あなたはどの学部に所属していますか。
        最も近いものを一つ選んでください。''',
        choices = [
            [1, '自然科学系（物理・工学・数学・医学など）'],
            [2, '社会科学系（法学・政治学・経済学・社会学など）'],
            [3, '人文科学系（文学・心理学・歴史学など）']
        ]
    )
    economist = models.BooleanField(
        label = 'あなたは経済学部（もしくは経営学部）に所属していますか。',
        choices = [
            [True, 'はい'],
            [False, 'いいえ']
        ],
        widget = widgets.RadioSelect
    )
    experience = models.BooleanField(
        label = 'あなたはこれまで、なんらかの経済実験に参加したことはありますか。',
        choices = [
            [False, 'いいえ'],
            [True, 'はい']
        ],
        widget = widgets.RadioSelect
    )
    donation = models.IntegerField(
        label = '''
        あなたは、この1年間に、<b>金銭による寄付</b>を何円くらいしましたか。
        <br>
        ※金銭による寄付とは、あなた自身や家族のためではなく、
        広く公共的・公益的な活動やその活動を行っている団体に対して、金銭を自発的に提供する行為のことを言います。''',
        choices = [
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
    )
    volunteer = models.IntegerField(
        label = '''
        あなたは、この1年間に、<b>ボランティア活動</b>をどのくらいしましたか。
        <br>
        ※ボランティア活動とは、あなた自身や家族のためではなく、
        他人や社会のために自発的に労務を提供する行為のことを言います。
        交通費などの経費が支払われるものも含まれます。
        また、オンラインやリモートで出来るものも含まれます。''',
        choices = [
            [1, 'ボランティア活動をしなかった'],
            [2, '年に1回'],
            [3, '年に数回'],
            [4, '月に1回'],
            [5, '月に数回'],
            [6, '週に1回'],
            [7, '週に数回'],
            [8, 'ほとんど毎日']
        ]
    )

# FUNCTIONS
# PAGES

class Demographic(Page):
    template_name = 'survey/SimpleForm.html'

    form_model = 'player'
    form_fields = ['male', 'age']

class AcademicInfo(Page):
    template_name = 'survey/SimpleForm.html'

    form_model = 'player'
    form_fields = ['academic_year', 'academic_field']

class Economist(Page):
    template_name = 'survey/SimpleForm.html'

    form_model = 'player'
    form_fields = ['economist']

    @staticmethod
    def is_displayed(player: Player):
        return player.academic_field == 2

class Experience(Page):
    template_name = 'survey/SimpleForm.html'

    form_model = 'player'
    form_fields = ['experience']

class AltruisticAction(Page):
    template_name = 'survey/SimpleForm.html'

    form_model = 'player'
    form_fields = ['donation', 'volunteer']

page_sequence = [
    Demographic,
    AcademicInfo,
    Economist,
    Experience,
    AltruisticAction
]
