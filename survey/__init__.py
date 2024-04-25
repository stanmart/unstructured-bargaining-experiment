from math import ceil

from otree.api import (
    BaseConstants,
    BaseGroup,
    BasePlayer,
    BaseSubsession,
    Page,
    WaitPage,
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
        choices=[["Male", "Male"], ["Female", "Female"], ["Other", "Other"]],
        label="What is your gender?",
        widget=widgets.RadioSelect,
    )  # type: ignore
    degree = models.StringField(
        choices=[
            ["Bachelor", "Bachelor"],
            ["Master", "Master"],
            ["PhD", "PhD"],
            ["Other", "Other"],
        ],
        label="What is your current degree?",
        widget=widgets.RadioSelect,
    )  # type: ignore
    study_field = models.StringField(
        label="""
        What is your field of study?"""
    )  # type: ignore
    nationality = models.StringField(
        label="""
        What is your nationality?"""
    )  # type: ignore
    reflection = models.LongStringField(
        label="""
        What was your bargaining strategy and why? What did you think about the behavior of the other players?"""  # noqa: E501
    )  # type: ignore

    # TODO: delete for the main experiment
    pilot_difficulty = models.StringField(
        label="""
        How would you rate the difficulty level of the game?"""
    )  # type: ignore
    pilot_explanation = models.StringField(
        label="""
        How well was the game explained? What parts were unclear to you? What would you change in the explanation?"""  # noqa: E501
    )  # type: ignore
    pilot_interface = models.StringField(
        label="""
        How well could you work with the bargaining interface? What parts would you change?"""  # noqa: E501
    )  # type: ignore
    pilot_time = models.StringField(
        label="""
        Did you feel there was enough time for the bargaining? How much would you have preferred?"""  # noqa: E501
    )  # type: ignore

    comments = models.LongStringField(
        label="""
        Any additional comments you want to share with us?"""
    )  # type: ignore


# FUNCTIONS
def compute_final_payoffs(subsession: Subsession):
    players = subsession.get_players()
    # get number of (non-trial) bargaining rounds
    for player in players:
        player.participant.payoff = cu(ceil(player.participant.payoff))
        player.participant.final_payoff = (
            player.participant.payoff_plus_participation_fee()
        )


# PAGES


class Questions(Page):
    form_model = "player"
    form_fields = [
        "age",
        "gender",
        "degree",
        "study_field",
        "nationality",
        "reflection",
        "pilot_difficulty",
        "pilot_explanation",
        "pilot_interface",
        "pilot_time",
        "comments",
    ]


class WaitForAll(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = compute_final_payoffs  # type: ignore
    # compute_final_payoffs expects a Subsession as input
    # because of wait_for_all_groups = True


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


page_sequence = [Questions, WaitForAll, Completion]
