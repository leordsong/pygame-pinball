import random
import collections

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten
from tensorflow.keras.optimizers import Adam


class DQNAgent:

    def __init__(self):
        self.model = None
        self.reward = 0
        self.learning_rate = 0.0005
        self.max_steps = 60 * 60 * 5  # play at least 5 minutes for each episode

        # Q learning hyperparameters
        self.gamma = 0.9

        # Exploration hyperparameters for epsilon greedy strategy
        self.explore_start = 1.0  # exploration probability at start
        self.explore_stop = 0.01  # minimum exploration probability
        self.decay_rate = 0.0001  # exponential decay rate for exploration prob
        self.epsilon = 0

        # Memory hyperparameters
        self.short_memory = collections.deque(maxlen=4)
        self.memory = collections.deque(maxlen=2500)

    def network(self, width, height, action_size):
        model = Sequential()
        model.add(Conv2D(16, 8, strides=[8, 8], activation='relu', input_shape=(width, height, 3)))
        model.add(Conv2D(16, 4, strides=[4, 4], activation='relu'))
        model.add(Flatten())
        model.add(Dense(100, activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(action_size, activation='softmax'))
        opt = Adam(self.learning_rate)
        model.compile(loss='mse', optimizer=opt)
        self.model = model

    def adjust_epsilon(self, step):
        self.epsilon = self.explore_stop + (self.explore_start - self.explore_stop) * np.exp(-self.decay_rate * step)

    def set_reward(self, points, game_over):
        self.reward = -10 if game_over else points
        return self.reward

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def predict(self, state):
        train_state = np.array([state])
        return self.model.predict(train_state)

    def reset(self):
        # reset stack
        self.short_memory.clear()
        self.reward = 0

    def train(self, memory, batch_size):
        if len(memory) > batch_size:
            minibatch = random.sample(memory, batch_size)
        else:
            minibatch = memory

        for state, action, reward, next_state, done in minibatch:
            next_state_array = np.array([next_state])
            state_array = np.array([state])
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state_array)[0])
            target_f = self.model.predict(state_array)
            target_f[0][action] = target
            self.model.fit(state_array, target_f, epochs=1, verbose=0)

    def train_short_memory(self, state, action, reward, next_state, done):
        target = reward
        train_state = np.array([next_state]).reshape([1, 300, 500, 1])
        # if not done:
        #     target = reward + self.gamma * np.amax(self.model.predict(train_state)[0])
        target_f = self.model.predict(train_state)
        target_f[0][np.argmax(action)] = target
        self.model.fit(train_state, target_f, epochs=1, verbose=0)
