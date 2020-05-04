import numpy as np
import qlearn
import time
import re

class Player(object):
    def __init__(self, actions, qfile='qtable.txt'):
        self.actions = actions


        qtable = {}
        # line[i] = (4239, 'right'):-1
        with open(qfile, "r") as f:
            lines = f.readlines()
        for line in lines:
            line = line.split(":")
            #["(69210, 'right')", '-1\n']

            index = line[0].split(",")
            index[0] = int(re.sub('[^A-Za-z0-9]+', '', index[0]))
            index[1] = re.sub('[^A-Za-z0-9]+', '', index[1])
            value = line[1].strip("\n")
            value = float(value)
            qtable[(index[0], index[1])] = value

        self.ai = qlearn.QLearn(actions, q=qtable, c=0, alpha=0.7, gamma=0.5)

    def new_game(self):
        self.last_state = None
        self.last_action = None

    def update(self, board, player_position, goal_position):
        state = []
        state = player_position + goal_position
        string_state = [str(i) for i in state]
        a_string = "".join(string_state)
        state = int(a_string)

        if board[player_position[0], player_position[1]] == 3:
            self.last_state = None
            return "end"

        if player_position == goal_position:
            self.last_state = None
            return "end"

        action = self.ai.choose_action(state)

        self.last_state = state
        self.last_action = action

        return(self.last_action)
