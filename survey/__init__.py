from otree.api import *
from random import randint

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
def compute_final_payoffs(subsession: Subsession):
    
    players = subsession.get_players()
    # get number of bargaining rounds
    player0_payoffs = [players[0].participant.vars['payoff_round' + str(i)] for i in range(1,6)]
    number_of_bargaining_rounds = sum(elem >= 0 for elem in player0_payoffs)
    payment_round = randint(1, number_of_bargaining_rounds)

    for player in players:
        player.participant.vars['final_payoff'] = player.participant.vars['payoff_round' + str(payment_round )] + subsession.session.config['participation_fee']

# PAGES

class Questions(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'reflection', 'comments']

class WaitForAll(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = compute_final_payoffs

class Completion(Page):
    pass



page_sequence = [Questions, WaitForAll, Completion]