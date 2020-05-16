import duel_qlearn as qlearn
import re
import numpy as np


class Mouse(object):
    def __init__(
            self,
            actions,
            map_size,
            qfile="qtables/mouse_q.txt",
            c=0.3,
            alpha=0.2,
            gamma=0.9,
            cdecay=0.9999,
    ):
        self.actions = actions

        self.last_x, self.last_y = 0, 0
        self.map_size = map_size
        self.middle = map_size / 2
        self.furthest = 0

        qtable = {}
        # line[i] = (4239, 'right'):-1
        with open(qfile, "r") as f:
            lines = f.readlines()
        for line in lines:
            line = line.split(":")
            # ["(69210, 'right')", '-1\n']

            index = line[0].split(",")
            index[0] = int(re.sub("[^A-Za-z0-9]+", "", index[0]))
            index[1] = re.sub("[^A-Za-z0-9]+", "", index[1])
            value = line[1].strip("\n")
            value = float(value)
            qtable[(index[0], index[1])] = value

        self.ai = qlearn.QLearn(actions, q=qtable, c=c, alpha=alpha, gamma=gamma, cdecay=cdecay)
    def new_game(self):
        self.last_state = None
        self.last_action = None
        self.furthest_y = 0
        self.furthest_x = 0

    def update(self, board, position):
        reward = -1
        game_end = None
        state = []
        if board[position[0], position[1]] == 1:
            # lose
            reward = -1000
            game_end = "Lose"
        elif board[position[0], position[1]] == 3:
            # win
            reward = 1000
            # print("WIN")
            game_end = "Win"


        state.append(str(position[1]))
        state.append(str(position[0]))
        state.append("99")
        row_start = position[0] - 2
        row_end = position[0] + 3
        col_start = position[1] - 2
        col_end = position[1] + 3
        if row_start < 0:
            row_start = 0
        elif row_end > self.map_size - 1:
            row_end = self.map_size - 1
        if col_start < 0:
            col_start = 0
        elif col_end > self.map_size - 1:
            col_end = self.map_size - 1
        a = board[
            row_start: row_end, col_start: col_end
            ]
        for i in a:
            for j in i:
                state.append(str(int(j)))
        a_string = "".join(state)
        state = int(a_string)

        if self.last_state is not None:
            self.ai.learn(self.last_state, self.last_action, reward, state)

        if game_end == "Win" or game_end == "Lose":
            return game_end



        action = self.ai.choose_action(state)

        self.last_state = state
        self.last_action = action

        return self.last_action

    def output_table(self, plays):
        with open(f"qtables/mouse_q.txt", "w+") as f:
            # f.truncate(0)
            for i in self.ai.q:
                f.write(str(i))
                f.write(":")
                f.write(str(self.ai.q[i]))
                f.write("\n")
