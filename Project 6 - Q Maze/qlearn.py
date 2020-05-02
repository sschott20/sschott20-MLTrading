import random


class QLearn(object):
    def __init__(self, actions, c=0.1, alpha=0.2, gamma=0.9):
        # table of [state,action] pairs and Q values
        self.q = {}

        # probability to randomly select an action instead of choosing highest Q value
        self.c = c

        # adoption rate of new Q values
        self.alpha = alpha

        # value of later rewards as opposed to immediate rewards
        self.gamma = gamma

        # things that can be done, presented as a list of integers
        self.actions = actions

        def get_q(self, state, action):
            # searches Q table for (state,action) and returns 0 if it doesn't exist
            return self.q.get((state, action), 0.0)

        def learn_q(self, state, action, reward, max_future_reward):

            # get current q value for (state, action) and return None if it doesn't exist yet
            oldq = self.q.get((state, action), None)

            if oldq == None:
                self.q[(state, action)] = reward
            else:
                self.q[(state, action)] = (1 - self.alpha) * oldq + self.alpha * (
                    reward + self.gamma * max_future_reward
                )

        def choose_action(self, state):
            if random.random() < c:
                return random.choice(self.actions)
            else:
                qmax = max([self.q.get(state, a) for a in self.actions])
                acceptable_actions = []
                for a in actions:
                    if self.q.get(state, a) == qmax:
                        acceptable_actions.append(a)
                return random.choice(acceptable_actions)

        def learn(self, state1, action1, reward, state2):
            max_future_reward = max([self.q.get(state2, a) for a in self.actions])
            self.learn_q(state1, action1, reward, max_future_reward)
