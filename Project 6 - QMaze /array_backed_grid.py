import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (235, 82, 52)
YELLOW = (252, 186, 3)

WIDTH = 30
HEIGHT = 30

MARGIN = 3


def display(grids):
    grid_width = len(grids[0][0])
    grid_height = len(grids[0])

    pygame.init()

    WINDOW_SIZE = [(WIDTH + MARGIN) * grid_width, (HEIGHT + MARGIN) * grid_height]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    pygame.display.set_caption("Qleaning Pathfinder")

    done = False

    clock = pygame.time.Clock()

    for grid in grids:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

        screen.fill(BLACK)

        for row in range(grid_height):
            for column in range(grid_width):
                color = WHITE
                if grid[row][column] == 1:
                    color = GREEN
                elif grid[row][column] == 3:
                    color = RED
                elif grid[row][column] == 2:
                    color = YELLOW
                pygame.draw.rect(
                    screen,
                    color,
                    [
                        (MARGIN + WIDTH) * column + MARGIN,
                        (MARGIN + HEIGHT) * row + MARGIN,
                        WIDTH,
                        HEIGHT,
                    ],
                )

        clock.tick(16)
        pygame.display.flip()
    pygame.quit()
