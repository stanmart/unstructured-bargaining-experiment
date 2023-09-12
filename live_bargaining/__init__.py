from otree.api import *

doc = """ 
"""
#todo: add doc
        
# todo: adapt role names to framing
class C(BaseConstants):
    NAME_IN_URL = 'live_bargaining'
    PLAYERS_PER_GROUP = 5 
    NUM_ROUNDS = 4

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
    members = []
    allocations = []

def check_validity(player: Player, members, allocations):
        if len(members) != len(allocations): 
            return {player.id_in_group: {"type": "error", "content" : "Data is incomplete"}}

        if any(allocations[i] > 0 and members[i] == 0 for i in range(len(members))): 
            return {player.id_in_group: {"type": "error", "content" : "Invalid allocation: only members in the coalition can receive positive payoffs"}}

        if not all(isinstance(val, int) and val >= 0 for val in allocations): 
            return {player.id_in_group: {"type": "error", "content" : "Invalid entry for allocation"}}
        
        if not all(isinstance(val, int) and (val == 0 or val == 1) for val in members): 
            return {player.id_in_group: {"type": "error", "content" : "Invalid entry for members"}}


        prod_fct = prod_fcts()[player.round_number]
        coalition_size = sum(members)
        big_player_included = any([player.group.get_player_by_id(i+1).role == 'Big Player' for i in range(len(self.members)) if self.members[i]==1]) #todo: check this works correctly

        if not big_player_included and sum(allocations) > 0: 
            return {player.id_in_group: {"type": "error", "content" : "Invalid allocation: allocation has to be zero when Big Player is not included"}}

        if big_player_included and sum(allocations) > prod_fct[coalition_size - 1]: 
            return {player.id_in_group: {"type": "error", "content" : "Invalid allocation: allocations exceed payoff available to this coalition"}}
        #todo: adapt error message to framing to players


class Bargain(Page):
#    timeout_seconds = 3

    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group)

    @staticmethod
    def live_method(player: Player, data):

        if 'propose' in data:
            error_messages = check_validity(player=player, members=data['members'], allocations=data['allocations'])
            if error_messages:
                return error_messages
            
            Proposal.create(player=player, members=data['members'], allocations=data['allocations'])
        return {0: {"type": "proposals_history", "proposals_history": Proposal.filter(group=group)}}

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            prod_fct = prod_fcts()[player.round_number]
            )

class Results(Page):
    pass

page_sequence = [Bargain, Results]
