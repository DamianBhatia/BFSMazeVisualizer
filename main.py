import pygame as pg
import sys
from pygame.locals import *
from typing import List, Tuple
import math
import random

# Create the maze
maze = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]



pg.init()
screen = pg.display.set_mode((700, 700))
dim = screen.get_width()
cyan = [(0, 255, 255), (0, 204, 204), (0, 153, 153), (0, 102, 102)]


def render():
    # Draw background
    for i in range(len(maze)):
        for j in range(len(maze)):
            if maze[i][j] == ' ':
                pg.draw.rect(screen, (224, 224, 224),
                             Rect(j * dim / len(maze), i * dim / len(maze), dim / len(maze), dim / len(maze)))
            if maze[i][j] == '*':
                pg.draw.rect(screen, (0, 0, 0),
                             Rect(j * dim / len(maze), i * dim / len(maze), dim / len(maze), dim / len(maze)))
            if maze[i][j] == 'E':
                pg.draw.rect(screen, (255, 102, 102),
                             Rect(j * dim / len(maze), i * dim / len(maze), dim / len(maze), dim / len(maze)))
            if maze[i][j] == 'S':
                pg.draw.rect(screen, (51, 51, 255),
                             Rect(j * dim / len(maze), i * dim / len(maze), dim / len(maze), dim / len(maze)))

    # Draw in Grid Lines
    for i in range(len(maze) + 1):
        pg.draw.line(screen, (169, 169, 169), (i * dim / len(maze), 0), (i * dim / len(maze), dim), 3)
        pg.draw.line(screen, (169, 169, 169), (0, i * dim / len(maze)), (dim, i * dim / len(maze)), 3)


def print_maze(maze: List[List[chr]]):
    for i in range(len(maze)):
        for j in range(len(maze)):
            print(maze[i][j], end=' ')
        print()


def valid(maze: List[List[chr]], x: int, y: int) -> bool:
    if 0 <= x < len(maze) and 0 <= y < len(maze):
        if maze[y][x] != '*':
            return True
    return False


def get_curr_pos(maze: List[List[chr]], x: int, y: int, path: str) -> List[int]:
    for move in path:
        if move == 'L':
            x -= 1
        elif move == 'R':
            x += 1
        elif move == 'U':
            y -= 1
        else:
            y += 1

    return [x, y]


def check_visit(x: int, y: int, visited: List[List[int]]) -> bool:
    for pos in visited:
        if pos[0] == x and pos[1] == y:
            return False
    return True


