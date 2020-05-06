import qlearn


class Player(object):
    def __init__(self, actions, c=0.3, alpha=0.7, gamma=0.5, cdecay=0.999):
        self.actions = actions
        self.ai = qlearn.QLearn(actions, c=c, alpha=alpha, gamma=gamma)

    def new_game(self):
        self.last_state = None
        self.last_action = None

    def update(self, board, player_position, goal_position):
        reward = -1
        state = []
        for i in board:
            for j in i:
                state.append(j)

        # state = [board, player_position, goal_position]
        # state = state + player_position + goal_position
        state = player_position + goal_position
        string_state = [str(i) for i in state]
        a_string = "".join(string_state)
        state = int(a_string)

        if board[player_position[0], player_position[1]] == 3:
            reward = -1000
            if self.last_state is not None:
                self.ai.learn(self.last_state, self.last_action, reward, state)
            self.last_state = None
            return "end"

        if player_position == goal_position:
            reward = 1000
            if self.last_state is not None:
                self.ai.learn(self.last_state, self.last_action, reward, state)
            self.last_state = None
            return "end"

        if self.last_state is not None:
            self.ai.learn(self.last_state, self.last_action, reward, state)
        action = self.ai.choose_action(state)
        # print(action)
        self.last_state = state
        self.last_action = action

        return(self.last_action)
    def output_table(self, plays):
        with open(f"qtables/qtable-{plays}.txt", "w+") as f:
            f.truncate(0)
            for i in self.ai.q:
                f.write(str(i))
                f.write(":")
                f.write(str(self.ai.q[i]))
                f.write("\n")