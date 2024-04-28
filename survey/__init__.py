from math import ceil

from country_list import countries_for_language

from otree.api import (
    BaseConstants,
    BaseGroup,
    BasePlayer,
    BaseSubsession,
    Page,
    cu,
    models,
    widgets,
)


class C(BaseConstants):
    pass
    NAME_IN_URL = "survey"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(label="What is your age?", min=13, max=125)  # type: ignore
    gender = models.StringField(
        choices=["Male", "Female", "Other"],
        label="What is your gender?",
        widget=widgets.RadioSelectHorizontal,
    )  # type: ignore
    gender_other = models.StringField(
        label="If you selected 'Other', would you like to specify?",
        blank=True,
    )  # type: ignore
    degree = models.StringField(
        choices=[
            "Bachelor",
            "Master",
            "PhD",
            "Other",
        ],
        label="What is the degree you are currently pursuing?",
        widget=widgets.RadioSelectHorizontal,
    )  # type: ignore
    degree_other = models.StringField(
        label="If you selected 'Other', please specify",
        blank=True,
    )  # type: ignore
    study_field = models.StringField(
        choices=[
            "Accounting",
            "Agriculture",
            "Anthropology",
            "Archaeology",
            "Architecture",
            "Business Administration",
            "Biology",
            "Business",
            "Chemistry",
            "Computer sciences",
            "Economics",
            "Education",
            "Engineering",
            "Environmental studies",
            "Finance",
            "Geography",
            "History",
            "Media studies and communication",
            "Law",
            "Linguistics",
            "Literature",
            "Mathematics",
            "Medicine",
            "Philosophy",
            "Physics",
            "Political science",
            "Psychology",
            "Public administration and policy",
            "Religious studies",
            "Sociology",
            "Statistics",
            "Other",
        ],
        label="What is your field of study?",
    )  # type: ignore
    study_field_other = models.StringField(
        label="If you selected 'Other', please specify",
        blank=True,
    )  # type: ignore
    nationality = models.StringField(
        label="What is your nationality?",
        choices=countries_for_language("en"),
    )  # type: ignore
    has_second_nationality = models.BooleanField(
        label="Do you have a second nationality?",  # type: ignore
        widget=widgets.RadioSelectHorizontal,  # type: ignore
        initial=False,  # type: ignore
    )  # type: ignore
    second_nationality = models.StringField(
        label="What is your second nationality?",
        choices=countries_for_language("en"),
        blank=True,
    )  # type: ignore
    own_strategy = models.LongStringField(
        label="What was your bargaining strategy and why?"
    )  # type: ignore
    other_players_strategy = models.LongStringField(
        label="What did you think about the behavior of the other players? What do you think their strategy was?"
    )  # type: ignore

    # TODO: delete for the main experiment
    pilot_difficulty = models.StringField(
        choices=[
            "Very easy",
            "Easy",
            "Medium difficulty",
            "Difficult",
            "Very difficult",
            "Prefer not to say",
        ],
        label="How would you rate the difficulty level of the game?",
        widget=widgets.RadioSelectHorizontal,
    )  # type: ignore
    pilot_explanation = models.StringField(
        choices=[
            "Very poorly",
            "Poorly",
            "Neutral",
            "Well",
            "Very well",
            "Prefer not to say",
        ],
        label="How well was the game explained?",
        widget=widgets.RadioSelectHorizontal,
    )  # type: ignore
    pilot_interface = models.StringField(
        choices=[
            "Very poorly",
            "Poorly",
            "Neutral",
            "Well",
            "Very well",
            "Prefer not to say",
        ],
        label="How well could you work with the bargaining interface?",
        widget=widgets.RadioSelectHorizontal,
    )  # type: ignore
    pilot_time = models.StringField(
        choices=[
            "Way too little",
            "Too little",
            "Just right",
            "Too much",
            "Way too much",
            "Prefer not to say",
        ],
        label="Did you feel there was enough time for the bargaining?",
        widget=widgets.RadioSelectHorizontal,
    )  # type: ignore

    comments = models.LongStringField(
        label="Any additional comments you want to share with us?",
        blank=True,
    )  # type: ignore

    dummy_player_axiom = models.StringField(
        choices=[
            "Strongly Disagree",
            "Disagree",
            "Neutral",
            "Agree",
            "Strongly Agree",
            "Prefer not to say",
        ],
        label="If adding player X to a group never increases the budget, player X should get nothing. ",
        widget=widgets.RadioSelectHorizontal,
    )  # type: ignore

    symmetry_axiom = models.StringField(
        choices=[
            "Strongly Disagree",
            "Disagree",
            "Neutral",
            "Agree",
            "Strongly Agree",
            "Prefer not to say",
        ],
        label="If adding player X to a group always has the same impact on the budget as adding player Y, then player X and player Y should get the same payoff.",
        widget=widgets.RadioSelectHorizontal,
    )  # type: ignore

    efficiency_axiom = models.StringField(
        choices=[
            "Strongly Disagree",
            "Disagree",
            "Neutral",
            "Agree",
            "Strongly Agree",
            "Prefer not to say",
        ],
        label="The payoffs at the end of a bargaining round should always add up to the biggest possible budget (100 CHF). ",
        widget=widgets.RadioSelectHorizontal,
    )  # type: ignore

    linearity_additivity_axiom = models.StringField(
        choices=[
            "Strongly Disagree",
            "Disagree",
            "Neutral",
            "Agree",
            "Strongly Agree",
            "Prefer not to say",
        ],
        label="Suppose in round 3 the budget each group (out of the three players) can get is the sum of the budget it can get in round 1 and 2. Then the payoff of player X should the be the sum of the payoff player X got in round 1 and 2.",
        widget=widgets.RadioSelectHorizontal,
    )  # type: ignore

    linearity_HD1_axiom = models.StringField(
        choices=[
            "Strongly Disagree",
            "Disagree",
            "Neutral",
            "Agree",
            "Strongly Agree",
            "Prefer not to say",
        ],
        label="Suppose in round 2 each group of players has double the budget they can get in round 1. Then the payoff of player X should be double the amount player X got in round 1.",
        widget=widgets.RadioSelectHorizontal,
    )  # type: ignore

    stability_axiom = models.StringField(
        choices=[
            "Strongly Disagree",
            "Disagree",
            "Neutral",
            "Agree",
            "Strongly Agree",
            "Prefer not to say",
        ],
        label="If player X and player Y would have a budget of Z if they formed a group on their own, then the payoffs of player X and Y should be at least Z in total in the final accepted proposal.",
        widget=widgets.RadioSelectHorizontal,
    )  # type: ignore