def solve(maze: List[List[chr]], start: Tuple[int], end: Tuple[int]) -> str:
    copy = maze.copy()

    queue = []
    visited = []
    x, y = start[1], start[0]

    visited.append([x, y])

    if valid(copy, x - 1, y):
        queue.append('L')
        pg.draw.rect(screen, cyan[random.randint(0,3)],
                     Rect((x-1) * dim / len(maze), y * dim / len(maze), dim / len(maze),
                          dim / len(maze)))
        pg.display.update()
    if valid(copy, x + 1, y):
        queue.append('R')
        pg.draw.rect(screen, cyan[random.randint(0,3)],
                     Rect((x+1) * dim / len(maze), y * dim / len(maze), dim / len(maze),
                          dim / len(maze)))
    if valid(copy, x, y - 1):
        queue.append('U')
        pg.draw.rect(screen, cyan[random.randint(0,3)],
                     Rect(x * dim / len(maze), (y-1) * dim / len(maze), dim / len(maze),
                          dim / len(maze)))
    if valid(copy, x, y + 1):
        queue.append('D')
        pg.draw.rect(screen, cyan[random.randint(0,3)],
                     Rect(x * dim / len(maze), (y+1) * dim / len(maze), dim / len(maze),
                          dim / len(maze)))

    while queue:
        curr_path = queue.pop(0)
        curr_pos = get_curr_pos(copy, x, y, curr_path)

        visited.append(curr_pos)

        if curr_pos[0] == end[1] and curr_pos[1] == end[0]:
            render()
            return curr_path

        for node in visited:
            if screen.get_at((node[0] * dim // len(maze) + 4, node[1] * dim // len(maze) + 4)) == (224, 224, 224):
                pg.draw.rect(screen, cyan[random.randint(0, 3)],
                             Rect(node[0] * dim / len(maze), node[1] * dim / len(maze), dim / len(maze),
                                  dim / len(maze)))

        if valid(copy, curr_pos[0] - 1, curr_pos[1]) and check_visit(curr_pos[0] - 1, curr_pos[1], visited):
            new_path = curr_path + 'L'
            queue.append(new_path)
        if valid(copy, curr_pos[0] + 1, curr_pos[1]) and check_visit(curr_pos[0] + 1, curr_pos[1], visited):
            new_path = curr_path + 'R'
            queue.append(new_path)
        if valid(copy, curr_pos[0], curr_pos[1] - 1) and check_visit(curr_pos[0], curr_pos[1] - 1, visited):
            new_path = curr_path + 'U'
            queue.append(new_path)
        if valid(copy, curr_pos[0], curr_pos[1] + 1) and check_visit(curr_pos[0], curr_pos[1] + 1, visited):
            new_path = curr_path + 'D'
            queue.append(new_path)
        pg.display.update()

    return 'in-existent'


def draw_path(maze: List[List[chr]], path: str, start: Tuple[int]) -> None:
    maze[start[0]][start[1]] = 'X'
    pg.draw.rect(screen, (0, 204, 0),
                 Rect(start[1] * dim / len(maze), start[0] * dim / len(maze), dim / len(maze), dim / len(maze)))
    sub_path = ''
    for move in path:
        sub_path = sub_path + move
        curr_pos = get_curr_pos(maze, start[1], start[0], sub_path)
        maze[curr_pos[1]][curr_pos[0]] = 'X'
        pg.draw.rect(screen, (0, 204, 0),
                     Rect(curr_pos[0] * dim / len(maze), curr_pos[1] * dim / len(maze), dim / len(maze),
                          dim / len(maze)))
        pg.display.update()
        pg.time.delay(80)

    # Draw in Grid Lines
    for i in range(len(maze) + 1):
        pg.draw.line(screen, (169, 169, 169), (i * dim / len(maze), 0), (i * dim / len(maze), dim), 3)
        pg.draw.line(screen, (169, 169, 169), (0, i * dim / len(maze)), (dim, i * dim / len(maze)), 3)


def search(maze: List[List[chr]], key: chr):
    for i in range(len(maze)):
        for j in range(len(maze)):
            if maze[i][j] == key:
                return i, j
    return None


# Draw original screen
render()

# Active loop
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                draw_path(maze, solve(maze, search(maze, 'S'), search(maze, 'E')), search(maze, 'S'))
            if event.key == pg.K_s:
                pos = pg.mouse.get_pos()
                y = math.ceil((dim / len(maze) / (dim / pos[1])) / 3) - 1
                x = math.ceil((dim / len(maze) / (dim / pos[0])) / 3) - 1
                maze[y][x] = 'S'
                render()
            if event.key == pg.K_e:
                pos = pg.mouse.get_pos()
                y = math.ceil((dim / len(maze) / (dim / pos[1])) / 3) - 1
                x = math.ceil((dim / len(maze) / (dim / pos[0])) / 3) - 1
                maze[y][x] = 'E'
                render()
        if pg.mouse.get_pressed()[0]:
            pos = pg.mouse.get_pos()
            y = math.ceil((dim / len(maze) / (dim / pos[1])) / 3) - 1
            x = math.ceil((dim / len(maze) / (dim / pos[0])) / 3) - 1
            maze[y][x] = '*'
            render()
        if pg.mouse.get_pressed()[2]:
            pos = pg.mouse.get_pos()
            y = math.ceil((dim / len(maze) / (dim / pos[1])) / 3) - 1
            x = math.ceil((dim / len(maze) / (dim / pos[0])) / 3) - 1
            maze[y][x] = ' '
            render()

    pg.display.update()
