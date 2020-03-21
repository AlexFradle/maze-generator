import random
from collections import ChainMap


class Maze:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.grid = [
            [("-" if (j + 1) % 2 == 0 else "/") if i % 2 == 0 else ("O" if (j + 1) % 2 == 0 else "|")
             for j in range(self.width + 1)] for i in range(self.height + 1)
        ]

    def get_adjacent_walls(self, cell: tuple) -> list:
        """
        Gets walls adjacent to cell
        :param cell: (x, y) coord for cell to check
        :return: Coords of all adjacent walls
        """
        return [i for i in [
            (cell[0] + 1, cell[1]), (cell[0] - 1, cell[1]), (cell[0], cell[1] + 1), (cell[0], cell[1] - 1)
        ] if (0 < i[0] < len(self.grid[0]) - 1 and 0 < i[1] < len(self.grid) - 1) and self.grid[i[1]][i[0]] != " "]

    def create(self, start_pos: tuple) -> None:
        """
        Creates maze using Randomized Prim's algorithm
        Example using 10x10:
        /-/-/-/-/-/
        |X X X X|X|
        / / /-/ / /
        |X|X X|X X|
        /-/ / /-/-/
        |X X|X X X|
        /-/ /-/-/-/
        |X X X X X|
        /-/ /-/-/ /
        |X X X|X X|
        /-/-/-/-/-/

        / = unused vertex, - = horizontal wall, | = vertical wall, ' ' = door
        :param start_pos: (x, y) of start position
        :return: None
        """
        # Cell positions, e.g (acc_x, acc_y): (puz_x, puz_y)
        cell_pos = dict(ChainMap(*[
            {c: d for c, d in zip(a, b)}
            for a, b in zip([[(p, c) for c in range(len(r))] for p, r in enumerate([check for check in [[cell for cell in row if cell == "O"] for row in self.grid] if check])],
                            [[(y, x) for x, z in enumerate(i) if z == "O"] for y, i in enumerate(self.grid) if "O" in i])
        ]))
        # In form (x, y), therefore must be used as grid[wall[1]][wall[0]]
        puz_cur_pos = cell_pos[start_pos]
        self.grid[puz_cur_pos[1]][puz_cur_pos[0]] = "X"
        walls = [*self.get_adjacent_walls(puz_cur_pos)]
        while walls:
            wall = random.choice(walls)
            # Vertical wall separating horizontal cells, checks if one isnt visited using xor
            if (self.grid[wall[1]][wall[0] - 1] == "O") ^ (self.grid[wall[1]][wall[0] + 1] == "O"):
                if self.grid[wall[1]][wall[0] - 1] == "O":
                    cell = (wall[0] - 1, wall[1])
                    self.grid[wall[1]][wall[0] - 1] = "X"

                elif self.grid[wall[1]][wall[0] + 1] == "O":
                    cell = (wall[0] + 1, wall[1])
                    self.grid[wall[1]][wall[0] + 1] = "X"
                self.grid[wall[1]][wall[0]] = " "
                walls.extend(self.get_adjacent_walls(cell))

            # Horizontal wall separating vertical cells, checks if one isnt visited using xor
            if (self.grid[wall[1] - 1][wall[0]] == "O") ^ (self.grid[wall[1] + 1][wall[0]] == "O"):
                if self.grid[wall[1] - 1][wall[0]] == "O":
                    cell = (wall[0], wall[1] - 1)
                    self.grid[wall[1] - 1][wall[0]] = "X"

                elif self.grid[wall[1] + 1][wall[0]] == "O":
                    cell = (wall[0], wall[1] + 1)
                    self.grid[wall[1] + 1][wall[0]] = "X"

                self.grid[wall[1]][wall[0]] = " "
                walls.extend(self.get_adjacent_walls(cell))
            walls.remove(wall)

        with open("solved_maze.txt", "w") as f:
            f.write("\n".join("".join(i) for i in self.grid))


if __name__ == '__main__':
    m = Maze(100, 100)
    # m = Maze(382, 220)
    m.create((0, 0))
