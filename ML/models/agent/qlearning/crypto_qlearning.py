from math import log10

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ML.models.agent.data_preprocess import preprocess
from datetime import datetime
import itertools
import argparse
import re
import os
import pickle
import sys
from sklearn.preprocessing import StandardScaler

scaler = None
# ROOT = sys.path[1] + '/data/'
# ROOT = '../../../../data/'
ROOT = '/home/afshin/tmp/pycharm_project_266/data/'
EPISODE_COUNTER = 0
MODE = 'Train'


# PRICE_COLUMNS = ['close']
# DIFFERENCE_COLUMNS = ['difference']


# create a scaler by playing a random episode and fitting the scaler on the observed states.
# can become more accurate by running the code for multiple episodes
def get_scaler(env):
    states = []
    for i in range(env.n_step):
        # print(f'iter {i}')
        action = np.random.choice(env.action_space)
        state, reward, done, info = env.step(action)
        states.append(state)
        if done:
            break

    scaler = StandardScaler()
    scaler.fit(states)
    return scaler


# creating a directory if it does not exist - utility function
def maybe_make_dir(dir):
    if not os.path.exists(dir):
        print('creating directory')
        os.mkdir(dir)


class LinearModel:
    def __init__(self, input_dim, n_actions):
        self.W = np.random.randn(input_dim, n_actions) / np.sqrt(input_dim)
        self.b = np.zeros(n_actions)
        # used for momentum in gradient descent
        self.vW = 0
        self.vb = 0
        self.losses = []

    def predict(self, X):
        # X must be of shape N * D and 2D
        assert (len(X.shape) == 2)
        # print(self.W)
        # print(self.b)
        # print(X)
        return X.dot(self.W) + self.b

    def sgd(self, X, Y, learning_rate=0.01, momentum=0.9):
        # X must be of shape N * D and 2D
        assert (len(X.shape) == 2)
        num_values = np.prod(Y.shape)
        Yhat = self.predict(X)
        gW = 2 * X.T.dot(Yhat - Y) / num_values
        gb = 2 * (Yhat - Y).sum(axis=0) / num_values

        # updating the momentum
        self.vW = momentum * self.vW - learning_rate * gW
        self.vb = momentum * self.vb - learning_rate * gb

        # update params
        self.W += self.vW
        self.b += self.vb

        mse = np.float128(np.mean((Yhat - Y) ** 2))
        self.losses.append(mse)

    def load_weights(self, filepath):
        npz = np.load(filepath)
        self.W = npz['W']
        self.b = npz['b']

    def save_weights(self, filepath):
        np.savez(filepath, W=self.W, b=self.b)


