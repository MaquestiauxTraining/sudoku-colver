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

# Empty Sudoku board (no pre-filled cells)
board = [[0 for _ in range(9)] for _ in range(9)]
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
                # Blue for numbers added by the solver, black for user-entered numbers
                color = BLUE if original_board[i][j] == 0 else BLACK
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

def handle_mouse_click(pos):
    """Select the cell based on the mouse click position."""
    global selected_row, selected_col
    if pos[1] < WIDTH:  # Ensure click is within grid
        selected_row = pos[1] // CELL_SIZE
        selected_col = pos[0] // CELL_SIZE

def handle_key_input(event):
    """Handle number input from the user."""
    if selected_row is not None and selected_col is not None:
        if event.unicode.isdigit() and 1 <= int(event.unicode) <= 9:
            board[selected_row][selected_col] = int(event.unicode)
            original_board[selected_row][selected_col] = int(event.unicode)  # Mark as user-entered
        elif event.key == pygame.K_BACKSPACE:  # Clear the cell
            board[selected_row][selected_col] = 0
            original_board[selected_row][selected_col] = 0  # Clear the original board too

def draw_selected_cell():
    if selected_row is not None and selected_col is not None:
        pygame.draw.rect(screen, GRAY, (selected_col * CELL_SIZE, selected_row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

def move_to_next_cell():
    """Move the selection to the next cell, wrapping around rows and columns."""
    global selected_row, selected_col
    if selected_row is not None and selected_col is not None:
        selected_col += 1
        if selected_col >= GRID_SIZE:  # Move to next row if end of column is reached
            selected_col = 0
            selected_row += 1
            if selected_row >= GRID_SIZE:  # Wrap around to the first cell
                selected_row = 0

def move_to_previous_cell():
    """Move the selection to the previous cell, wrapping around rows and columns."""
    global selected_row, selected_col
    if selected_row is not None and selected_col is not None:
        selected_col -= 1
        if selected_col < 0:  # Move to previous row if start of column is reached
            selected_col = GRID_SIZE - 1
            selected_row -= 1
            if selected_row < 0:  # Wrap around to the last cell
                selected_row = GRID_SIZE - 1

def move_up():
    global selected_row
    selected_row -= 1
    if selected_row < 0:
        selected_row = GRID_SIZE - 1

def move_down():
    global selected_row
    selected_row += 1
    if selected_row >= GRID_SIZE:
        selected_row = 0

def move_left():
    global selected_col
    selected_col -= 1
    if selected_col < 0:
        selected_col = GRID_SIZE - 1

def move_right():
    global selected_col
    selected_col += 1
    if selected_col >= GRID_SIZE:
        selected_col = 0

# Initial state
selected_row, selected_col = 0, 0  # Start at top-left (0,0)

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
                else:
                    handle_mouse_click(event.pos)  # Handle grid click
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:  # Move to the next cell on Tab key press
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:  # Check if Shift is pressed
                        move_to_previous_cell()
                    else:
                        move_to_next_cell()
                elif event.key == pygame.K_UP:
                    move_up()  # Move up
                elif event.key == pygame.K_DOWN:
                    move_down()  # Move down
                elif event.key == pygame.K_LEFT:
                    move_left()  # Move left
                elif event.key == pygame.K_RIGHT:
                    move_right()  # Move right
                else:
                    handle_key_input(event)  # Handle number input

        draw_grid()
        draw_selected_cell()
        draw_numbers(board)
        button_rect = draw_button()  # Draw the solve button

        pygame.display.update()

if __name__ == '__main__':
    main()
