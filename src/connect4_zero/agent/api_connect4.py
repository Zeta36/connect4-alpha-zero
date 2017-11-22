from connect4_zero.config import Config


class Connect4ModelAPI:
    def __init__(self, config: Config, agent_model):
        self.config = config
        self.agent_model = agent_model

    def predict(self, x):
        assert x.ndim in (3, 4)
        assert x.shape == (2, 6, 7) or x.shape[1:] == (2, 6, 7)
        orig_x = x
        if x.ndim == 3:
            x = x.reshape(1, 2, 6, 7)
        policy, value = self.agent_model.model.predict_on_batch(x)

        if orig_x.ndim == 3:
            return policy[0], value[0]
        else:
            return policy, value


