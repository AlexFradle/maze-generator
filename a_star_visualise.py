import pygame
from a_star import AStar
from random import randint
pygame.init()


class Space(pygame.Rect):
    def __init__(self, x, y, w, h, wall):
        super().__init__(x, y, w, h)
        self.wall = wall
        self.path = False


width, height = 1024, 720
display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

font = pygame.font.SysFont("Courier", 15, True)
running = True

grid_w, grid_h = 51, 35
grid = [[Space(20 * j, 20 * i, 20, 20, True if randint(1, 100) < 30 else False) for j in range(grid_w)] for i in range(grid_h)]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Quits game
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RETURN:
                file = "\n".join(["".join([" " if not s.wall else "#" for s in row]) for row in grid])
                with open("maze.txt", "w") as f:
                    f.write(file)
                a = AStar(grid_w, grid_h, True, False)
                path = a.solve()
                if path is not None:
                    for p in path:
                        grid[p.y][p.x].path = True
                else:
                    print("NOT SOLVEABLE")
            elif event.key == pygame.K_r:
                grid = [[Space(20 * j, 20 * i, 20, 20, True if randint(1, 100) < 20 else False) for j in range(grid_w)]
                        for i in range(grid_h)]
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            for row in grid:
                for space in row:
                    if space.collidepoint(mx, my):
                        space.wall = not space.wall

    display.fill((0, 0, 0))

    for row in grid:
        for space in row:
            col = (0, 255, 0) if space.path else ((255, 255, 255) if not space.wall else (255, 0, 0))
            pygame.draw.rect(display, col, space)

    pygame.display.update()
    clock.tick(200)

pygame.quit()


