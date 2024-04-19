from otree.api import Bot, Submission
from . import Coalitions, Instructions, Payment, Proposal, Welcome


class PlayerBot(Bot):
    def play_round(self):
        yield Welcome
        yield Instructions
        yield Submission(
            Proposal, timeout_happened=True, check_html=False
        )  # do not test tasks
        yield Submission(
            Coalitions, timeout_happened=True, check_html=False
        )  # do not test tasks
        yield Payment
