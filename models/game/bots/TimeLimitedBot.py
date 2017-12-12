from .Bot import Bot


class TimeLimitedBot(Bot):
    def __init__(self, player, time_limit=10, name=None):
        """
        Abstract superclass for bots which are constrained by a time limit
        :param player: Board.X or Board.O
        :param time_limit: the maximum time that this bot can take to decide a move, in seconds
        :param name: a human-readable name for the bot
        """
        if name is None:
            name = "Time-Limited Bot"
        Bot.__init__(self, player, name)
        self.time_limit = time_limit
        self.player_type = 'timed bot'
