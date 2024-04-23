from otree.api import BaseConstants, BaseGroup, BasePlayer, BaseSubsession, Page


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
        )

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            small_coalition_value=list(player.session.config["prod_fct"].values())[1],
            grand_coalition_value=list(player.session.config["prod_fct"].values())[-1],
            last_player_is_dummy=len(player.session.config["prod_fct"])
            == 2,  # hardcoded group size
        )


class Coalitions(Page):
    @staticmethod
    def js_vars(player: Player):
        return dict(
            my_id=1,
            prod_fct=list(player.session.config["prod_fct"].values()),
        )


class Payment(Page):
    pass


page_sequence = [Welcome, Instructions, Proposal, Coalitions, Payment]
