from scenes.MainMenu import MainMenu
from scenes.SetupGame import SetupGame
from scenes.PlayGame import PlayGame
from scenes.GameCompleted import GameCompleted
from scenes.SetupExperiment import SetupExperiment
from scenes.RunExperiment import RunExperiment

"""
This module provides convenience functions for switching to scenes.  This solves problems with scene circular dependence
For example, MainMenu requires SetupGame requires PlayGame requires GameCompleted requires MainMenu
"""


def go_to_main_menu(current_scene):
    current_scene.switch_to_scene(MainMenu())


def go_to_setup_game(current_scene):
    current_scene.switch_to_scene(SetupGame())


def go_to_play_game(current_scene, p1, p2):
    current_scene.switch_to_scene(PlayGame(p1, p2))


def go_to_game_completed(current_scene, game):
    current_scene.switch_to_scene(GameCompleted(game))


def go_to_setup_experiment(current_scene):
    current_scene.switch_to_scene(SetupExperiment())


def go_to_experiment(current_scene, experiment):
    current_scene.switch_to_scene(RunExperiment(experiment))


# dirty hack that I'm very ashamed of to make menu scene work from initial bootstrap in main.py
def get_main_menu_instance():
    return MainMenu()


