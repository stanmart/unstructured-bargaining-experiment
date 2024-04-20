from os import environ

SESSION_CONFIGS = [
    dict(
        name="live_bargaining",
        app_sequence=["introduction", "live_bargaining", "survey"],
        num_demo_participants=3,
    ),
    dict(
        name="bargaining_test",
        app_sequence=["live_bargaining"],
        num_demo_participants=3,
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

DEMO_PAGE_INTRO_HTML = """ """

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
