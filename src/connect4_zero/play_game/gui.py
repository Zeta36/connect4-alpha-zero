from logging import getLogger


from connect4_zero.config import Config, PlayWithHumanConfig
from connect4_zero.play_game.game_model import PlayWithHuman
from connect4_zero.env.connect4_env import Connect4Env, Player, Winner
from random import random

logger = getLogger(__name__)


def start(config: Config):
    PlayWithHumanConfig().update_play_config(config.play)
    connect4_model = PlayWithHuman(config)

    while True:
        env = Connect4Env().reset()
        human_is_black = random() < 0.5
        connect4_model.start_game(human_is_black)

        while not env.done:
            if env.player_turn() == Player.black:
                if not human_is_black:
                    action = connect4_model.move_by_ai(env)
                    print("IA moves to: " + str(action))
                else:
                    action = connect4_model.move_by_human(env)
                    print("You move to: " + str(action))
            else:
                if human_is_black:
                    action = connect4_model.move_by_ai(env)
                    print("IA moves to: " + str(action))
                else:
                    action = connect4_model.move_by_human(env)
                    print("You move to: " + str(action))
            env.step(action)
            env.render()

        print("\nEnd of the game.")
        print("Game result:")
        if env.winner == Winner.white:
            print("X wins")
        elif env.winner == Winner.black:
            print("O wins")
        else:
            print("Game was a draw")
