import numpy as np
import player
import smart_player
import random
from array_backed_grid import display
import time


def start_game(maze_template, player, delay=0, output=False):
    game_end = False
    display_grids = []

    player_position = [random.randint(1, MAP_SIZE - 2), random.randint(1, MAP_SIZE - 2)]
    goal_position = [random.randint(1, MAP_SIZE - 2), random.randint(1, MAP_SIZE - 2)]
    # player_position = [1,1]
    # goal_position = [1,3]
    while maze_template[player_position[0], player_position[1]] == 3:
        player_position = [
            random.randint(1, MAP_SIZE - 2),
            random.randint(1, MAP_SIZE - 2),
        ]
    while maze_template[goal_position[0], goal_position[1]] != 0:
        goal_position = [
            random.randint(1, MAP_SIZE - 2),
            random.randint(1, MAP_SIZE - 2),
        ]

    maze_display = np.copy(maze_template)

    maze_display[goal_position[0], goal_position[1]] = 2
    maze_display[player_position[0], player_position[1]] = 1

    player.new_game()
    if output:
        for j in range(10):
            display_grids.append(maze_display)
    i = 0
    while not game_end:
        i += 1
        new_goal_position = [0, 0]
        new_goal_position[0] = goal_position[0] + random.choice([-1, 1, 0])
        new_goal_position[1] = goal_position[1] + random.choice([-1, 1, 0])
        # goal_position[0] += 1
        # goal_position[1] += 1
        if (
            maze_template[new_goal_position[0], new_goal_position[1]] != 3
            and goal_position != player_position
        ):
            goal_position = new_goal_position
        maze_display = np.copy(maze_template)
        maze_display[goal_position[0], goal_position[1]] = 2
        maze_display[player_position[0], player_position[1]] = 1
        if output:
            display_grids.append(maze_display)

        action = player.update(maze_template, player_position, goal_position)
        if i > 100:
            if output:
                a = 1 / 0
            else:
                action = "end"
        if action == "left":
            player_position[1] -= 1
        elif action == "right":
            player_position[1] += 1
        elif action == "up":
            player_position[0] -= 1
        elif action == "down":
            player_position[0] += 1
        elif action == "end":
            game_end = True
            if output:
                display(display_grids)
            break
        # Prep maze to be displayed to the observer
        maze_display = np.copy(maze_template)
        maze_display[goal_position[0], goal_position[1]] = 2
        maze_display[player_position[0], player_position[1]] = 1
        if output:
            display_grids.append(maze_display)


if __name__ == "__main__":

    training_steps = 200000
    actions = ["left", "right", "up", "down"]
    training_player = player.Player(
        actions, alpha=0.3, gamma=0.9, c=0.5, cdecay=0.999999
    )
    MAP_SIZE = 26
    maze_template = np.zeros((MAP_SIZE, MAP_SIZE), dtype=int)
    maze_template[0, :] = 3
    maze_template[1:, 0] = 3
    maze_template[1:, -1] = 3
    maze_template[-1, 1:-1] = 3
    for i in range(6):
        a, b = random.randint(1, MAP_SIZE - 2), random.randint(1, MAP_SIZE - 2)

        maze_template[a, b : b + random.randint(3, 7)] = 3
    for i in range(6):
        a, b = random.randint(1, MAP_SIZE - 2), random.randint(1, MAP_SIZE - 2)
        maze_template[a : a + random.randint(3, 7), b] = 3
    for i in range(150):
        maze_template[
            random.randint(1, MAP_SIZE - 2), random.randint(1, MAP_SIZE - 2)
        ] = 3

    print("Training Start")
    for i in range(training_steps + 1):
        if i % 2500 == 0:
            training_player.output_table(i)
            print(i)
        start_game(
            delay=0, output=False, maze_template=maze_template, player=training_player
        )
    print("Training Complete")

    print(f"--- {training_steps} Games Completed ---")

    print("Starting Testing")
    player_list = []
    for i in range(0, training_steps + 1, 2500):
        file = "qtables/qtable-" + str(i) + ".txt"
        player_list.append(smart_player.Player(actions, qfile=file))
    for n, ai in enumerate(player_list):
        print(n * 2500)
        for i in range(1):
            t = True
            while t:
                try:
                    start_game(
                        delay=0, output=True, maze_template=maze_template, player=ai
                    )
                    t = False
                except:
                    pass
