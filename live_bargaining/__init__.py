import pickle
import time
from datetime import datetime

from otree.api import (
    BaseConstants,
    BaseGroup,
    BasePlayer,
    BaseSubsession,
    ExtraModel,
    Page,
    WaitPage,
    models,
)

doc = """
The actual bargaining game.
Players can propose, discuss and accept offers in real time.
Proposals must conform to the group budgets (characteristic function of the game).
No action is binding during the bargaining phase, but current choices ara auto-accepted and binding at the end of the round.
"""
# todo: add doc


def creating_session(subsession):
    num_active_groups = len(subsession.get_groups())
    if num_active_groups in [6, 7]:
        subsession_index = subsession.round_number - 1
        with open(
            "preparation/group_matrices/group_matrices_"
            + str(num_active_groups)
            + "_groups.pkl",
            "rb",
        ) as file:
            group_matrices = pickle.load(file)
        if subsession_index < len(group_matrices):
            subsession.set_group_matrix(group_matrices[subsession_index])
        else:
            subsession.group_randomly()
    else:
        subsession.group_randomly()

    for player in subsession.get_players():
        player.participant.vars["payoff_list"] = []


class C(BaseConstants):
    NAME_IN_URL = "live_bargaining"
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 5  # todo: adjust for main experiment


class Subsession(BaseSubsession):
    start_time = models.FloatField(initial=float("inf"))  # type: ignore
    expiry = models.FloatField(initial=float("inf"))  # type: ignore


class Group(BaseGroup):
    last_offer_id = models.IntegerField(initial=0)  # type: ignore


class Player(BasePlayer):
    accepted_offer = models.IntegerField(
        initial=0  # type: ignore
    )  # 0 means no offer accepted
    payoff_this_round = models.IntegerField(initial=0)  # type: ignore
    end_time = models.FloatField(initial=float("inf"))  # type: ignore


class Proposal(ExtraModel):
    timestamp_iso = models.StringField()
    timestamp = models.FloatField()
    player = models.Link(Player)
    group = models.Link(Group)
    offer_id = models.IntegerField()
    member_1 = models.BooleanField()
    member_2 = models.BooleanField()
    member_3 = models.BooleanField()
    allocation_1 = models.IntegerField()
    allocation_2 = models.IntegerField()
    allocation_3 = models.IntegerField()

    @classmethod
    def create_fromlist(cls, player, members, allocations):
        player.group.last_offer_id += 1
        return cls.create(
            timestamp_iso=datetime.now().isoformat(),
            timestamp=time.time(),
            player=player,
            group=player.group,
            offer_id=player.group.last_offer_id,
            member_1=members[0],
            member_2=members[1],
            member_3=members[2],
            allocation_1=allocations[0],
            allocation_2=allocations[1],
            allocation_3=allocations[2],
        )

    @classmethod
    def filter_tolist(cls, *args, **kwargs):
        filtered = cls.filter(*args, **kwargs)
        return [
            {
                "offer_id": proposal.offer_id,
                "player": proposal.player.id_in_group,
                "members": [
                    proposal.member_1,
                    proposal.member_2,
                    proposal.member_3,
                ],
                "allocations": [
                    proposal.allocation_1,
                    proposal.allocation_2,
                    proposal.allocation_3,
                ],
            }
            for proposal in filtered
        ]


class Acceptance(ExtraModel):
    timestamp_iso = models.StringField()
    timestamp = models.FloatField()
    player = models.Link(Player)
    group = models.Link(Group)
    offer_id = models.IntegerField()


class PageLoad(ExtraModel):
    timestamp_iso = models.StringField()
    timestamp = models.FloatField()
    player = models.Link(Player)
    group = models.Link(Group)


