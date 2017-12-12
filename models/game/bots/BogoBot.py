import random
from .Bot import Bot


class BogoBot(Bot):
    title = "Random Bot"
    """
    This bot moves at random
    """
    def __init__(self, player):
        Bot.__init__(self, player, "BogoBot")
        self.player_type = 'rng bot'
        random.seed()

    def compute_next_move(self, board, valid_moves):
        return random.choice(valid_moves)

    def setup_bot(self, game):
        pass
