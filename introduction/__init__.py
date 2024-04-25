from otree.api import BaseConstants, BaseGroup, BasePlayer, BaseSubsession, Page

doc = """
A welcome page with some information about the experiment, followed by instructions about the game.
The instructions involve a number of interactive exercises to make sure that the participants understand the game.
"""


class C(BaseConstants):
    NAME_IN_URL = "introduction"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# FUNCTIONS

# PAGES


class Welcome(Page):
    pass


class Instructions(Page):
    pass


class Proposal(Page):
    @staticmethod
    def js_vars(player: Player):
        return dict(
            prod_fct=list(player.session.config["prod_fct"].values()),
            prod_fct_labels=list(player.session.config["prod_fct"].keys()),
            my_id=1,
            player_names=player.session.config["player_names"],
        )

    @staticmethod
    def vars_for_template(player: Player):
        return player.session.config["player_names"]


class Coalitions(Page):
    @staticmethod
    def js_vars(player: Player):
        return dict(
            my_id=1,
            player_names=player.session.config["player_names"],
        )

    @staticmethod
    def vars_for_template(player: Player):
        return player.session.config["player_names"]


class Payment(Page):
    pass


page_sequence = [Welcome, Instructions, Proposal, Coalitions, Payment]