class MultiStockEnv:
    """
      A 3-stock trading environment.
      State: vector of size 7 (n_stock * 2 + 1)
        - # shares of stock 1 owned
        - # shares of stock 2 owned
        - # shares of stock 3 owned
        - price of stock 1 (using daily close price)
        - price of stock 2
        - price of stock 3
        - cash owned (can be used to purchase more stocks)
      Action: categorical variable with 27 (3^3) possibilities
        - for each stock, you can:
        - 0 = sell
        - 1 = hold
        - 2 = buy
      """

    def __init__(self, data, coin_n, state_mode, initial_coins=None, initial_investment=20000):
        # information about the data
        self.coin_price_history = data
        self.n_step = data.shape[0]
        self.n_coins = coin_n
        # controlling variables
        self.cur_step = None
        self.coin_owned = None
        self.coin_price = None
        self.coin_difference = None
        self.initial_investment = initial_investment
        self.initial_coins = initial_coins
        self.cash_in_hand = None
        self.action_space = np.arange(3 ** self.n_coins)
        """
         used to indicate which sort of state we want 1: only price 2: only difference 3: combination
        """
        self.mode = state_mode
        # creates all the permutations of the actions for each stock
        """
        actions:
            sell = 0
            hold = 1
            buy = 2
        """
        self.action_list = list(map(list, itertools.product([0, 1, 2], repeat=self.n_coins)))
        if self.mode == 1 or self.mode == 2:
            self.state_dim = 2 * self.n_coins + 1
        elif self.mode == 3:
            self.state_dim = 3 * self.n_coins + 1
        elif self.mode == 4:
            self.state_dim = 5 * self.n_coins + 1
        self.reset()

    def reset(self):
        self.cur_step = 0
        if self.initial_coins is None:
            self.coin_owned = np.zeros(self.n_coins)
        else:
            self.coin_owned = self.initial_coins.copy()
        self.coin_price = self.coin_price_history[self.cur_step, 0]
        # TODO: the position of columns for difference columns needs to be dynamic
        self.coin_difference = self.coin_price_history[self.cur_step, 1]
        self.coin_indicators = self.coin_price_history[self.cur_step, -2:].flatten()
        self.cash_in_hand = self.initial_investment
        return self._get_obs()

    def step(self, action):
        # check if the action is valid
        assert action in self.action_space

        prev_val = self._get_val()
        self.cur_step += 1
        self.coin_price = self.coin_price_history[self.cur_step, 0]
        self.coin_difference = self.coin_price_history[self.cur_step, 1]
        self.coin_indicators = self.coin_price_history[self.cur_step, -2:].flatten()
        self._trade(action)
        cur_val = self._get_val()
        reward = cur_val - prev_val

        done = (self.cur_step == self.n_step - 1)
        info = {'cur_val': cur_val}

        return self._get_obs(), reward, done, info

    # return observation/state
    def _get_obs(self):
        state = np.empty(self.state_dim)
        if self.mode == 1:
            state[:self.n_coins] = self.coin_owned
            state[self.n_coins:2 * self.n_coins] = self.coin_price
        elif self.mode == 2:
            state[:self.n_coins] = self.coin_owned
            state[self.n_coins:2 * self.n_coins] = self.coin_difference
        elif self.mode == 3:
            state[:self.n_coins] = self.coin_owned
            state[self.n_coins:2 * self.n_coins] = self.coin_price
            state[2 * self.n_coins:3 * self.n_coins] = self.coin_difference
        # indicator mode
        elif self.mode == 4:
            state[:self.n_coins] = self.coin_owned
            state[self.n_coins:2 * self.n_coins] = self.coin_price
            state[2 * self.n_coins:3 * self.n_coins] = self.coin_difference
            # TODO: make it dynamic
            state[3 * self.n_coins:5 * self.n_coins] = self.coin_indicators
        # state[-1] = log10(self.cash_in_hand)
        state[-1] = self.cash_in_hand
        return state

    def _get_val(self):
        return self.coin_owned.dot(self.coin_price) + self.cash_in_hand

    def _trade(self, action):
        action_vec = self.action_list[action]
        sell_indices = []
        buy_indices = []
        for i, a in enumerate(action_vec):
            if a == 0:
                sell_indices.append(i)
            elif a == 2:
                buy_indices.append(i)
        if sell_indices:
            # the sell action sells all the stocks of the certain stock
            for i in sell_indices:
                self.cash_in_hand += self.coin_price[i] * self.coin_owned[i]
                self.coin_owned[i] = 0

        if buy_indices:
            # the buy action buys 1 of each stock until there is no more cash is left
            can_buy = True
            while can_buy:
                for i in buy_indices:
                    if self.cash_in_hand > self.coin_price[i]:
                        self.coin_owned[i] += 1  # buy one share
                        self.cash_in_hand -= self.coin_price[i]
                    else:
                        can_buy = False


class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = 0.9
        self.epsilon = 1
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.model = LinearModel(state_size, action_size)

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def train(self, state, action, reward, next_state, done):
        if done:
            target = reward
        else:
            target = reward + self.gamma * np.amax(self.model.predict(next_state), axis=1)
        # So we only calculated the target for the action we took
        # We need to keep the value for the other targets the same
        target_full = self.model.predict(state)
        # We change the value for the action we took to the new target - the others remain the same
        target_full[0, action] = target

        self.model.sgd(state, target_full)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)


def play_one_episode(agent, env, is_train):
    state = env.reset()
    non_scaled_state = state
    state = scaler.transform([state])
    done = False
    episode_data = []
    while not done:
        action = agent.act(state)

        t = np.append(non_scaled_state, env.action_list[action])
        episode_data.append(t.tolist())

        next_state, reward, done, info = env.step(action)
        non_scaled_state = next_state
        next_state = scaler.transform([next_state])
        if is_train == 'train':
            agent.train(state, action, reward, next_state, done)
        state = next_state

    return info['cur_val'], episode_data


