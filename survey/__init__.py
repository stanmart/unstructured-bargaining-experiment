from math import ceil

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
    study_field = models.StringField(label="What is your field of study?")  # type: ignore
    nationality = models.StringField(label="What is your nationality?")  # type: ignore
    own_strategy = models.LongStringField(
        label="What was your bargaining strategy and why?"
    )  # type: ignore
    other_players_strategy = models.LongStringField(
        label="What did you think about the behavior of the other players?"
    )  # type: ignore

    # TODO: delete for the main experiment
    pilot_difficulty = models.StringField(
        choices=[
            "Very easy",
            "Easy",
            "Medium difficulty",
            "Difficult",
            "Very difficult",
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
        ],
        label="Players who contribute nothing should receive nothing.",
        widget=widgets.RadioSelectHorizontal,
    )  # type: ignore

    symmetry_axiom = models.StringField(
        choices=[
            "Strongly Disagree",
            "Disagree",
            "Neutral",
            "Agree",
            "Strongly Agree",
        ],
        label="If two players contribute the same to the group's budget, they should receive the same payoff.",
        widget=widgets.RadioSelectHorizontal,
    )  # type: ignore

    efficiency_axiom = models.StringField(
        choices=[
            "Strongly Disagree",
            "Disagree",
            "Neutral",
            "Agree",
            "Strongly Agree",
        ],
        label="The whole available budget should be distributed (nothing should be left on the table).",
        widget=widgets.RadioSelectHorizontal,
    )  # type: ignore

    linearity_axiom = models.StringField(
        choices=[
            "Strongly Disagree",
            "Disagree",
            "Neutral",
            "Agree",
            "Strongly Agree",
        ],
        label="I don't know how to do linearity tbh...",
        widget=widgets.RadioSelectHorizontal,
    )  # type: ignore

    stability_axiom = models.StringField(
        choices=[
            "Strongly Disagree",
            "Disagree",
            "Neutral",
            "Agree",
            "Strongly Agree",
        ],
        label="If a smaller group has a budget of X, then their members should receive at least X in total.",
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
        "linearity_axiom",
        "stability_axiom",
        "age",
        "gender",
        "degree",
        "study_field",
        "nationality",
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
            num_axiom_questions=5,  # They need to come first in form_fields
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
