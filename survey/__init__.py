from otree.api import *
from random import randint

class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    payment_round = models.IntegerField()


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(label='What is your age?', min=13, max=125)
    gender = models.StringField(
        choices=[['Male', 'Male'], ['Female', 'Female'], ['Other', 'Other']],
        label='What is your gender?',
        widget=widgets.RadioSelect,
    )
    degree = models.StringField(
        choices=[['Bachelor', 'Bachelor'], ['Master', 'Master'], ['PhD', 'PhD'],['Other', 'Other']],
        label='What is your current degree?',
        widget=widgets.RadioSelect,
    )
    study_field = models.StringField(
        label = '''
        What is your field of study?'''
    )
    nationality= models.StringField(
        label = '''
        What is your nationality?'''
    )
    reflection = models.LongStringField(
        label='''
        What was your bargaining strategy and why? What did you think about the behavior of the other players?'''
    )

    #TODO: delete for the main experiment
    pilot_difficulty = models.StringField(
        label = '''
        How would you rate the difficulty level of the game?'''
    )
    pilot_explanation = models.StringField(
        label = '''
        How well was the game explained? What parts were unclear to you? What would you change in the explanation?'''
    )
    pilot_interface = models.StringField(
        label = '''
        How well could you work with the bargaining interface? What parts would you change?'''
    )
    pilot_time = models.StringField(
        label = '''
        Did you feel there was enough time for the bargaining? How much would you have preferred?'''
    )

    comments = models.LongStringField(
        label='''
        Any additional comments you want to share with us?'''
    )
  

# FUNCTIONS
def compute_final_payoffs(subsession: Subsession):
    
    players = subsession.get_players()
    # get number of (non-trial) bargaining rounds
    player0_payoffs = [players[0].participant.vars['payoff_round' + str(i)] for i in range(2,7)] 
    number_of_bargaining_rounds = sum(elem >= 0 for elem in player0_payoffs)
    subsession.payment_round = randint(2, number_of_bargaining_rounds)

    for player in players:
        player.payoff = getattr(player.participant, 'payoff_round' + str(subsession.payment_round))
        player.participant.final_payoff = player.participant.payoff_plus_participation_fee()


# PAGES

class Questions(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'degree', 'study_field', 'nationality', 'reflection', 'pilot_difficulty', 'pilot_explanation', 'pilot_interface', 'pilot_time', 'comments']

class WaitForAll(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = compute_final_payoffs

class Completion(Page):
    pass


page_sequence = [Questions, WaitForAll, Completion]
