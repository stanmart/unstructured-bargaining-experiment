from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'introduction'
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

class Instructions2(Page):
    pass

class Instructions3(Page):
    pass

class Instructions4(Page):
    pass

page_sequence = [Welcome, Instructions, Instructions2, Instructions3, Instructions4]
