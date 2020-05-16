import duel_qlearn as qlearn
import re

class Trapper(object):
    def __init__(self, actions, map_size, qfile="qtables/trapper_q.txt", c=0.3, alpha=0.7, gamma=0.5, cdecay=0.999):
        self.actions = actions

        self.map_size = map_size
        self.last_state = None
        self.last_action = None

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

        self.ai = qlearn.QLearn(actions, q=qtable, c=c, alpha=alpha, gamma=gamma)
    def new_game(self):
        self.last_state = None
        self.last_action = None

    def update(self, board, position):
        reward = 1
        state = []

        if board[position[0], position[1]] == 1:
            reward = 1000
        elif board[position[0], position[1]] == 3:
            reward = -1000

        row_start = position[0] - 4
        row_end = position[0] + 5
        col_start = position[1] - 4
        col_end = position[1] + 5
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
        state.append(str(position[1]))
        state.append(str(position[0]))

        a_string = "".join(state)
        state = int(a_string)

        action = self.ai.choose_action(state)

        wall_position =[int(action[0]), int(action[1])]

        if self.map_size - 1 > wall_position[0] + position[0] - 2 > 1:
            if self.map_size - 1 > wall_position[1] + position[1] - 2 > 1:
                reward -= 50

        if self.last_state is not None:
            self.ai.learn(self.last_state, self.last_action, reward, state)

        self.last_state = state
        self.last_action = action

        return self.last_action

    def output_table(self, plays):
        with open(f"qtables/trapper_q.txt", "w+") as f:
            for i in self.ai.q:
                f.write(str(i))
                f.write(":")
                f.write(str(self.ai.q[i]))
                f.write("\n")
