import pygame
import random

# 初期化
pygame.init()

# 画面設定
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tetris")

# 色の定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# テトリミノの形状
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

# テトリミノの色
COLORS = [CYAN, YELLOW, MAGENTA, RED, GREEN, BLUE, ORANGE]

# ゲーム設定
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20

# グリッドの初期化
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# 現在のテトリミノ
current_piece = None
current_x = 0
current_y = 0
current_color = None

# 次のテトリミノ
next_piece = random.choice(SHAPES)
next_color = random.choice(COLORS)

# スコア
score = 0
font = pygame.font.Font(None, 36)

def new_piece():
    global current_piece, current_x, current_y, current_color, next_piece, next_color
    current_piece = next_piece
    current_color = next_color
    current_x = GRID_WIDTH // 2 - len(current_piece[0]) // 2
    current_y = 0
    next_piece = random.choice(SHAPES)
    next_color = random.choice(COLORS)

def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x]:
                pygame.draw.rect(screen, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_current_piece():
    for y, row in enumerate(current_piece):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, current_color, ((current_x + x) * BLOCK_SIZE, (current_y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, WHITE, ((current_x + x) * BLOCK_SIZE, (current_y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_next_piece():
    for y, row in enumerate(next_piece):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, next_color, (GRID_WIDTH * BLOCK_SIZE + 50 + x * BLOCK_SIZE, 50 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, WHITE, (GRID_WIDTH * BLOCK_SIZE + 50 + x * BLOCK_SIZE, 50 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def check_collision(piece, x, y):
    for y_offset, row in enumerate(piece):
        for x_offset, cell in enumerate(row):
            if cell:
                if (x + x_offset < 0 or x + x_offset >= GRID_WIDTH or
                    y + y_offset >= GRID_HEIGHT or
                    grid[y + y_offset][x + x_offset]):
                    return True
    return False

def rotate_piece(piece):
    return [list(row) for row in zip(*piece[::-1])]

def clear_lines():
    global grid, score
    lines_cleared = 0
    for y in range(GRID_HEIGHT - 1, -1, -1):
        if all(grid[y]):
            del grid[y]
            grid.insert(0, [0 for _ in range(GRID_WIDTH)])
            lines_cleared += 1
    score += lines_cleared ** 2 * 100

def game_over():
    text = font.render("GAME OVER", True, WHITE)
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

def main():
    global current_piece, current_x, current_y, score

    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5
    new_piece()

    running = True
    while running:
        fall_time += clock.get_rawtime()
        clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not check_collision(current_piece, current_x - 1, current_y):
                    current_x -= 1
                if event.key == pygame.K_RIGHT and not check_collision(current_piece, current_x + 1, current_y):
                    current_x += 1
                if event.key == pygame.K_DOWN and not check_collision(current_piece, current_x, current_y + 1):
                    current_y += 1
                if event.key == pygame.K_UP:
                    rotated = rotate_piece(current_piece)
                    if not check_collision(rotated, current_x, current_y):
                        current_piece = rotated

        if fall_time / 1000 > fall_speed:
            if not check_collision(current_piece, current_x, current_y + 1):
                current_y += 1
            else:
                for y, row in enumerate(current_piece):
                    for x, cell in enumerate(row):
                        if cell:
                            grid[current_y + y][current_x + x] = current_color
                clear_lines()
                new_piece()
                if check_collision(current_piece, current_x, current_y):
                    game_over()
                    running = False
            fall_time = 0

        screen.fill(BLACK)
        draw_grid()
        draw_current_piece()
        draw_next_piece()

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (GRID_WIDTH * BLOCK_SIZE + 50, 150))

        pygame.draw.rect(screen, WHITE, (0, 0, GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE), 2)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
