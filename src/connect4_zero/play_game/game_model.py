from logging import getLogger

from connect4_zero.agent.player_connect4 import HistoryItem
from connect4_zero.agent.player_connect4 import Connect4Player, Player
from connect4_zero.config import Config
from connect4_zero.lib.model_helpler import load_best_model_weight

logger = getLogger(__name__)


class PlayWithHuman:
    def __init__(self, config: Config):
        self.config = config
        self.human_color = None
        self.observers = []
        self.model = self._load_model()
        self.ai = None  # type: Connect4Player
        self.last_evaluation = None
        self.last_history = None  # type: HistoryItem

    def start_game(self, human_is_black):
        self.human_color = Player.black if human_is_black else Player.white
        self.ai = Connect4Player(self.config, self.model)

    def _load_model(self):
        from connect4_zero.agent.model_connect4 import Connect4Model
        model = Connect4Model(self.config)
        if not load_best_model_weight(model):
            raise RuntimeError("best model not found!")
        return model

    def move_by_ai(self, env):
        action = self.ai.action(env.board)

        self.last_history = self.ai.ask_thought_about(env.observation)
        self.last_evaluation = self.last_history.values[self.last_history.action]
        logger.debug(f"evaluation by ai={self.last_evaluation}")

        return action

    def move_by_human(self, env):
        while True:
            try:
                movement = input('\nEnter your movement (1, 2, 3, 4, 5, 6, 7): ')
                movement = int(movement) - 1
                legal_moves = env.legal_moves()
                if legal_moves[int(movement)] == 1:
                    return int(movement)
                else:
                    print("That is NOT a valid movement :(.")
            except:
                print("That is NOT a valid movement :(.")