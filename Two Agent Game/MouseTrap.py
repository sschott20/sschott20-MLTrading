import numpy as np
import random
from display_grid import display
from trapper import Trapper
from mouse import Mouse
import time
from math import floor, ceil

def start_game(template, delay=0, output=True):
    game_end = False
    display_grids = []
    board = np.copy(template)
    mouse.new_game()
    # trapper.new_game()
    n = MAP_SIZE / 2
    middle_square = [floor(n), ceil(n), floor(n) - 1, ceil(n) - 1, floor(n) - 2, ceil(n) - 2]
    mouse_position = [random.choice(middle_square), random.choice(middle_square)]

    board_display = np.copy(board)
    board_display[mouse_position[0], mouse_position[1]] = 2

    i = 0
    while not game_end:
        i += 1

        # for i in range(1):
        #     while True:
        #         new_wall = [
        #             random.randint(1, MAP_SIZE - 2),
        #             random.randint(1, MAP_SIZE - 2),
        #         ]
        #
        #         if new_wall != mouse_position:
        #             break
        #     board[new_wall[0], new_wall[1]] = 1

        board_display = np.copy(board)
        board_display[mouse_position[0], mouse_position[1]] = 2
        if output:
            display_grids.append(board_display)

        trapper_action = trapper.update(board, mouse_position)
        wall_position = [int(trapper_action[0]), int(trapper_action[1])]
        q, c = wall_position[0] + mouse_position[0] - 2, wall_position[1] + mouse_position[1] - 2

        if MAP_SIZE - 1 > q > 1:
            if MAP_SIZE - 1 > c > 1:
                if [q,c] != mouse_position:
                    board[q, c] = 1

        # print(mouse_position, wall_position, wall_position[0] + mouse_position[0] - 2, wall_position[1] + mouse_position[1] - 2)
        board_display = np.copy(board)
        board_display[mouse_position[0], mouse_position[1]] = 2
        if output:
            display_grids.append(board_display)

        mouse_action = mouse.update(board, mouse_position)

        if mouse_action == "left":
            mouse_position[1] -= 1
        elif mouse_action == "right":
            mouse_position[1] += 1
        elif mouse_action == "up":
            mouse_position[0] -= 1
        elif mouse_action == "down":
            mouse_position[0] += 1
        elif mouse_action == "Win" or mouse_action == "Lose":
            winner = mouse_action
            game_end = True
        # elif mouse_action == 'Can't Move':
        #     game_end = True

        # Prep maze to be displayed to the observer
        board_display = np.copy(board)
        board_display[mouse_position[0], mouse_position[1]] = 2

        if output and not game_end:
            # for i in range(20):
            display_grids.append(board_display)

        # game_end = True
    if output:
        display(display_grids)

    time.sleep(delay)
    return winner

if __name__ == "__main__":
    print(" --- Init ---")
    MAP_SIZE = 19
    training_steps = 100000
    actions_mouse = ["left", "right", "up", "down"]
    actions_trapper = []
    winlog = []
    for i in range(9):
        for j in range(9):
            a = str(i) + str(j)
            if a != "44":
                actions_trapper.append(a)

    board_template = np.zeros([MAP_SIZE, MAP_SIZE])
    board_template[0, :] = 3
    board_template[-1, :] = 3
    board_template[:, 0] = 3
    board_template[:, -1] = 3
    print(" --- Loading Q Files --- ")
    trapper = Trapper(actions_trapper, MAP_SIZE, c=0)
    mouse = Mouse(actions_mouse, MAP_SIZE, c=0)
    print(" --- Training start --- ")
    start_time = time.time()
    # for i in range(10):
    #     start_game(board_template, output=True, delay=0)

    for i in range(training_steps + 1):
        if i % 10000 == 0:
            print(i, round(time.time() - start_time))
            for i in range(5):
                winlog.append(start_game(board_template, output=True))


        winlog.append(start_game(board_template, output=False))
    print(f" --- Training end --- ")
    print(f" --- {training_steps} games completed over {round(time.time() - start_time, 2)} seconds --- ")
    mouse.output_table(training_steps)
    trapper.output_table(training_steps)
    for i in range(5):
        winlog.append(start_game(board_template, output=True))

    mouse_win = 0
    trapper_win = 0
    for i in winlog:
        if i == 'Win':
            mouse_win += 1
        else:
            trapper_win += 1
    print(f"M: {mouse_win}, T: {trapper_win}")
