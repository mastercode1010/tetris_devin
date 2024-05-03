import pygame
import random

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),
    (255, 255, 0),
    (128, 0, 128),
    (0, 255, 0),
    (255, 0, 0),
    (0, 0, 255),
    (255, 127, 0)
]

# Define game settings
BLOCK_SIZE = 30
ROWS = 20
COLS = 10
WIDTH = COLS * BLOCK_SIZE
HEIGHT = ROWS * BLOCK_SIZE

# Define tetromino shapes
SHAPES = [
    [[1, 1, 1],
     [0, 1, 0]],
    
    [[0, 2, 2],
     [2, 2, 0]],
    
    [[3, 3, 0],
     [0, 3, 3]],
    
    [[4, 0, 0],
     [4, 4, 4]],
    
    [[0, 0, 5],
     [5, 5, 5]],
    
    [[6, 6, 6, 6]],
    
    [[7, 7],
     [7, 7]]
]

class Tetromino:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = COLORS[shape]
        self.rotation = 0

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

def create_grid():
    grid = [[BLACK] * COLS for _ in range(ROWS)]
    return grid

def draw_grid(screen, grid):
    for y in range(ROWS):
        for x in range(COLS):
            pygame.draw.rect(screen, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    
    for y in range(ROWS):
        pygame.draw.line(screen, GRAY, (0, y * BLOCK_SIZE), (WIDTH, y * BLOCK_SIZE))
        for x in range(COLS):
            pygame.draw.line(screen, GRAY, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, HEIGHT))

def draw_tetromino(screen, tetromino):
    shape_matrix = tetromino.shape[tetromino.rotation % len(tetromino.shape)]
    for y, row in enumerate(shape_matrix):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, tetromino.color, (tetromino.x * BLOCK_SIZE + x * BLOCK_SIZE,
                                                           tetromino.y * BLOCK_SIZE + y * BLOCK_SIZE,
                                                           BLOCK_SIZE, BLOCK_SIZE), 0)

def check_collision(grid, tetromino):
    shape_matrix = tetromino.shape[tetromino.rotation % len(tetromino.shape)]
    for y, row in enumerate(shape_matrix):
        for x, cell in enumerate(row):
            try:
                if cell and grid[tetromino.y + y][tetromino.x + x] != BLACK:
                    return True
            except IndexError:
                return True
    return False

def merge_tetromino(grid, tetromino):
    shape_matrix = tetromino.shape[tetromino.rotation % len(tetromino.shape)]
    for y, row in enumerate(shape_matrix):
        for x, cell in enumerate(row):
            if cell:
                grid[tetromino.y + y][tetromino.x + x] = tetromino.color

def remove_completed_lines(grid):
    completed_lines = 0
    for y in range(ROWS - 1, -1, -1):
        if BLACK not in grid[y]:
            completed_lines += 1
            del grid[y]
            grid.insert(0, [BLACK] * COLS)
    return completed_lines

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    
    grid = create_grid()
    current_tetromino = Tetromino(COLS // 2, 0, random.choice(SHAPES))
    next_tetromino = Tetromino(COLS // 2, 0, random.choice(SHAPES))
    fall_speed = 0.5
    fall_time = 0
    score = 0
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_tetromino.move(-1, 0)
                    if check_collision(grid, current_tetromino):
                        current_tetromino.move(1, 0)
                elif event.key == pygame.K_RIGHT:
                    current_tetromino.move(1, 0)
                    if check_collision(grid, current_tetromino):
                        current_tetromino.move(-1, 0)
                elif event.key == pygame.K_DOWN:
                    current_tetromino.move(0, 1)
                    if check_collision(grid, current_tetromino):
                        current_tetromino.move(0, -1)
                        merge_tetromino(grid, current_tetromino)
                        completed_lines = remove_completed_lines(grid)
                        score += completed_lines * 10
                        current_tetromino = next_tetromino
                        next_tetromino = Tetromino(COLS // 2, 0, random.choice(SHAPES))
                elif event.key == pygame.K_UP:
                    current_tetromino.rotate()
                    if check_collision(grid, current_tetromino):
                        current_tetromino.rotate()
                        current_tetromino.rotate()
                        current_tetromino.rotate()
        
        fall_time += clock.get_rawtime()
        clock.tick()
        
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_tetromino.move(0, 1)
            if check_collision(grid, current_tetromino):
                current_tetromino.move(0, -1)
                merge_tetromino(grid, current_tetromino)
                completed_lines = remove_completed_lines(grid)
                score += completed_lines * 10
                current_tetromino = next_tetromino
                next_tetromino = Tetromino(COLS // 2, 0, random.choice(SHAPES))
        
        screen.fill(BLACK)
        draw_grid(screen, grid)
        draw_tetromino(screen, current_tetromino)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
