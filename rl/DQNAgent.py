import random
import collections
from os.path import join, isfile

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten
from tensorflow.keras.optimizers import Adam
from tqdm import tqdm


class DQNAgent:

    def __init__(self, name):
        self.model = None
        self.name = name
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
        self.memory = collections.deque(maxlen=10000)

    def network(self, width, height, action_size, weight_path=None):
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

        if weight_path is not None:
            index_file = join(weight_path, self.name + ".index")
            if isfile(index_file):
                weights_path = join(weight_path, self.name)
                self.model.load_weights(weights_path)

    def save_weights(self, weight_path):
        if weight_path is not None:
            weights_path = join(weight_path, self.name)
            self.model.save_weights(weights_path)

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

        for state, action, reward, next_state, done in tqdm(minibatch):
            self.train_short_memory(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        next_state_array = np.array([next_state])
        state_array = np.array([state])
        target = reward
        if not done:
            target = reward + self.gamma * np.amax(self.model.predict(next_state_array)[0])
        target_f = self.model.predict(state_array)
        target_f[0][action] = target
        self.model.fit(state_array, target_f, epochs=1, verbose=0)
