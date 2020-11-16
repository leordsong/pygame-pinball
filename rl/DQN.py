from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
import random
import numpy as np
from operator import add
import collections


class DQNAgent(object):
    def __init__(self):
        self.reward = 0
        self.gamma = 0.9
        self.short_memory = np.array([])
        self.agent_target = 1
        self.agent_predict = 0
        self.learning_rate = 0.0005
        self.epsilon = 1
        self.actual = []
        self.first_layer = 50
        self.second_layer = 300
        self.third_layer = 50
        self.memory = collections.deque(maxlen=2500)
        self.model = self.network()

    def network(self):
        model = Sequential()
        model.add(Dense(self.first_layer, activation='relu', input_dim=11))
        model.add(Dense(self.second_layer, activation='relu'))
        model.add(Dense(self.third_layer, activation='relu'))
        model.add(Dense(100, output_dim=3, activation='softmax'))
        opt = Adam(self.learning_rate)
        model.compile(loss='mse', optimizer=opt)
        return model

    def get_state(self, game, player, food):
        state = [
            (player.x_change == 20 and player.y_change == 0 and (
                        (list(map(add, player.position[-1], [20, 0])) in player.position) or
                        player.position[-1][0] + 20 >= (game.game_width - 20))) or (
                        player.x_change == -20 and player.y_change == 0 and (
                            (list(map(add, player.position[-1], [-20, 0])) in player.position) or
                            player.position[-1][0] - 20 < 20)) or (player.x_change == 0 and player.y_change == -20 and (
                        (list(map(add, player.position[-1], [0, -20])) in player.position) or
                        player.position[-1][-1] - 20 < 20)) or (player.x_change == 0 and player.y_change == 20 and (
                        (list(map(add, player.position[-1], [0, 20])) in player.position) or
                        player.position[-1][-1] + 20 >= (game.game_height - 20))),  # danger straight

            (player.x_change == 0 and player.y_change == -20 and (
                        (list(map(add, player.position[-1], [20, 0])) in player.position) or
                        player.position[-1][0] + 20 > (game.game_width - 20))) or (
                        player.x_change == 0 and player.y_change == 20 and ((list(map(add, player.position[-1],
                                                                                      [-20, 0])) in player.position) or
                                                                            player.position[-1][0] - 20 < 20)) or (
                        player.x_change == -20 and player.y_change == 0 and ((list(map(
                    add, player.position[-1], [0, -20])) in player.position) or player.position[-1][-1] - 20 < 20)) or (
                        player.x_change == 20 and player.y_change == 0 and (
                        (list(map(add, player.position[-1], [0, 20])) in player.position) or player.position[-1][
                    -1] + 20 >= (game.game_height - 20))),  # danger right

            (player.x_change == 0 and player.y_change == 20 and (
                        (list(map(add, player.position[-1], [20, 0])) in player.position) or
                        player.position[-1][0] + 20 > (game.game_width - 20))) or (
                        player.x_change == 0 and player.y_change == -20 and ((list(map(
                    add, player.position[-1], [-20, 0])) in player.position) or player.position[-1][0] - 20 < 20)) or (
                        player.x_change == 20 and player.y_change == 0 and (
                        (list(map(add, player.position[-1], [0, -20])) in player.position) or player.position[-1][
                    -1] - 20 < 20)) or (
                    player.x_change == -20 and player.y_change == 0 and (
                        (list(map(add, player.position[-1], [0, 20])) in player.position) or
                        player.position[-1][-1] + 20 >= (game.game_height - 20))),  # danger left

            player.x_change == -20,  # move left
            player.x_change == 20,  # move right
            player.y_change == -20,  # move up
            player.y_change == 20,  # move down
            food.x_food < player.x,  # food left
            food.x_food > player.x,  # food right
            food.y_food < player.y,  # food up
            food.y_food > player.y  # food down
        ]

        for i in range(len(state)):
            if state[i]:
                state[i] = 1
            else:
                state[i] = 0

        return np.asarray(state)

    def set_reward(self, points, game_over):
        self.reward = 0
        if game_over:
            self.reward = -10
            return self.reward
        self.reward = points
        return self.reward

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay_new(self, memory, batch_size):
        if len(memory) > batch_size:
            minibatch = random.sample(memory, batch_size)
        else:
            minibatch = memory
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(np.array([next_state]))[0])
            target_f = self.model.predict(np.array([state]))
            target_f[0][np.argmax(action)] = target
            self.model.fit(np.array([state]), target_f, epochs=1, verbose=0)

    def train_short_memory(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            target = reward + self.gamma * np.amax(self.model.predict(next_state.reshape((1, 11)))[0])
        target_f = self.model.predict(state.reshape((1, 11)))
        target_f[0][np.argmax(action)] = target
        self.model.fit(state.reshape((1, 11)), target_f, epochs=1, verbose=0)