def check_proposal_validity(player: Player, members, allocations):
    if len(members) != C.PLAYERS_PER_GROUP or len(allocations) != C.PLAYERS_PER_GROUP:
        return {player.id_in_group: {"type": "error", "content": "Data is incomplete"}}

    try:
        allocations = [int(val) for val in allocations]
    except (ValueError, TypeError):
        return {
            player.id_in_group: {
                "type": "error",
                "content": "Invalid entry for allocation",
            }
        }

    if any(
        allocation > 0 and member == 0
        for allocation, member in zip(allocations, members)
    ):
        return {
            player.id_in_group: {
                "type": "error",
                "content": "Invalid allocation: only members in the group can receive positive amounts",  # noqa: E501
            }
        }

    if not all(isinstance(val, bool) for val in members):
        return {
            player.id_in_group: {
                "type": "error",
                "content": "Invalid entry for members",
            }
        }

    prod_fct = list(player.session.config["prod_fct"].values())
    coalition_size = sum(members)
    big_player_included = members[0]  # the big player is always first

    if not all(val >= 0 for val in allocations):
        return {
            player.id_in_group: {
                "type": "error",
                "content": "Invalid entry for allocation",
            }
        }

    last_player_is_dummy = len(prod_fct) == C.PLAYERS_PER_GROUP - 1

    if not last_player_is_dummy and not big_player_included and sum(allocations) > 0:
        return {
            player.id_in_group: {
                "type": "error",
                "content": (
                    "Invalid allocation: allocation has to be zero when "
                    f"Player {player.session.config['player_names']['P1']} is not included"
                ),
            }
        }

    if (
        last_player_is_dummy
        and not (members[0] and members[1])
        and sum(allocations) > 0
    ):
        return {
            player.id_in_group: {
                "type": "error",
                "content": (
                    "Invalid allocation: allocation has to be zero when Players "
                    f"{player.session.config['player_names']['P1']} and "
                    f"{player.session.config['player_names']['P2']} are not included"
                ),
            }
        }

    num_small_players = coalition_size - big_player_included
    if last_player_is_dummy:  # last player is a dummy player
        num_small_players -= members[-1]  # the dummy player is always last

    if sum(allocations) > prod_fct[num_small_players]:
        return {
            player.id_in_group: {
                "type": "error",
                "content": "Invalid allocation: allocations exceed value available to this group",  # noqa: E501
            }
        }

    if any(
        member and allocation == 0 for member, allocation in zip(members, allocations)
    ):
        return {
            player.id_in_group: {
                "type": "error",
                "content": "Invalid allocation: all members must receive a positive amount",  # noqa: E501
            }
        }


def check_acceptance_validity(player: Player, offer_id):
    if not isinstance(offer_id, int):
        return {player.id_in_group: {"type": "error", "content": "Invalid offer id"}}
    if offer_id != 0 and offer_id not in (
        proposal["offer_id"] for proposal in Proposal.filter_tolist(group=player.group)
    ):
        return {
            player.id_in_group: {
                "type": "error",
                "content": "The offer you are trying to accept does not exist",
            }
        }


def create_acceptance_data(group: Group):
    players: list[Player] = sorted(group.get_players(), key=lambda p: p.id_in_group)
    p1_offer = players[0].accepted_offer
    if players[0].accepted_offer == 0:  # P1 not in any coalition
        return {
            "acceptances": [player.accepted_offer for player in players],
            "coalition_members": [False] * C.PLAYERS_PER_GROUP,
            "payoffs": [0] * C.PLAYERS_PER_GROUP,
        }
    else:
        offer = Proposal.filter_tolist(group=group, offer_id=p1_offer)[0]
        if all(
            player.accepted_offer == p1_offer
            for member, player in zip(offer["members"], players)
            if member
        ):
            return {
                "acceptances": [player.accepted_offer for player in players],
                "coalition_members": offer["members"],
                "payoffs": offer["allocations"],
            }
        else:  # Not everyone accepted the offer
            return {
                "acceptances": [player.accepted_offer for player in players],
                "coalition_members": [False] * C.PLAYERS_PER_GROUP,
                "payoffs": [0] * C.PLAYERS_PER_GROUP,
            }


class Info(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            last_player_is_dummy=len(player.session.config["prod_fct"])
            == C.PLAYERS_PER_GROUP - 1,
            actual_round_number=player.subsession.round_number - 1,
            player_name=player.session.config["player_names"][f"P{player.id_in_group}"],
        )

    @staticmethod
    def js_vars(player: Player):
        return dict(
            my_id=player.id_in_group,
            prod_fct=list(player.session.config["prod_fct"].values()),
            prod_fct_labels=list(player.session.config["prod_fct"].keys()),
        )


class WaitForBargaining(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession: BaseSubsession):  # type: ignore
        subsession.start_time = time.time()  # type: ignore
        subsession.expiry = time.time() + subsession.session.config["seconds_per_round"]  # type: ignore


