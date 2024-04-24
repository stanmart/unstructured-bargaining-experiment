from otree.api import Bot
from . import Questions


class PlayerBot(Bot):
    def play_round(self):
        answers = {
            "age": 14,  # not bad for a dog, might be a bit young for our subjects
            "gender": "Female",
            "degree": "PhD",
            "study_field": "Canine Behavior",
            "nationality": "CH",
            "own_strategy": "I barked a lot and they barked back",
            "other_players_strategy": "They didn't give me ear scratches :(",
            "pilot_difficulty": "Very easy",
            "pilot_explanation": "Very well",
            "pilot_interface": "Very well",
            "pilot_time": "Just right",
            # "comments": "Woof woof bark bark",
            "dummy_player_axiom": "Strongly Disagree",
            "symmetry_axiom": "Strongly Agree",
            "efficiency_axiom": "Agree",
            "linearity_axiom": "Neutral",
            "stability_axiom": "Disagree",
        }
        yield Questions, answers
