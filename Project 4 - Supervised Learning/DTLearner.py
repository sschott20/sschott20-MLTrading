import numpy as np

class DTLearner(object):

    def __init__(self, leaf_size=1, verbose=False):
        self.leaf_size = leaf_size
        print("DT init")
        pass  # move along, these aren't the drones you're looking for


    def addEvidence(self, dataX, dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """

        data = np.append(dataX, dataY[:, None], axis=1)
        self.tree = self.build_tree(data)
        # print(self.tree)
        # build and save the model
        # print("output: \n" + str(build_tree(data)))
    def query(self, points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        guesses = []
        for point in points:
            current_point = 0
            line = self.tree[current_point]
            feature = line[0]
            next_point = 0
            while feature != "Leaf":
                # print(point, line)
                if point[feature] <= line[1]:
                    next_point += line[2]
                if point[feature] > line[1]:
                    next_point += line[3]
                line = self.tree[next_point]
                feature = line[0]
            guesses.append(line[1])
        return np.array(guesses, dtype=float)


    def build_tree(self, data):
        if data.shape[0] <= self.leaf_size:
            return np.array([["Leaf", np.mean(data[:, -1]), "NA", "NA"]], dtype=object)
        # check to see if all Y data is the same and return leaf if so
        a = data[:, -1] == data[0, -1]
        if np.all(a): return np.array([["Leaf", data[0, -1], "NA", "NA"]], dtype=object)

        i = self.find_highest_coralation(data)
        SplitVal = np.median(data[:, i])
        left_tree_data = data[data[:, i] <= SplitVal]
        right_tree_data = data[data[:, i] > SplitVal]

        if left_tree_data.shape[0] == 0 or right_tree_data.shape[0] == 0:
            return np.array([["Leaf", np.mean(data[:, -1]), "NA", "NA"]])

        left_tree = self.build_tree(left_tree_data)
        right_tree = self.build_tree(right_tree_data)
        root = np.array([[i, SplitVal, 1, left_tree.shape[0] + 1]], dtype=object)

        return np.concatenate((root, left_tree, right_tree), axis=0)

    def find_highest_coralation(self, data):
        # Return index of feature with highest absolute correlation to outputs
        max_correlation = 0
        index = 0
        for i in range(data.shape[1] - 1):
            correlation = np.correlate(data[:, i], data[:, -1])
            if abs(correlation) > max_correlation:
                max_correlation = correlation
                index = i
        return index

if __name__ == "__main__":
    print("the secret clue is 'zzyzx'")