class Bargain(Page):
    timer_text = "Time left for bargaining:"

    @staticmethod
    def get_timeout_seconds(player: Player):
        return player.subsession.expiry - time.time()  # type: ignore

    @staticmethod
    def js_vars(player: Player):
        return dict(
            my_id=player.id_in_group,
            prod_fct=list(player.session.config["prod_fct"].values()),
            prod_fct_labels=list(player.session.config["prod_fct"].keys()),
            player_names=player.session.config["player_names"],
        )

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            last_player_is_dummy=len(player.session.config["prod_fct"])
            == C.PLAYERS_PER_GROUP - 1,
            player_name=player.session.config["player_names"][f"P{player.id_in_group}"],
            actual_round_number=player.subsession.round_number - 1,
            **player.session.config["player_names"],
        )

    @staticmethod
    def live_method(player: Player, data):
        if "type" in data and data["type"] == "propose":
            error_messages = check_proposal_validity(
                player=player, members=data["members"], allocations=data["allocations"]
            )
            if error_messages:
                return error_messages

            Proposal.create_fromlist(
                player=player, members=data["members"], allocations=data["allocations"]
            )
            return {
                0: {
                    "type": "proposals_history",
                    "proposals_history": Proposal.filter_tolist(group=player.group),
                }
            }

        elif "type" in data and data["type"] == "accept":
            error_messages = check_acceptance_validity(
                player=player, offer_id=data["offer_id"]
            )
            if error_messages:
                return error_messages

            offer_id = data["offer_id"]
            Acceptance.create(
                timestamp_iso=datetime.now().isoformat(),
                timestamp=time.time(),
                player=player,
                group=player.group,
                offer_id=offer_id,
            )
            player.accepted_offer = offer_id
            return_data = create_acceptance_data(group=player.group)  # type: ignore
            return_data["type"] = "acceptances"
            return {0: return_data}

        else:
            # (re)load page case:
            PageLoad.create(
                timestamp_iso=datetime.now().isoformat(),
                timestamp=time.time(),
                player=player,
                group=player.group,
            )
            return {
                player.id_in_group: {
                    "type": "reload",
                    "proposals_history": Proposal.filter_tolist(group=player.group),
                    **create_acceptance_data(group=player.group),  # type: ignore
                }
            }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.end_time = time.time()  # type: ignore


def compute_payoffs(group: Group):
    players = sorted(group.get_players(), key=lambda p: p.id_in_group)
    final_payoffs = create_acceptance_data(group)["payoffs"]

    for player, final_payoff in zip(players, final_payoffs):
        player.payoff_this_round = final_payoff
        player.participant.vars["payoff_list"].append(player.payoff_this_round)

        if group.round_number == 1:
            player.payoff = 0
        else:
            player.payoff = player.payoff_this_round / (C.NUM_ROUNDS - 1)


class WaitForAnswers(WaitPage):
    after_all_players_arrive = compute_payoffs


class BargainingResults(Page):
    @staticmethod
    def js_vars(player: Player):
        acceptance_data = create_acceptance_data(player.group)  # type: ignore
        return dict(
            my_id=player.id_in_group,
            past_offers=Proposal.filter_tolist(group=player.group),
            acceptances=acceptance_data["acceptances"],
            coalition_members=acceptance_data["coalition_members"],
            payoffs=acceptance_data["payoffs"],
            player_names=player.session.config["player_names"],
        )

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            payoff_to_display=f"CHF {player.payoff_this_round:.2f}",
            **player.session.config["player_names"],
        )


def custom_export(players):
    yield [
        "timestamp_iso",
        "timestamp",
        "event_type",
        "session_code",
        "participant_code",
        "round_number",
        "player_id",
        "id_in_group",
        "group_id",
        "offer_id",
        "member_1",
        "member_2",
        "member_3",
        "allocation_1",
        "allocation_2",
        "allocation_3",
        "accepted_offer",
    ]

    # 'filter' without any args returns everything
    proposals = Proposal.filter()
    for proposal in proposals:
        player = proposal.player
        participant = player.participant
        session = player.session
        yield [
            proposal.timestamp_iso,
            proposal.timestamp,
            "proposal",
            session.code,
            participant.code,
            player.round_number,
            player.id,
            player.id_in_group,
            player.group.id,
            proposal.offer_id,
            proposal.member_1,
            proposal.member_2,
            proposal.member_3,
            proposal.allocation_1,
            proposal.allocation_2,
            proposal.allocation_3,
            "",
        ]

    acceptances = Acceptance.filter()
    for acceptance in acceptances:
        player = acceptance.player
        participant = player.participant
        session = player.session
        yield [
            acceptance.timestamp_iso,
            acceptance.timestamp,
            "acceptance",
            session.code,
            participant.code,
            player.round_number,
            player.id,
            player.id_in_group,
            player.group.id,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            acceptance.offer_id,
        ]

    page_loads = PageLoad.filter()
    for page_load in page_loads:
        player = page_load.player
        participant = player.participant
        session = player.session
        yield [
            page_load.timestamp_iso,
            page_load.timestamp,
            "page_load",
            session.code,
            participant.code,
            player.round_number,
            player.id,
            player.id_in_group,
            player.group.id,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]


page_sequence = [
    Info,
    WaitForBargaining,
    Bargain,
    WaitForAnswers,
    BargainingResults,
]
