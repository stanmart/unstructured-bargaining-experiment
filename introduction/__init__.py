from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, Page


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
    pass


class Coalitions(Page):
    pass


page_sequence = [Welcome, Instructions, Proposal, Coalitions]
