from random import randint as rand
import pygame, sys

CELL_SIZE, CELL_NUMBER = 10, 50


class Object:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen


class Grid(Object):
    def __init__(self, x, y, screen, occupied):
        Object.__init__(self, x, y, screen)
        self.occupied = occupied
        self.neighbors = 0
        self.font1 = pygame.font.Font(None, 24)

    def draw(self):
        obj = pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, (0, 0, 0), obj)
        if self.occupied:
            obj = pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1)
            pygame.draw.rect(self.screen, (255, 255, 255), obj)
        else:
            obj = pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1)
            pygame.draw.rect(self.screen, (0, 0, 255), obj)

        #text1 = self.font1.render(str(self.neighbors), True, (180, 0, 0))
        #self.screen.blit(text1, (self.x * CELL_SIZE + 5, self.y * CELL_SIZE + 5))


class MainController:
    def __init__(self, screen):
        self.screen = screen
        self.current_state_grid = []
        self.spawn_grid()
        self.new_state_grid = self.current_state_grid
        self.cages = []
        for y in range(CELL_NUMBER):
            for x in range(CELL_NUMBER):
                self.spawn_cell(x, y, rand(0, 5) == 5)

    def update(self, event):
        self.count_neighbors_all()
        #if event == pygame.MOUSEBUTTONDOWN:
        self.logic()
        self.draw()

    def draw(self):
        for row in self.current_state_grid:
            for block in row:
                block.draw()

    def spawn_cell(self, x, y, state):
        self.new_state_grid[y][x].occupied = state

    def count_neighbors(self, cx, cy):
        count = 0
        for y in range(cy-1, cy+2):
            for x in range(cx-1, cx+2):
                if self.current_state_grid[y][x].occupied:
                    count += 1
        if self.current_state_grid[cy][cx].occupied:
            count -= 1
        return count

    def spawn_grid(self):
        for _ in range(CELL_NUMBER):
            self.current_state_grid.append([])
        for y in range(CELL_NUMBER):
            for x in range(CELL_NUMBER):
                self.current_state_grid[y].append(Grid(x, y, self.screen, False))

    def count_neighbors_all(self):
        for row in self.current_state_grid:
            for cell in row:
                try:
                    cell.neighbors = self.count_neighbors(cell.x, cell.y)
                except IndexError:
                    cell.neighbors = 0

    def logic(self):
        for row in self.current_state_grid:
            for cell in row:
                if cell.occupied:
                    self.new_state_grid[cell.y][cell.x].occupied = cell.neighbors in (2, 3)
                else:
                    self.new_state_grid[cell.y][cell.x].occupied = cell.neighbors == 3
        self.current_state_grid = self.new_state_grid


def main():
    name_project = 'LIFE'
    pygame.font.init()
    screen = pygame.display.set_mode((CELL_NUMBER * CELL_SIZE, CELL_NUMBER * CELL_SIZE))
    pygame.display.set_caption(name_project)
    main_controller = MainController(screen)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((255, 255, 255))
        main_controller.update(event.type)
        pygame.display.update()
        clock.tick(5)


if __name__ == '__main__':
    main()
