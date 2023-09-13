from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(label='What is your age?', min=13, max=125)
    gender = models.StringField(
        choices=[['Male', 'Male'], ['Female', 'Female'], ['Other', 'Other']],
        label='What is your gender?',
        widget=widgets.RadioSelect,
    )
    reflection = models.StringField(
        label='''
        What was your bargaining strategy and why? What did you think about the behavior of the other players?'''
    )
    comments = models.StringField(
        label='''
        Any additional comments you want to share with us?'''
    )
  

# FUNCTIONS
# PAGES
class Questions(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'reflection', 'comments']

class Completion(Page):
    pass

page_sequence = [Questions, Completion]