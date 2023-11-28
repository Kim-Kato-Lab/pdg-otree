from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'ja'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'JPY'
USE_POINTS = True
POINTS_CUSTOM_NAME = 'トークン'

PARTICIPANT_FIELDS = [
    'payoff_list',
    'game_payoff_list',
    'belief_payoff_list',
    'selected_round',
    'first_dictator'
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point = 5,
    participation_fee = 1000
)

    
SESSION_CONFIGS = [
    dict(
        name = 'quiz',
        display_name = 'PDG: Quiz',
        num_demo_participants = 1,
        app_sequence = ['quiz']
    ),
    dict(
        name = 'fd',
        display_name = 'PDG-FD',
        num_demo_participants = 3,
        dictator_first = True,
        timeout_seconds = None,
        app_sequence = [
            'move_exogenous',
            'payment_info'
        ]
    ),
    dict(
        name = 'sd',
        display_name = 'PDG-SD',
        num_demo_participants = 3,
        dictator_first = False,
        dictator_promise = False,
        allocation_contractible_odd = False,
        allocation_contractible_even = False,
        timeout_seconds = None,
        app_sequence = [
            'move_exogenous',
            'payment_info'
        ]
    ),
    dict(
        name = 'sd_promise',
        display_name = 'PDG-SD (promise)',
        num_demo_participants = 3,
        dictator_first = False,
        dictator_promise = True,
        allocation_contractible_odd = False,
        allocation_contractible_even = False,
        timeout_seconds = None,
        app_sequence = [
            'move_exogenous',
            'payment_info'
        ]
    ),
    dict(
        name = 'sd_contractible_odd',
        display_name = 'PDG-SD (contractible; odd rounds)',
        num_demo_participants = 3,
        dictator_first = False,
        allocation_contractible_odd = True,
        allocation_contractible_even = False,
        timeout_seconds = None,
        app_sequence = [
            'move_exogenous',
            'payment_info'
        ]
    ),
    dict(
        name = 'sd_contractible_even',
        display_name = 'PDG-SD (contractible; even rounds)',
        num_demo_participants = 3,
        dictator_first = False,
        allocation_contractible_odd = False,
        allocation_contractible_even = True,
        timeout_seconds = 5,
        app_sequence = [
            'move_exogenous',
            'payment_info'
        ]
    ),
    dict(
        name = 'dictator',
        display_name = 'DG treatment',
        num_demo_participants = 4,
        timeout_seconds = None, # if you want to run experiments without time-out, then specify `None`
        app_sequence = [
            'dictator',
            'payment_info'
        ]
    )
]

ROOMS = [
    dict(
        name='socio',
        display_name='Research Institute for Socionetwork Strategies (Kansai University)',
        participant_label_file='_rooms/socio.txt'
    )
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Economic Experiments developed by Hiroki Kato.
Source code can be found at <a href='https://github.com/KatoPachi'>Github</a>
"""
# don't share this with anybody.
SECRET_KEY = environ.get('OTREE_SECRET_KEY')