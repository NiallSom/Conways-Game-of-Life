import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
CELL_SIZE = 10

cols, rows = (WIDTH // CELL_SIZE), (HEIGHT // CELL_SIZE)


class CONTROLLER:
    def __init__(self):
        self.map = []

    def createMap(self):
        for x in range(0, WIDTH, CELL_SIZE):
            self.map.append([])
        self.genMapCells()

    def genMapCells(self):
        for x in range(0, cols):
            for y in range(0, rows):
                self.map[x].append(0)

    def getNeighbours(self, x, y):
        # Daniel Shiffmans algorithm
        sum = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                col = (x + i + cols) % cols
                row = (y + j + rows) % rows
                sum += self.map[col][row]
        sum -= self.map[x][y]
        return sum

    def showAll(self):
        for x in range(0, cols):
            for y in range(0, rows):
                if self.map[x][y] == 1:
                    pygame.draw.rect(screen, (0, 0, 0), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def nextGeneration(self):
        # generate next generation
        nextGenMap = [[0 for _ in range(rows)] for _ in range(cols)]
        for x in range(0, cols):
            for y in range(0, rows):
                # get the initial state of cell
                state = self.map[x][y]
                # return the amount of neighbours cell(x,y) has
                neighbours = self.getNeighbours(x, y)

                # game of life conditions
                if state == 0 and neighbours == 3:
                    nextGenMap[x][y] = 1
                elif state == 1 and (neighbours < 2 or neighbours > 3):
                    nextGenMap[x][y] = 0
                else:
                    nextGenMap[x][y] = state
        # set the next generation to the map so it can be displayed
        self.map = nextGenMap

    def selectCell(self, mousePosition):
        x = mousePosition[0] // CELL_SIZE
        y = mousePosition[1] // CELL_SIZE
        self.map[x][y] = not self.map[x][y]


controller = CONTROLLER()
controller.createMap()

while 1:
    screen.fill((255, 255, 255))
    clock.tick(60)
    controller.showAll()
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                controller.nextGeneration()
        if event.type == pygame.MOUSEBUTTONDOWN:
            controller.selectCell(pygame.mouse.get_pos())
