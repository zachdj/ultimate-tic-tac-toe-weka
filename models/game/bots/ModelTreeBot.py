from models.game.bots.MinimaxBot import MinimaxBot
from models.data.BoardDataModel import BoardDataModel
import weka.core.serialization as serialization
from weka.classifiers import Classifier


class ModelTreeBot(MinimaxBot):
    def __init__(self, number, name=None):
        """
        Minimax bot which uses a Model Tree to score board states

        :param number:  Board.X for player1 or Board.O for player2
        :param name: A descriptive name for the Bot
        """
        if name is None:
            name = "Model Tree Bot"
        MinimaxBot.__init__(self, number, name=name)
        self.player_type = 'modeltree minimax'

        objects = serialization.read_all("models/game/bots/weka_models/model-tree.model")
        self.classifier = Classifier(jobject=objects[0])

    def compute_score(self, board):
        data_model = BoardDataModel(board)
        weka_instance = data_model.get_weka_instance(categorical=False)
        score = self.classifier.classify_instance(weka_instance)

        # ensure score doesnt exceed legal range (1 and -1 are reserved for win/loss scores)
        score = min(score, 0.99)
        score = max(score, -0.99)

        return score
