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

doc = """
A short survey at the end of the experiment.
Includes questions about demographics, players' strategies, preferences, and some feedback on the game itself.
The final page displays payoffs and instructions on how to proceed.
"""


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
            "No opinion",
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
            "No opinion",
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
            "No opinion",
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
            "No opinion",
        ],
        label="Did you feel there was enough time for the bargaining?",
        widget=widgets.RadioSelectHorizontal,
    )  # type: ignore

    research_question = models.StringField(
        label="What do you think is the research question we are studying in this experiment?",
        blank=True,
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
            "No opinion",
        ],
        label="If adding a certain player to a group never increases the budget, this player should get nothing.",
        widget=widgets.RadioSelectHorizontal,
    )  # type: ignore

    symmetry_axiom = models.StringField(
        choices=[
            "Strongly Disagree",
            "Disagree",
            "Neutral",
            "Agree",
            "Strongly Agree",
            "No opinion",
        ],
        label="If adding a certain player to a group always has the same impact on the budget as adding a certain other player, then both players should get the same payoff.",
        widget=widgets.RadioSelectHorizontal,
    )  # type: ignore

    efficiency_axiom = models.StringField(
        choices=[
            "Strongly Disagree",
            "Disagree",
            "Neutral",
            "Agree",
            "Strongly Agree",
            "No opinion",
        ],
        label="At the end of a bargaining round the biggest possible budget (100 points) should be paid out. ",
        widget=widgets.RadioSelectHorizontal,
    )  # type: ignore

    linearity_additivity_axiom = models.StringField(
        choices=[
            "Strongly Disagree",
            "Disagree",
            "Neutral",
            "Agree",
            "Strongly Agree",
            "No opinion",
        ],
        label="Suppose in round 3 the group budgets are the sum of the group budgets in round 1 and 2, for any group. Then the payoff of a player should the be the sum of the payoff that that player got in round 1 and 2.",
        widget=widgets.RadioSelectHorizontal,
    )  # type: ignore

    linearity_HD1_axiom = models.StringField(
        choices=[
            "Strongly Disagree",
            "Disagree",
            "Neutral",
            "Agree",
            "Strongly Agree",
            "No opinion",
        ],
        label="Suppose in round 2 each group budget is twice as large as in in round 1. Then the payoff of a player should be double the amount that player got in round 1.",
        widget=widgets.RadioSelectHorizontal,
    )  # type: ignore

    stability_axiom = models.StringField(
        choices=[
            "Strongly Disagree",
            "Disagree",
            "Neutral",
            "Agree",
            "Strongly Agree",
            "No opinion",
        ],
        label="If two players would have a budget of B points if they formed a group on their own, then the payoff of both players should sum up to at least B points in total in the final accepted proposal.",
        widget=widgets.RadioSelectHorizontal,
    )  # type: ignore


# FUNCTIONS
def compute_final_payoffs(player: Player):
    player.participant.final_payoff = ceil(
        player.participant.payoff_plus_participation_fee()
    )


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
        "research_question",
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
                f"Round {i}: {round_payoff:.2f} points"
                for i, round_payoff in enumerate(player.participant.payoff_list)  # type: ignore
                if i > 0
            ],
            "num_of_rounds": len(player.participant.payoff_list) - 1,
            "avg_payoff": float(player.participant.payoff) / 4,
            "converted_bargaining_payoff": ceil(
                player.participant.payoff.to_real_world_currency(player.session)
            ),
        }


page_sequence = [Questions, Completion]
