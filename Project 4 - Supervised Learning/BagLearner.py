import numpy as np

class BagLearner(object):

    def __init__(self, learner, kwargs, bags, boost, sample_percent, verbose=False):
        self.learners_list = []
        self.learner = learner
        for i in range(0, bags):
            self.learners_list.append(learner(**kwargs))
        self.bags = bags
        self.boost = boost
        self.verbose = verbose
        self.sample_percent = sample_percent
        pass  # move along, these aren't the drones you're looking for


    def addEvidence(self, dataX, dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        data = np.append(dataX, dataY[:, None], axis=1)

        learners_data = []

        for i in range(0, self.bags):
            random_indecies = np.random.choice(data.shape[0], int(self.sample_percent * data.shape[0]), replace=False)
            learners_data.append(data[random_indecies, :])

        for i in range(0, self.bags):
            self.learners_list[i].addEvidence(learners_data[i][:, :-1], learners_data[i][:, -1])

    def query(self, points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        q = []
        for learner in self.learners_list:
            q.append(learner.query(points))
        q_array = np.array(q)
        ans = np.mean(q_array, axis=0)

        return ans


if __name__ == "__main__":
    print("the secret clue is 'zzyzx'")
