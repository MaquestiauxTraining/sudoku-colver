import pygame
import sys

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 540, 600  # Window size (extra space for button)
GRID_SIZE = 9  # 9x9 grid
CELL_SIZE = WIDTH // GRID_SIZE  # Size of each cell
LINE_WIDTH = 2  # Thickness of the grid lines
FONT = pygame.font.Font(None, 36)  # Font for numbers
BUTTON_FONT = pygame.font.Font(None, 48)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Button
BUTTON_COLOR = (0, 150, 0)
BUTTON_HOVER_COLOR = (0, 200, 0)
BUTTON_TEXT_COLOR = WHITE

# Sample Sudoku board
board = [
    [0, 9, 7, 0, 8, 0, 4, 0, 0],
    [0, 4, 0, 0, 0, 5, 7, 8, 0],
    [0, 6, 0, 0, 0, 7, 0, 1, 0],
    [9, 0, 6, 0, 7, 0, 0, 4, 3],
    [4, 0, 3, 2, 0, 6, 0, 0, 8],
    [8, 0, 1, 3, 0, 9, 0, 0, 0],
    [6, 8, 5, 1, 3, 0, 0, 0, 0],
    [0, 3, 4, 5, 9, 0, 2, 6, 0],
    [0, 1, 0, 0, 6, 0, 0, 0, 0],
]

original_board = [row[:] for row in board]  # Store original board for comparison


# Create a window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

# Solver function (backtracking algorithm)
def is_valid(board, row, col, num):
    """Check if placing num in board[row][col] is valid."""
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    box_row, box_col = row // 3 * 3, col // 3 * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False
    return True

def solve_sudoku(board):
    """Solve the Sudoku board using backtracking."""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def draw_grid():
    screen.fill(WHITE)
    for i in range(GRID_SIZE + 1):
        line_width = LINE_WIDTH if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH), line_width)
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), line_width)

def draw_numbers(board):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] != 0:
                color = BLACK if original_board[i][j] != 0 else BLUE  # Blue for solved values
                text = FONT.render(str(board[i][j]), True, color)
                x = j * CELL_SIZE + CELL_SIZE // 2 - text.get_width() // 2
                y = i * CELL_SIZE + CELL_SIZE // 2 - text.get_height() // 2
                screen.blit(text, (x, y))

def draw_button():
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 50, 200, 50)
    mouse_pos = pygame.mouse.get_pos()

    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)

    button_text = BUTTON_FONT.render("Solve", True, BUTTON_TEXT_COLOR)
    screen.blit(button_text, (button_rect.x + 50, button_rect.y + 10))

    return button_rect

def main():
    solved = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_rect = draw_button()
                if button_rect.collidepoint(event.pos) and not solved:
                    solved = solve_sudoku(board)  # Solve the Sudoku puzzle

        draw_grid()
        draw_numbers(board)
        button_rect = draw_button()  # Draw the solve button

        pygame.display.update()

if __name__ == '__main__':
    main()
