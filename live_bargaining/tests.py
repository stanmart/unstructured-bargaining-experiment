from otree.api import Currency as c, expect, Bot, Submission
from . import Info, Bargain, BargainingResults


def create_offers(method):
    method(
        1,
        {
            "type": "propose",
            "members": [True, True, True],
            "allocations": [100, 0, 0],
        },
    )
    method(
        3,
        {
            "type": "propose",
            "members": [True, True, True],
            "allocations": [50, 25, 25],
        },
    )
    method(
        1,
        {
            "type": "propose",
            "members": [True, True, False],
            "allocations": [5, 5, 0],
        },
    )


def test_invalid_input(method):
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

    allocation_exceeds_total = method(
        2,
        {
            "type": "propose",
            "members": [True, True, False],
            "allocations": [50, 50, 0],
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
    expect(
        p1_not_included,
        {
            3: {
                "type": "error",
                "content": "Invalid allocation: allocation has to be zero when Player 1 is not included",
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


def call_live_method(method, **kwargs):
    # Grand coalition
    if kwargs["round_number"] == 2:
        create_offers(method)
        method(3, {"type": "accept", "offer_id": 1})
        method(1, {"type": "accept", "offer_id": 2})
        method(2, {"type": "accept", "offer_id": 2})
        method(3, {"type": "accept", "offer_id": 2})

    # No agreement
    if kwargs["round_number"] == 3:
        create_offers(method)
        method(1, {"type": "accept", "offer_id": 2})
        method(2, {"type": "accept", "offer_id": 2})
        method(3, {"type": "accept", "offer_id": 2})
        method(3, {"type": "accept", "offer_id": 0})

    # Smaller coalition
    if kwargs["round_number"] == 4:
        create_offers(method)
        method(1, {"type": "accept", "offer_id": 3})
        method(2, {"type": "accept", "offer_id": 3})
        method(3, {"type": "accept", "offer_id": 1})

    # Invalid input
    if kwargs["round_number"] == 5:
        test_invalid_input(method)


class PlayerBot(Bot):
    def play_round(self):
        yield Info
        yield Submission(Bargain, timeout_happened=True, check_html=False)

        num_real_rounds = 4

        if self.round_number == 2:
            if self.player.id_in_group == 1:
                expect(self.player.payoff, c(50 / num_real_rounds))
            else:
                expect(self.player.payoff, c(25 / num_real_rounds))

        if self.round_number == 3:
            expect(self.player.payoff, c(0))

        if self.round_number == 4:
            if self.player.id_in_group in [1, 2]:
                expect(self.player.payoff, c(5 / num_real_rounds))
            else:
                expect(self.player.payoff, c(0))

        yield BargainingResults
