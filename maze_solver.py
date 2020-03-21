import math
from random import randint
import pygame
pygame.init()


class Vertex:
    def __init__(self, x, y, wall):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbours = []
        self.previous = None
        # self.wall = True if randint(1, 100) < 20 else False
        self.wall = wall

    def add_neighbours(self, grid):
        self.neighbours.append(grid[self.y + 1][self.x]) if self.y < len(grid) - 1 else 0
        self.neighbours.append(grid[self.y - 1][self.x]) if self.y > 0 else 0
        self.neighbours.append(grid[self.y][self.x + 1]) if self.x < len(grid[0]) - 1 else 0
        self.neighbours.append(grid[self.y][self.x - 1]) if self.x > 0 else 0


class MazeSolver:
    def __init__(self, cols=5, rows=5, from_file=True):
        self.cols = cols
        self.rows = rows
        self.open_set = []
        self.closed_set = []
        if from_file:
            self.grid = self.load_from_file()
        else:
            self.grid = [[Vertex(j, i, True if randint(1, 100) < 20 else False) for j in range(cols)] for i in range(rows)]

    @staticmethod
    def heuristic(a, b):
        return abs(a.x - b.x) + abs(a.y - b.y)

    def load_from_file(self, fn="solved_maze.txt"):
        with open(fn) as f:
            maze = [i.replace("\n", "") for i in f.readlines()]
        self.cols = len(maze[0])
        self.rows = len(maze)
        grid = [[Vertex(j, i, True if maze[i][j] in ["/", "-", "|"] else False) for j in range(len(maze[0]))] for i in range(len(maze))]
        return grid

    def solve(self):
        for row in self.grid:
            for v in row:
                v.add_neighbours(self.grid)

        start = self.grid[1][1]
        end = self.grid[self.rows - 2][self.cols - 2]

        self.open_set.append(start)

        while self.open_set:
            smallest = 0
            for i in range(len(self.open_set)):
                if self.open_set[i].f < self.open_set[smallest].f:
                    smallest = i

            path = []
            current = self.open_set[smallest]
            temp = current
            path.append(temp)
            while temp.previous:
                path.append(temp.previous)
                temp = temp.previous

            if current == end:
                print(current.x, current.y)
                return path

            self.open_set.remove(current)
            self.closed_set.append(current)

            neighbours = current.neighbours
            for i in neighbours:
                neighbour = i
                if neighbour not in self.closed_set and not neighbour.wall:
                    temp_g = current.g + 1
                    if neighbour in self.open_set:
                        if temp_g < neighbour.g:
                            neighbour.g = temp_g
                    else:
                        neighbour.g = temp_g
                        self.open_set.append(neighbour)

                    neighbour.h = self.heuristic(neighbour, end)
                    neighbour.f = neighbour.g + neighbour.h
                    neighbour.previous = current


if __name__ == '__main__':
    m = MazeSolver(25, 25)
    solved = m.solve()
    solved = [(i.x, i.y) for i in solved]
    a = "\n".join([" ".join(["O" if (j, i) in solved else ("#" if m.grid[i][j].wall else " ") for j in range(m.cols)]) for i in range(m.rows)])
    print(a)
    # width, height = 1024, 720
    # display = pygame.display.set_mode((width, height), pygame.SRCALPHA)
    # clock = pygame.time.Clock()
    #
    # font = pygame.font.SysFont("Courier", 15, True)
    # running = True
    #
    # solv = MazeSolver(10, 10)
    # path = solv.solve()
    # rects = [
    #     [
    #         (pygame.Rect(50 * j, 50 * i, 50, 50), (0, 255, 0) if (j, i) in path else ((0, 0, 0) if solv.grid[j][i].wall else (255, 255, 255)))
    #         for j in range(solv.cols - 1)
    #     ]
    #     for i in range(solv.rows - 1)
    # ]
    #
    # while running:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    #
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_ESCAPE:
    #                 running = False
    #
    #     display.fill((20, 20, 20))
    #
    #     for rect in rects:
    #         for r in rect:
    #             pygame.draw.rect(display, r[1], r[0])
    #
    #     pygame.display.update()
    #     clock.tick(60)
    #
    # pygame.quit()
