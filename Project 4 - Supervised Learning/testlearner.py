import numpy as np
import math
import LinRegLearner as lrl
import DTLearner as dtl
import BagLearner as bl
import RTLearner as rtl
# import RTLearner as rtl
import sys

if __name__ == "__main__":
    # # Open and convert .csv
    inf = open('./Data/Istanbul.csv')
    data = np.genfromtxt(inf, delimiter=',')
    # For Istanbul.csv
    data = data[1:, 1:]

    # inf = open('./Data/winequality-red.csv')
    # data = np.genfromtxt(inf, delimiter=',')

    # Compute rows allocated to training and testing
    train_rows = int(0.6 * data.shape[0])

    # Training and testing data
    # Inputs (X) are worldwide index returns, output (Y) is emerging market EM return
    trainX = data[:train_rows, 0:-1]
    trainY = data[:train_rows, -1]
    testX = data[train_rows:, 0:-1]
    testY = data[train_rows:, -1]

    learner = bl.BagLearner(learner=rtl.RTLearner, kwargs={"leaf_size": 1}, bags=100, boost=False,
                            verbose=False, sample_percent=1)
    # learner = dtl.DTLearner(leaf_size=1)
    # learner = dtl.DTLearner(leaf_size=2)
    learner.addEvidence(trainX, trainY)
    Y = learner.query(testX)

    print(f"{testX.shape}")
    print(f"{testY.shape}")
    for i in range(10):
        print(round(Y[i], 4), " : ", round(data[train_rows + i, -1], 4))
    # evaluate in sample
    predY = learner.query(trainX)

    print(trainY.shape)
    predY = predY[:, None]
    trainY = trainY[:, None]

    # Calculate statistics
    rmse = math.sqrt(((trainY - predY) ** 2).sum() / trainY.shape[0])
    print("In sample results")
    print(f"RMSE: {rmse}")
    c = np.corrcoef(predY.T, trainY.T)
    print(f"corr: {c[0, 1]}")

    # evaluate out of sample
    predY = learner.query(testX)
    rmse = math.sqrt(((testY - predY) ** 2).sum() / testY.shape[0])
    print()
    print("Out of sample results")
    print(f"RMSE: {rmse}")
    c = np.corrcoef(predY.T, testY.T)
    print(f"corr: {c[0, 1]}")