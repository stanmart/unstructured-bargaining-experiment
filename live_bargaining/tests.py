from otree.api import Bot, Submission, expect
from otree.api import Currency as c

from . import Bargain, BargainingResults, Info


def create_offers(method, Y):
    # Offer 1

    method(
        1,
        {
            "type": "propose",
            "members": [True, True, True],
            "allocations": [90, 5, 5],
        },
    )

    # Offer 2
    method(
        3,
        {
            "type": "propose",
            "members": [True, True, True],
            "allocations": [50, 25, 25],
        },
    )

    # Offer 3
    method(
        1,
        {
            "type": "propose",
            "members": [True, True, False],
            "allocations": [
                Y // 2,
                Y // 2,
                0,
            ],
        },
    )


def test_invalid_input(method, Y, dummy_player, player_names):
    non_existing_offer = method(1, {"type": "accept", "offer_id": 1})
    expect(
        non_existing_offer,
        {
            1: {
                "type": "error",
                "content": "The offer you are trying to accept does not exist",
            }
        },
    )

    if not dummy_player:
        allocation_exceeds_total = method(
            2,
            {
                "type": "propose",
                "members": [True, True, False],
                "allocations": [
                    Y // 2 + 5,
                    Y // 2 + 5,
                    0,
                ],
            },
        )
    else:
        allocation_exceeds_total = method(
            2,
            {
                "type": "propose",
                "members": [True, True, True],
                "allocations": [50, 50, 10],
            },
        )
    expect(
        allocation_exceeds_total,
        {
            2: {
                "type": "error",
                "content": "Invalid allocation: allocations exceed value available to this group",
            }
        },
    )

    p1_not_included = method(
        3,
        {
            "type": "propose",
            "members": [False, True, True],
            "allocations": [0, 50, 50],
        },
    )
    if not dummy_player:
        expect(
            p1_not_included,
            {
                3: {
                    "type": "error",
                    "content": f"Invalid allocation: allocation has to be zero when Player {player_names['P1']} is not included",
                }
            },
        )
    else:
        expect(
            p1_not_included,
            {
                3: {
                    "type": "error",
                    "content": f"Invalid allocation: allocation has to be zero when Players {player_names['P1']} and {player_names['P2']} are not included",
                }
            },
        )

    invalid_allocaion_negative = method(
        1,
        {
            "type": "propose",
            "members": [True, True, True],
            "allocations": [50, 50, -20],
        },
    )
    expect(
        invalid_allocaion_negative,
        {1: {"type": "error", "content": "Invalid entry for allocation"}},
    )

    invalid_allocation_char = method(
        2,
        {
            "type": "propose",
            "members": [True, True, True],
            "allocations": [50, 50, "a"],
        },
    )
    expect(
        invalid_allocation_char,
        {2: {"type": "error", "content": "Invalid entry for allocation"}},
    )

    invalid_members = method(
        3,
        {"type": "propose", "members": [True, True, 5], "allocations": [50, 50, 0]},
    )
    expect(
        invalid_members,
        {3: {"type": "error", "content": "Invalid entry for members"}},
    )

    positive_to_nonmember = method(
        1,
        {
            "type": "propose",
            "members": [True, True, False],
            "allocations": [0, 5, 5],
        },
    )
    expect(
        positive_to_nonmember,
        {
            1: {
                "type": "error",
                "content": "Invalid allocation: only members in the group can receive positive amounts",
            }
        },
    )

    incomplete_data_members = method(
        2, {"type": "propose", "members": [True, True], "allocations": [5, 5, 0]}
    )
    expect(
        incomplete_data_members,
        {2: {"type": "error", "content": "Data is incomplete"}},
    )

    incomplete_data_allocations = method(
        3,
        {"type": "propose", "members": [True, True, False], "allocations": [5, 5]},
    )
    expect(
        incomplete_data_allocations,
        {3: {"type": "error", "content": "Data is incomplete"}},
    )

    member_receives_zero = method(
        1,
        {
            "type": "propose",
            "members": [True, True, True],
            "allocations": [100, 0, 0],
        },
    )
    expect(
        member_receives_zero,
        {
            1: {
                "type": "error",
                "content": "Invalid allocation: all members must receive a positive amount",
            }
        },
    )


def call_live_method(method, **kwargs):
    print(
        f"Session {kwargs['group'].session.config['name']}, round {kwargs['round_number']}: ",
        end="",
    )

    prod_fct = kwargs["group"].session.config["prod_fct"]
    player_names = kwargs["group"].session.config["player_names"]
    Y = list(prod_fct.values())[1]
    dummy_player = len(prod_fct) == 2

    if kwargs["round_number"] == 1:
        print("Testing invalid input")
        test_invalid_input(method, Y, dummy_player, player_names)

    if kwargs["round_number"] == 2:
        print("Testing grand coalition")
        create_offers(method, Y)
        method(3, {"type": "accept", "offer_id": 1})
        method(1, {"type": "accept", "offer_id": 2})
        method(2, {"type": "accept", "offer_id": 2})
        method(3, {"type": "accept", "offer_id": 2})

    if kwargs["round_number"] == 3:
        print("Testing no agreement")
        create_offers(method, Y)
        method(1, {"type": "accept", "offer_id": 2})
        method(2, {"type": "accept", "offer_id": 2})
        method(3, {"type": "accept", "offer_id": 1})

    if kwargs["round_number"] == 4:
        print("Testing smaller coalition")
        create_offers(method, Y)
        method(1, {"type": "accept", "offer_id": 3})
        method(2, {"type": "accept", "offer_id": 3})
        method(3, {"type": "accept", "offer_id": 1})

    if kwargs["round_number"] == 5:
        print("Testing revoking acceptance")
        create_offers(method, Y)
        method(1, {"type": "accept", "offer_id": 1})
        method(2, {"type": "accept", "offer_id": 1})
        method(3, {"type": "accept", "offer_id": 1})
        method(2, {"type": "accept", "offer_id": 0})

    if kwargs["round_number"] == 6:
        print("Testing revoking acceptance")
        create_offers(method, Y)
        method(1, {"type": "accept", "offer_id": 1})
        method(2, {"type": "accept", "offer_id": 1})
        method(3, {"type": "accept", "offer_id": 1})
        method(2, {"type": "accept", "offer_id": 0})


class PlayerBot(Bot):
    def play_round(self):
        yield Info  # just press proceed
        # call_live_method is automagically executed here
        yield Submission(
            Bargain, timeout_happened=True, check_html=False
        )  # act as if timer expired
        # payoffs are now realized, check them

        Y = list(self.session.config["prod_fct"].values())[1]

        num_real_rounds = 4
        expected_payoffs = {
            1: [0, 0, 0],
            2: [50, 25, 25],
            3: [0, 0, 0],
            4: [Y // 2, Y // 2, 0],
            5: [0, 0, 0],
        }

        expect(
            self.player.payoff,
            c(expected_payoffs[self.round_number][self.player.id_in_group - 1]),
        )

        yield BargainingResults  # just press proceed
