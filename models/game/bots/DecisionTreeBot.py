from models.game.bots.MinimaxBot import MinimaxBot
from models.data.BoardDataModel import BoardDataModel
import weka.core.serialization as serialization
from weka.classifiers import Classifier


class DecisionTreeBot(MinimaxBot):
    def __init__(self, number, name=None):
        """
        Minimax bot which uses a decision tree to score board states
        The decision tree outputs one of ten classes.  The higher the class number, the better the board state for X

        :param number:  Board.X for player1 or Board.O for player2
        :param name: A descriptive name for the Bot
        """
        if name is None:
            name = "DTree Bot"
        MinimaxBot.__init__(self, number, name=name)
        self.player_type = 'dtree minimax'

        objects = serialization.read_all("models/game/bots/weka_models/j48_default.model")
        self.classifier = Classifier(jobject=objects[0])

    def compute_score(self, board):
        data_model = BoardDataModel(board)
        weka_instance = data_model.get_weka_instance(categorical=True)
        # for some reason, the j48 model occasionally throws indexoutofbounds exceptions when classifying new instances
        # this try/except block is a hacky way of handling those, so we can at least get some results
        try:
            category = self.classifier.classify_instance(weka_instance)  # category will be one of the ten classes
        except Exception:
            print("Error in Decision-Tree Classifier!!")
            category = 5
        #  converts the class value into a numeric score between -1 and 1.   E.g. class 1 gets converted to -0.90, class 3 is converted to -0.50, class 10 is converted to 0.90, etc.
        score = ((category - 5.0) / 5.0) - 0.1

        return score
