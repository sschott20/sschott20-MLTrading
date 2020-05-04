import numpy as np
import player
import smart_player
import random
from Game import start_game

if __name__ == "__main__":
    training_steps = 10000
    actions = ["left", "right", "up", "down"]
    training_player = player.Player(actions, c=0.5, cdecay=0.9999)
    MAP_SIZE = 15
    maze_template = np.zeros((MAP_SIZE, MAP_SIZE), dtype=int)
    maze_template[0, :] = 3
    maze_template[1:, 0] = 3
    maze_template[1:, -1] = 3
    maze_template[-1, 1:-1] = 3
    maze_template[3, 3:6] = 3
    maze_template[5, 3:10] = 3
    maze_template[7:11, 3] = 3
    maze_template[3:11, 11] = 3
    maze_template[9, 5:10] = 3
    for i in range(10):
        maze_template[random.randint(1, MAP_SIZE - 2), random.randint(1, MAP_SIZE - 2)] = 3

    print("Training Start")
    for i in range(training_steps):
        start_game(delay=0, output=False, maze_template=maze_template, player=training_player)

    training_player.output_table(training_steps)
    print("Training Complete")

    print(f"--- {training_steps} Games Completed ---")

    print("Starting Testing")
    smart_player = smart_player.Player(actions, qfile="qtable-10000.txt")
    for i in range(4):
        print("Game: ", i + 1)
        start_game(delay=0, output=True, maze_template=maze_template, player=smart_player)
