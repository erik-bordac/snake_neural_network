
from keras.optimizers import Adam
from keras import Sequential
from keras.layers import Dense, Dropout
import random
import numpy as np
import pandas as pd
from operator import add
import collections


class Agent():
    def __init__(self, params):
        self.reward = 0
        self.gamma = 0.9
        self.learning_rate = params['learning_rate']       
        self.epsilon = 1
        self.first_layer = params['first_layer_size']
        self.second_layer = params['second_layer_size']
        self.third_layer = params['third_layer_size']
        self.weights = params['weights_path']
        self.load_weights = params['load_weights']
        self.model = self.network()

    def network(self):
        model = Sequential()
        model.add(Dense(output_dim=self.first_layer, activation='relu', input_dim=11))
        model.add(Dense(output_dim=self.second_layer, activation='relu'))
        model.add(Dense(output_dim=self.third_layer, activation='relu'))
        model.add(Dense(output_dim=4, activation='softmax'))
        opt = Adam(self.learning_rate)
        model.compile(loss='mse', optimizer=opt)

        if self.load_weights:
            model.load_weights(self.weights)
        return model

    def set_reward(self, snake, crash):
        self.reward = 0
        if crash:
            self.reward = -10
            return self.reward
        if snake.ate:
            self.reward = 10
        return self.reward

    def train(self, state, action, reward, next_state, done):
        target = reward
        state = np.asarray(state)
        next_state = np.asarray(next_state)
        if not done:
            target = reward + self.gamma * np.amax(self.model.predict(next_state.reshape((1, 11)))[0])
        target_f = self.model.predict(state.reshape((1, 11)))
        target_f[0][np.argmax(action)] = target
        self.model.fit(state.reshape((1, 11)), target_f, epochs=1, verbose=0)
