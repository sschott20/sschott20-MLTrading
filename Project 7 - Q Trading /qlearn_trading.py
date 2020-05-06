import random


class QLearn(object):
    def __init__(self, actions, q=None, c=0.3, alpha=0.2, gamma=0.9, cdecay=0.999):
        # table of [state,action] pairs and Q values
        if q is None:
            self.q = {}
        else:
            self.q = q
        # probability to randomly select an action instead of choosing highest Q value
        self.c = c
        self.cdecay = cdecay
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
        if random.random() < self.c:
            self.c = self.cdecay * self.c
            # print("c= ", self.c)
            return random.choice(self.actions)
        else:
            q = [self.get_q(state, a) for a in self.actions]
            maxQ = max(q)
            count = q.count(maxQ)
            if count > 1:
                best = [i for i in range(len(self.actions)) if q[i] == maxQ]
                i = random.choice(best)
            else:
                i = q.index(maxQ)
            action = self.actions[i]
            return action

    def learn(self, state1, action1, reward, state2):
        max_future_reward = max([self.get_q(state2, a) for a in self.actions])
        # print("max future q: ", max_future_reward)
        self.learn_q(state1, action1, reward, max_future_reward)
