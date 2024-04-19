from otree.api import Bot
from . import Questions


class PlayerBot(Bot):
    def play_round(self):
        answers = {
            "age": 14,  # not bad for a dogm might be a bit young for out subjects
            "gender": "Female",
            "degree": "PhD",
            "study_field": "Canine Behavior",
            "nationality": "Isle of Dogs",
            "reflection": "I barked a lot and they barked back",
            "pilot_difficulty": "Easy-peasy lemon squeezy",
            "pilot_explanation": "You did a great job!",
            "pilot_interface": "Bit hard to navigate with paws",
            "pilot_time": "35 dog minutes, more than enough",
            "comments": "Woof woof bark bark",
        }
        yield Questions, answers
