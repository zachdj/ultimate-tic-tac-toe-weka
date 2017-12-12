from .BogoBot import BogoBot
from .RandoMaxBot import RandoMaxBot
from .MonteCarloBot import MonteCarloBot
from .ContinuousNeuralNetBot import ContinuousNeuralNetBot
from .ModelTreeBot import ModelTreeBot
from .NominalNeuralNetBot import NominalNeuralNetBot
from .CostSensitiveNeuralNetBot import CostSensitiveNeuralNetBot
from .DecisionTreeBot import DecisionTreeBot

"""
The BotLoader module loads a list of all bots with a human-readable name, description, and difficulty (0-10)

This module is used in the SetupGame and SetupExperiment scenes to provide the user with a selectable list of Bot types
Right now, the "difficulty" and "description" values are not used for anything.  In the future, they may be used in the 
menu where bots are selected
"""

bots = [
    {
        "title" : "Random Bot",
        "description": "Chooses moves at random.",
        "difficulty": 0,
        "data": BogoBot
     },
    {
        "title": "RandoMax Bot",
        "description": "Bot that moves randomly unless a winning move is available",
        "difficulty": 1,
        "data": RandoMaxBot
    },
    {
        "title": "Monte Carlo Search Tree",
        "description": "Uses the Monte Carlo Search Tree algorithm to play..",
        "difficulty": 3,
        "data": MonteCarloBot
     },
    {
        "title": "Nominal MLP Bot",
        "description": "Minimax bot that uses a nominal neural net to score boards",
        "difficulty": 5,
        "data": NominalNeuralNetBot
    },
    {
        "title": "DTree Bot",
        "description": "Minimax bot that uses a boosted decision tree model to score boards",
        "difficulty": 5,
        "data": DecisionTreeBot
    },
    {
        "title": "Continuous MLP Bot",
        "description": "Minimax bot that uses a neural net to score boards",
        "difficulty": 5,
        "data": ContinuousNeuralNetBot
    },
    {
        "title": "Model Tree Bot",
        "description": "Minimax bot that uses a Model Tree to score boards",
        "difficulty": 5,
        "data": ModelTreeBot
    },
    {
        "title": "Cost Sensitive MLP Bot",
        "description": "Minimax bot that uses a cost-sensitive neural net to score boards",
        "difficulty": 5,
        "data": CostSensitiveNeuralNetBot
    },
]


def get_bots():
    return bots

