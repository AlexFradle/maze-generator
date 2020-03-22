import pygame
from maze_creator import MazeCreator
from a_star import AStar
from random import randrange
pygame.init()


class Wall(pygame.Rect):
    def __init__(self, x: int, y: int, used: int, orientation: int):
        # 1 = vertical, 2 = horizontal
        w = 1 if orientation == 1 else 10
        h = 10 if orientation == 1 else 1
        super().__init__(x, y, w, h)
        self.open_ = bool(used)


class Cell(pygame.Rect):
    def __init__(self, x: int, y: int, open_: int, w: int=9, h: int=9):
        super().__init__(x, y, w, h)
        self.open_ = open_


class Door(pygame.Rect):
    def __init__(self, x: int, y: int, used: int, orientation: int):
        # 1 = vertical, 2 = horizontal
        w = 1 if orientation == 1 else 10
        h = 10 if orientation == 1 else 1
        super().__init__(x, y, w, h)
        self.open_ = bool(used)


class Board(pygame.Surface):
    def __init__(self, width, height):
        super().__init__((width, height), pygame.SRCALPHA)
        self.__width = width
        self.__height = height
        self.__grid = self.load_maze("maze.txt")
        cell_num_y = ["X" for _ in self.__grid].count("X")
        cell_num_x = self.__grid[1].count("X")
        # All cell positions
        self.cell_pos = [[Cell(9 * j + (1 * (j + 1)), 9 * i + (1 * (i + 1)), 1) for j in range(cell_num_x)]
                         for i in range(cell_num_y)]
        # All horizontal walls
        self.hori_wall_pos = [[Wall(10 * j + 1, 10 * i, 1, 2) for j in range(cell_num_x)] for i in range(cell_num_y)]
        # All vertical walls
        self.vert_wall_pos = [[Wall(10 * j, 10 * i + 1, 1, 1) for j in range(cell_num_x)] for i in range(cell_num_y)]
        # All horizontal doors
        self.hori_door_pos = [
            [Door(10 * (j // 2), 10 * (i // 2), 0 if self.__grid[i][j + 1] == "-" else 1, 2)
             for j in range(0, len(self.__grid[0]) - 1, 2)] for i in range(0, len(self.__grid), 2)]
        # All vertical doors
        self.vert_door_pos = [
            [Door(10 * (j // 2), 10 * (i // 2), 0 if self.__grid[i][j - 1] == "|" else 1, 1)
             for j in range(1, len(self.__grid[0]) + 1, 2)] for i in range(1, len(self.__grid), 2)]
        self.maze = AStar(0, 0)
        path = self.maze.solve()
        self.cell_colours = [[
            (255, 255, 255) if self.maze.grid[i][j] not in path else (0, 255, 0)
            for j in range(1, len(self.maze.grid[0]), 2)] for i in range(1, len(self.maze.grid), 2)
        ]

    @property
    def grid(self):
        return self.__grid

    @grid.setter
    def grid(self, item):
        self.__grid = item

    @staticmethod
    def load_maze(fn: str) -> list:
        with open(fn) as f:
            return [i.replace("\n", "") for i in f.readlines()]

    def update(self) -> None:
        """
        Update the board
        :return: None
        """
        self.fill((0, 0, 0))
        for hor in self.hori_wall_pos:
            for h in hor:
                pygame.draw.rect(self, (0, 0, 0), h)
        for vert in self.vert_wall_pos:
            for v in vert:
                pygame.draw.rect(self, (0, 0, 0), v)
        for door in self.hori_door_pos:
            for d in door:
                pygame.draw.rect(self, (255, 255, 255) if d.open_ else (0, 0, 0), d)
        for door in self.vert_door_pos:
            for d in door:
                pygame.draw.rect(self, (255, 255, 255) if d.open_ else (0, 0, 0), d)
        for row, cols in zip(self.cell_pos, self.cell_colours):
            for cell, col in zip(row, cols):
                pygame.draw.rect(self, col, cell)


width, height = 1920, 1080
display = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
clock = pygame.time.Clock()
board = Board(width, height)

font = pygame.font.SysFont("Courier", 15, True)
running = True
pos = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Quits game
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RETURN:
                m = MazeCreator(50, 50)
                # m = Maze(randrange(20, 150, 2), randrange(20, 150, 2))
                m.create((0, 0))
                board = Board(width, height)

    display.fill((0, 0, 0))

    board.update()
    display.blit(board, (0, 0))

    pygame.display.update()
    clock.tick(200)

pygame.image.save(display, "maze_1_solved.png")
pygame.quit()



