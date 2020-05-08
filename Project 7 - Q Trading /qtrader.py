import pandas as pd
import qlearn_trading as qlearn
import qutil
from historical_data import *
import re

class QTrader(object):
    def __init__(self, actions, parameters, start_date, start_balance=100000, qfile='qtables/qtable.txt'):

        self.actions = actions
        self.start_balance = start_balance
        self.balance = start_balance
        self.parameters = parameters
        self.start_date = start_date
        self.holding = 0

        qtable = {}
        with open(qfile, "r") as f:
            lines = f.readlines()
        for line in lines:
            line = line.split(":")
            index = line[0].split(",")
            index[0] = int(re.sub("[^A-Za-z0-9]+", "", index[0]))
            index[1] = re.sub("[^A-Za-z0-9]+", "", index[1])
            value = line[1].strip("\n")
            value = float(value)
            qtable[(index[0], index[1])] = value


        self.value = pd.DataFrame()
        self.ai = qlearn.QLearn(
            actions, q=qtable, c=0.3, alpha=0.2, gamma=0.9, cdecay=0.9,
        )

    def calculate_state_value(self, stock, end_date, data):
        """
        range should be from start of data to latest date that the ai is allowed to see
        """

        date_range = pd.date_range("2010-01-01", end_date)
        adj_close = data['2010-01-01': end_date]
        self.adj_close = adj_close.copy()
        daily_return = (adj_close[1:] / adj_close.values[:-1]) - 1

        holding_value = float(adj_close.iloc[-1] * self.holding)
        # print(end_date, round(self.balance), self.holding, round(holding_value), round(float(adj_close.iloc[-1])))
        # self.value = self.value.append(
        #     pd.DataFrame({"Value": [(holding_return + self.balance) / self.balance]}, index=[end_date])
        # )
        self.value = self.value.append(
            pd.DataFrame({"Value": [holding_value + self.balance]}, index=[end_date])
        )

        reward = holding_value + self.balance - self.start_balance
        state = [1]

        if "Daily Return" in self.parameters:
            state.append(int(holding_value * 10000))
        if "Adj/SMA" in self.parameters:
            window = self.parameters["Adj/SMA"]
            sma = adj_close.iloc[:, 0].rolling(window=window).mean()
            adj = adj_close.iloc[:, 0]
            sma_adj = (sma / adj).dropna()
            steps = 30
            stepsize = math.floor(len(sma_adj) / steps)

            thresholds = []
            sma_adj = sma_adj.sort_values(0)
            thresholds.append(0)

            for i in range(0, steps):
                thresholds.append(round(sma_adj.iloc[((i + 1) * stepsize) - 1], 4))
            thresholds.append(10)

            discritized = pd.cut(
                sma_adj, bins=thresholds, labels=[x for x in range(steps + 1)]
            )

            x = discritized[date_range].dropna()

            state.append(x[-1])

        if "Bolinger Bands" in self.parameters:
            window = self.parameters['Bolinger Bands']
            rolling_mean = adj_close.iloc[:, 0].rolling(window=window).mean()
            rolling_std = adj_close.iloc[:, 0].rolling(window=window).std()
            factor = float((adj_close.iloc[-1] - rolling_mean[-1]) / (rolling_std[-1]))
            if factor >= 0:
                d = "1" + str(round(factor * 10))
            else:
                d = "2" + str(abs(round(factor * 10)))
            state.append(int(d))

        if "Holding" in self.parameters:
            state.append(self.holding)
        q = []
        for j in state:
            q.append("{0:0=3d}".format(j))
        state_int = int("".join(q))

        return state_int, reward

    def train(self, stock, start_date, end_date):
        self.balance = self.start_balance
        # self.value = pd.DataFrame({"Date": [start_date], "Value": [self.start_balance]})
        self.value = pd.DataFrame()
        self.holding = 0
        last_action = None
        last_state = None
        current_date = start_date

        date_range = pd.date_range("2010-01-01", end_date)
        adj_close = qutil.get_data([stock], date_range, removeSPY=True)

        self.trading_dates = qutil.get_data(
            ["SPY"], pd.date_range(start_date, end_date), removeSPY=False
        ).index

        for date in self.trading_dates:
            # print(self.balance, self.holding)
            state, reward = self.calculate_state_value(stock, date, adj_close)

            if last_state != None:
                self.ai.learn(last_state, last_action, reward, state)

            action = self.ai.choose_action(state)
            if action != "NNN":
                amount = int(action[1:3])
            else:
                amount = 0

            current_price = float(self.adj_close.iloc[-1])
            if action[0] == "S":
                if amount > self.holding:
                    amount = self.holding
                self.balance += current_price * amount
                self.holding -= amount
            elif action[0] == "B":
                while current_price * amount > self.balance:
                    amount -= 1
                action = "B" + str(amount)
                self.holding += amount
                self.balance -= current_price * amount
            last_state = state
            last_action = action

    def plot_port_value(self, normalized=False):

        self.value.index = pd.DatetimeIndex(self.value.index).normalize()
        if normalized:
            qutil.plot_data(self.value/self.value.values[0], "Portfolio Value")

    def output_table(self):
        with open("qtables/qtable.txt", "w+") as f:
            f.truncate(0)
            for i in self.ai.q:
                f.write(str(i))
                f.write(":")
                f.write(str(self.ai.q[i]))
                f.write("\n")