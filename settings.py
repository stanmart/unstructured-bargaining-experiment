from os import environ

# Note: session config is not as flexible as it seems.
# The production function must be of length 2 and 3.
# 3 assumes that P1 is the big player and P2 and P3 are the small players.
# 2 assumes that P1 and P2 symmetric P3 is a dummy player.

SESSION_CONFIGS = [
    dict(
        name="treatment_y_10",
        display_name="Treatment: Y=10",
        app_sequence=["introduction", "live_bargaining", "survey"],
        num_demo_participants=3,
        seconds_per_round=5 * 60,
        prod_fct={
            "B1+B2": 0,
            "A+B1<br>A+B2": 10,
            "A+B1+B2": 100,
        },
        player_names={
            "P1": "A",
            "P2": "B1",
            "P3": "B2",
        },
        doc="Treatment with production function [0, 10, 100]",
    ),
    dict(
        name="treatment_y_30",
        display_name="Treatment: Y=30",
        app_sequence=["introduction", "live_bargaining", "survey"],
        num_demo_participants=3,
        seconds_per_round=5 * 60,
        prod_fct={
            "B1+B2": 0,
            "A+B1<br>A+B2": 30,
            "A+B1+B2": 100,
        },
        player_names={
            "P1": "A",
            "P2": "B1",
            "P3": "B2",
        },
        doc="Treatment with production function [0, 30, 100]",
    ),
    dict(
        name="treatment_y_90",
        display_name="Treatment: Y=90",
        app_sequence=["introduction", "live_bargaining", "survey"],
        num_demo_participants=3,
        seconds_per_round=5 * 60,
        prod_fct={
            "B1+B2": 0,
            "A+B1<br>A+B2": 90,
            "A+B1+B2": 100,
        },
        player_names={
            "P1": "A",
            "P2": "B1",
            "P3": "B2",
        },
        doc="Treatment with production function [0, 90, 100]",
    ),
    dict(
        name="treatment_dummy_player",
        display_name="Treatment: Dummy Player",
        app_sequence=["introduction", "live_bargaining", "survey"],
        num_demo_participants=3,
        seconds_per_round=5 * 60,
        prod_fct={
            "A1+B<br>A2+B": 0,
            "A1+A2<br>A1+A2+B": 100,
        },
        player_names={
            "P1": "A1",
            "P2": "A2",
            "P3": "B",
        },
        doc="Treatment with production function [0, 100] and P3 as dummy player",
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=10.00, doc=""
)

PARTICIPANT_FIELDS = [
    "final_payoff",
    "payoff_list",
]
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = "en"

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = "CHF"
USE_POINTS = False

ADMIN_USERNAME = "admin"
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get("OTREE_ADMIN_PASSWORD")

DEMO_PAGE_INTRO_HTML = """
<b>Welcome to the live bargaining experiment!</b>
Please choose one of the treatments on the left to start a demo session.
"""

SECRET_KEY = "5644004254536"

ROOMS = [
    dict(
        name="blu",
        display_name="BLU Econ Lab (secure URLs)",
        participant_label_file="_rooms/blu.txt",
        use_secure_urls=True,
    ),
    dict(
        name="blu_ns",
        display_name="BLU Econ Lab (non-secure URLs)",
        participant_label_file="_rooms/blu.txt",
        use_secure_urls=False,
    ),
]