if __name__ == '__main__':
    batch_size = 128
    n_coins = 3
    initial_investment = 10000
    # initial_investment = 0
    initial_coins = None
    # initial_coins = np.array([10.0, 10.0, 10.0])  # 6618$
    # initial_coins = np.array([10.0])  # 6618$
    num_episodes = 1000
    state_mode = 4
    # if_single = True
    if_single = False
    models_folder = ROOT + 'linear_rl_trader_models'
    rewards_folder = ROOT + 'linear_rl_trader_rewards'

    # creating an argument parser object to run the code in command line
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', type=str, required=True,
                        help='either "train" or "test"')
    args = parser.parse_args()

    maybe_make_dir(models_folder)
    maybe_make_dir(rewards_folder)
    address = 'combined_h_4'
    # address = 'ethereum_h_4'
    # columns_we_want = ['close', 'difference', 'STOCHRSIk_14_14_3_3', 'STOCHRSId_14_14_3_3']
    # columns_we_want = ['close', 'difference']
    columns_we_want = ['close', 'difference','mfi_14','sma_14']
    data = preprocess(address + '.csv', columns=columns_we_want, n_coins=n_coins)

    n_timesteps = data.shape[0]
    n_train = n_timesteps // 2

    # data from the beginning of 2021
    n_train = 9669
    # n_train = 10494

    # data = np.stack((price_data, difference_data), axis=1)
    train_data = data[:n_train]
    test_data = data[n_train:]

    env = MultiStockEnv(train_data, coin_n=n_coins, state_mode=state_mode, initial_coins=initial_coins,
                        initial_investment=initial_investment)
    state_size = env.state_dim
    action_size = len(env.action_space)
    agent = DQNAgent(state_size, action_size)
    scaler = get_scaler(env)

    # store the final value of the portfolio (end of episode)
    portfolio = []

    # changing some parameters in case we are in testing mode
    if args.mode == 'test':
        # load the previous scaler
        with open(f'{models_folder}/{address}_scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)

        # remake the env with test data
        env = MultiStockEnv(test_data, coin_n=n_coins, state_mode=state_mode, initial_coins=initial_coins,
                            initial_investment=initial_investment)

        # make sure epsilon is not 1!
        # no need to run multiple episodes if epsilon = 0, it's deterministic
        agent.epsilon = 0.01

        # agent.epsilon = 0.0

        # load trained weights
        agent.load(f'{models_folder}/{address}_linear.npz')

        # play the game num_episodes times
    for e in range(num_episodes):
        # print(f'episode: {e}')
        t0 = datetime.now()
        val, episode_data = play_one_episode(agent, env, args.mode)
        # TODO: needs to be dynamic
        # if args.mode == 'test':
        # episode_columns = ['coin_1', 'coin_2', 'coin_3',
        #                    'coin_price_1', 'coin_price_2', 'coin_price_3',
        #                    'difference_percentage_1', 'difference_percentage_2', 'difference_percentage_3',
        #                    'cash_at_hand',
        #                    'action_1', 'action_2', 'action_3']
        # episode_df = pd.DataFrame(episode_data, columns=episode_columns)
        # episode_df.to_csv(ROOT + f'/backtest/test{e}.csv')
        dt = datetime.now() - t0
        print(f"episode: {e + 1}/{num_episodes}, episode end value: {val:.2f}, duration: {dt}")
        portfolio.append(val)  # append episode end portfolio value

        # save the weights when we are done
    if args.mode == 'train':
        # save the DQN
        agent.save(f'{models_folder}/{address}_linear.npz')

        # save the scaler
        with open(f'{models_folder}/{address}_scaler.pkl', 'wb') as f:
            pickle.dump(scaler, f)

        # # plot losses
        # plt.plot(agent.model.losses)
        # plt.show()

        # save portfolio value for each episode
    np.save(f'{rewards_folder}/{address}_{args.mode}.npy', portfolio)
