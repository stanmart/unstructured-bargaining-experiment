import pickle
from otree.api import *

doc = """ 
"""
#todo: add doc


def creating_session(subsession):
    num_active_groups = len(subsession.get_groups())
    if num_active_groups in [6,7]:
        subsession_index = subsession.round_number - 1
        with open('preparation/group_matrices/group_matrices_' + str(num_active_groups) + '_groups.pkl', 'rb') as file:
            group_matrices = pickle.load(file)
        if subsession_index < len(group_matrices):
            subsession.set_group_matrix(group_matrices[subsession_index])
        else:
            subsession.group_randomly()
    else:
        subsession.group_randomly()


       
# todo: adapt role names to framing
class C(BaseConstants):
    NAME_IN_URL = 'live_bargaining'
    PLAYERS_PER_GROUP = 5 
    NUM_ROUNDS = 5

    BIG_ROLE = 'Big Player'
    SMALL1_ROLE = 'Small Player'
    SMALL2_ROLE = 'Small Player'
    SMALL3_ROLE = 'Small Player'
    SMALL4_ROLE = 'Small Player'

    
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    deal_price = models.CurrencyField(initial = 0) 
class Player(BasePlayer):
    pass

#todo: set values for dummy treatment, possibly adjust values
def prod_fcts():
    return {
                1: [0, 25, 50, 75, 100], #linear
                2: [0, 5, 20, 60, 100], #convex
                3: [0,  45,  80,  90, 100], #concave
                4: [0, 0, 0, 0, 0] #dummy
            } 
#todo: move to constants?

class Proposal(ExtraModel):
    player = models.Link(Player)
    group = models.Link(Group)
    member_1 = models.BooleanField()
    member_2 = models.BooleanField()
    member_3 = models.BooleanField()
    member_4 = models.BooleanField()
    member_5 = models.BooleanField()
    allocation_1 = models.IntegerField()
    allocation_2 = models.IntegerField()
    allocation_3 = models.IntegerField()
    allocation_4 = models.IntegerField()
    allocation_5 = models.IntegerField()

    @classmethod
    def create_fromlist(cls, player, members, allocations):
        return cls.create(
            player=player,
            group=player.group,
            member_1=members[0],
            member_2=members[1],
            member_3=members[2],
            member_4=members[3],
            member_5=members[4],
            allocation_1=allocations[0],
            allocation_2=allocations[1],
            allocation_3=allocations[2],
            allocation_4=allocations[3],
            allocation_5=allocations[4],
        )

    @classmethod
    def filter_tolist(cls, *args, **kwargs):
        filtered = cls.filter(*args, **kwargs)
        return [
            {
                "offer_id": id,
                "player": proposal.player.id_in_group,
                "members": [proposal.member_1, proposal.member_2, proposal.member_3, proposal.member_4, proposal.member_5],
                "allocations": [proposal.allocation_1, proposal.allocation_2, proposal.allocation_3, proposal.allocation_4, proposal.allocation_5],
            }
            for id, proposal in enumerate(filtered)
        ]


def check_validity(player: Player, members, allocations):
    if len(members) != len(allocations): 
        return {player.id_in_group: {"type": "error", "content" : "Data is incomplete"}}
    
    try:
        allocations = [int(val) for val in allocations]
    except ValueError:
        return {player.id_in_group: {"type": "error", "content" : "Invalid entry for allocation"}}

    if any(allocations[i] > 0 and members[i] == 0 for i in range(len(members))): 
        return {player.id_in_group: {"type": "error", "content" : "Invalid allocation: only members in the coalition can receive positive payoffs"}}

    if not all(isinstance(val, int) and val >= 0 for val in allocations): 
        return {player.id_in_group: {"type": "error", "content" : "Invalid entry for allocation"}}
    
    if not all(isinstance(val, int) and (val == 0 or val == 1) for val in members): 
        return {player.id_in_group: {"type": "error", "content" : "Invalid entry for members"}}


    prod_fct = prod_fcts()[player.round_number]
    coalition_size = sum(members)
    big_player_included = any([player.group.get_player_by_id(i+1).role == 'Big Player' for i in range(len(members)) if members[i]]) #todo: check this works correctly

    if not big_player_included and sum(allocations) > 0: 
        return {player.id_in_group: {"type": "error", "content" : "Invalid allocation: allocation has to be zero when Big Player is not included"}}

    if big_player_included and sum(allocations) > prod_fct[coalition_size - 1]: 
        return {player.id_in_group: {"type": "error", "content" : "Invalid allocation: allocations exceed payoff available to this coalition"}}
    #todo: adapt error message to framing to players


class Bargain(Page):
#    timeout_seconds = 3

    @staticmethod
    def js_vars(player: Player):
        return dict(
            my_id=player.id_in_group,
            prod_fct = prod_fcts()[player.round_number],
        )

    @staticmethod
    def live_method(player: Player, data):

        if 'type' in data and data['type'] == 'propose':
            error_messages = check_validity(player=player, members=data['members'], allocations=data['allocations'])
            if error_messages:
                return error_messages
            
            Proposal.create_fromlist(player=player, members=data['members'], allocations=data['allocations'])
            return {0: {"type": "proposals_history", "proposals_history": Proposal.filter_tolist(group=player.group)}}

class Results(Page):
    pass

page_sequence = [Bargain, Results]
