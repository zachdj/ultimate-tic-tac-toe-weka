from models.game.bots.Bot import Bot
from models.game.Game import Game
from models.data.GameDataModel import GameDataModel
from models.data import DatabaseConnection as DB


class Experiment(object):
    def __init__(self, player1, player2, iterations, record=True):
        """ An Experiment is a sequence of several games between two bots.  Results can be saved or discarded

        :param player1: the Bot playing as 'X'
        :param player2: the Bot playing as 'O'
        :param iterations: the number of games to play for this experiment
        :param record: boolean indicator - should the result of games be recorded or not?
        """
        if not isinstance(player1, Bot) or not isinstance(player2, Bot):
            raise Exception("Invalid Experiment: both players must be bots")

        self.p1 = player1
        self.p2 = player2
        self.iterations = iterations
        self.completed_iterations = 0
        self.p1_wins = 0
        self.p2_wins = 0
        self.ties = 0
        self.record_result = record
        self.finished = False

    def run(self, callback=None):
        """ Runs the current experiment.  The callback function will be called after each game is finished.

        :param callback: a function to call at the termination of each game.  The iteration number and winner will be passed as arguments
        :return: None
        """
        db_insertion_scripts = []
        for i in list(range(0, self.iterations)):
            game = Game(self.p1, self.p2)
            game.finish_game()
            self.completed_iterations += 1
            winner = game.get_winner()
            if winner == self.p1.number:
                self.p1_wins += 1
            elif winner == self.p2.number:
                self.p2_wins += 1
            else:
                self.ties += 1

            if self.record_result:
                game_dm = GameDataModel(game)
                db_insertion_scripts.append(game_dm.get_save_script())

            if callback is not None:
                callback(i+1, game.get_winner())

        if self.record_result:
            insertion_script = "\n".join(db_insertion_scripts)
            DB.execute(insertion_script)

        self.finished = True

    def get_p1_win_rate(self):
        if self.completed_iterations == 0:
            return 0

        return self.p1_wins / self.completed_iterations

    def get_p2_win_rate(self):
        if self.completed_iterations == 0:
            return 0

        return self.p2_wins / self.completed_iterations

    def get_tie_rate(self):
        if self.completed_iterations == 0:
            return 0

        return self.ties / self.completed_iterations