# FUNCTIONS
def compute_final_payoffs(player: Player):
    player.participant.payoff = cu(ceil(player.participant.payoff))
    player.participant.final_payoff = player.participant.payoff_plus_participation_fee()


# PAGES


class Questions(Page):
    form_model = "player"
    form_fields = [
        "dummy_player_axiom",
        "symmetry_axiom",
        "efficiency_axiom",
        "linearity_additivity_axiom",
        "linearity_HD1_axiom",
        "stability_axiom",
        "age",
        "gender",
        "gender_other",
        "degree",
        "degree_other",
        "study_field",
        "study_field_other",
        "nationality",
        "has_second_nationality",
        "second_nationality",
        "own_strategy",
        "other_players_strategy",
        "pilot_difficulty",
        "pilot_explanation",
        "pilot_interface",
        "pilot_time",
        "comments",
    ]

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            num_axiom_questions=6,  # They need to come first in form_fields
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        compute_final_payoffs(player)


class Completion(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return {
            "all_payoffs": [
                f"Round {i}: CHF{round_payoff:.2f}"
                for i, round_payoff in enumerate(player.participant.payoff_list)  # type: ignore
                if i > 0
            ],
            "num_of_rounds": len(player.participant.payoff_list) - 1,
        }


page_sequence = [Questions, Completion]
