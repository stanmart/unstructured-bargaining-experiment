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


PROD_FCT = {
    "{P2, P3}": 0,
    "{P1, P2}, {P1, P3}": 50,
    "Everyone": 100,
}


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
            prod_fct=list(PROD_FCT.values()),
            prod_fct_labels=list(PROD_FCT.keys()),
            my_id=1,
        )


class Coalitions(Page):
    @staticmethod
    def js_vars(player: Player):
        return dict(
            my_id=1,
        )


class Payment(Page):
    pass


page_sequence = [Welcome, Instructions, Proposal, Coalitions, Payment]
