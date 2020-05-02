import numpy as np

if __name__ == '__main__':
    maze = np.negative(np.ones((5,5), dtype=int))

    maze[-1,-1] = 100

    player = Ai()

    while True:
        player.update()


class Ai(object):
    def __init__(self):
        pass

    def update(self, board, position):

        reward =