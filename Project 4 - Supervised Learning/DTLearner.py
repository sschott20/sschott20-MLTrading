import numpy as np


class DecisionTree(object):

    def __init__(self, leaf_size=1, verbose=False):
        print("DT init")
        pass  # move along, these aren't the drones you're looking for


    def addEvidence(self, dataX, dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """

        data = np.append(dataX, dataY[:, None], axis=1)
        print(data)
        # build and save the model
        # print("output: \n" + str(build_tree(data)))

    def query(self, points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        return (self.model_coefs[:-1] * points).sum(axis=1) + self.model_coefs[-1]

def build_tree(data):
    # return leaf if input has only one row
    if data.shape[0] == 1: return ([-1, data[0][12], -1, -1])

    # check to see if all Y data is the same and return leaf if so
    a = dataY == dataY[0]
    if np.all(a): return([-1, dataY[0]], -1, -1)
    else:
        # determine best feature, xi, to split on
        i = 2
        SplitVal = dataX[:i].median()
        left_tree = build_tree(data)




if __name__ == "__main__":
    print("the secret clue is 'zzyzx'")
