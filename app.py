import pygame
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
BLOCK_SIZE = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('TETRIS')

tetriminos = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3],
     [3, 3]],

    [[0, 4, 0],
     [4, 4, 4]],

    [[5, 0],
     [5, 0],
     [5, 5]],

    [[6, 0],
     [6, 0],
     [6, 0],
     [6, 0]],

    [[7, 7, 0],
     [0, 7, 7]]
]

def draw_block(x, y, color):
    pygame.draw.rect(screen, color, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, BLACK, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_board(board):
    for y, row in enumerate(board):
        for x, block in enumerate(row):
            if block:
                draw_block(x, y, colors[block])

def new_piece():
    return random.choice(tetriminos)

def valid_position(board, piece, offset):
    for y, row in enumerate(piece):
        for x, block in enumerate(row):
            if block:
                board_y = y + offset[1]
                board_x = x + offset[0]
                if not (0 <= board_x < 10 and 0 <= board_y < 20) or board[board_y][board_x]:
                    return False
    return True

def merge_board(board, piece, offset):
    for y, row in enumerate(piece):
        for x, block in enumerate(row):
            if block:
                board[y + offset[1]][x + offset[0]] = piece[y][x]
    return board

def remove_full_rows(board):
    full_rows = [i for i, row in enumerate(board) if all(row)]
    for row in full_rows:
        del board[row]
        board.insert(0, [0 for _ in range(10)])
    return len(full_rows)

def game_over():
    font = pygame.font.SysFont(None, 48)
    text = font.render("Game Over", True, WHITE)
    screen.blit(text, (80, SCREEN_HEIGHT // 2 - 24))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    quit()

# Initialize game variables
board = [[0 for _ in range(10)] for _ in range(20)]
current_piece = new_piece()
current_x, current_y = 3, 0
colors = {
    1: (255, 0, 0),   # Red
    2: (0, 255, 0),   # Green
    3: (0, 0, 255),   # Blue
    4: (255, 255, 0), # Yellow
    5: (255, 0, 255), # Purple
    6: (0, 255, 255), # Cyan
    7: (255, 165, 0)  # Orange
}
clock = pygame.time.Clock()
fall_time = 0
fall_speed = 0.5
score = 0

running = True
while running:
    screen.fill(BLACK)
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if valid_position(board, current_piece, (current_x - 1, current_y)):
                    current_x -= 1
            elif event.key == pygame.K_RIGHT:
                if valid_position(board, current_piece, (current_x + 1, current_y)):
                    current_x += 1
            elif event.key == pygame.K_DOWN:
                if valid_position(board, current_piece, (current_x, current_y + 1)):
                    current_y += 1
            elif event.key == pygame.K_UP:
                rotated_piece = [list(row) for row in zip(*current_piece[::-1])]
                if valid_position(board, rotated_piece, (current_x, current_y)):
                    current_piece = rotated_piece

    fall_time += clock.get_rawtime()
    clock.tick()

    if fall_time / 1000 >= fall_speed:
        if valid_position(board, current_piece, (current_x, current_y + 1)):
            current_y += 1
        else:
            board = merge_board(board, current_piece, (current_x, current_y))
            score += remove_full_rows(board)
            current_piece = new_piece()
            current_x, current_y = 3, 0
            if not valid_position(board, current_piece, (current_x, current_y)):
                game_over()

        fall_time = 0

    draw_board(board)
    for y, row in enumerate(current_piece):
        for x, block in enumerate(row):
            if block:
                draw_block(x + current_x, y + current_y, colors[block])

    pygame.display.flip()

pygame.quit()
