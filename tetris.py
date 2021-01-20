import pygame
import sys
from shape import Shape, T, L, LAlt, Skew, SkewAlt, Square, Straight
from random import random

TILE_SIZE = 40
SCREEN_WIDTH = TILE_SIZE * 10 + 11 # tetris board is 10 tiles wide, leaving a one pixel gap between tiles
SCREEN_HEIGHT = TILE_SIZE * 20 + 21 # 20 tiles tall, one pixel gap between tiles
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# directions for updating active shape position
DOWN = 0
LEFT = 1
RIGHT = 2

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
screen.fill((100,100,100))
pygame.display.set_caption('Tetris')

MOVEEVENT, t = pygame.USEREVENT + 1, 250

game_over = False

board = []
active_shape = None

# initialize the board to be empty
def init_board():
    global board

    board = [[None for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

def draw_game_board():
    """
    Draws the game board.
    board[i][j] refers to row i, column j
    """
    for i in range(len(board)):
        for j in range(len(board[i])):
            color = (20,20,20)

            if board[i][j] != None:
                color = board[i][j]

            pygame.draw.rect(
                screen,
                color,
                (j * TILE_SIZE + (j + 1), i * TILE_SIZE + (i + 1), TILE_SIZE, TILE_SIZE)
            )

def spawn_shape():
    """
    Spawn a random shape at the top of the game board.
    Need to do a check to make sure the game board isn't so full
    that a shape is spawning on top of another.
    """
    global active_shape

    rand_no = int(random() * 7)
    shape = None

    # get a random shape
    if rand_no == 0:
        shape = T()
    elif rand_no == 1:
        shape = L()
    elif rand_no == 2:
        shape = LAlt()
    elif rand_no == 3:
        shape = Skew()
    elif rand_no == 4:
        shape = SkewAlt()
    elif rand_no == 5:
        shape = Square()
    elif rand_no == 6:
        shape = Straight()
    
    active_shape = shape

    # add the shape to the board
    add_shape_to_board(shape)

def add_shape_to_board(shape: Shape):
    global board

    for c in shape.coordinates:
        vert_pos = c[0]
        horiz_pos = c[1]
        board[vert_pos][horiz_pos] = shape.color

def clear_active_shape():
    """
    Clear the active shape from the board.
    """
    global board

    for c in active_shape.coordinates:
        vert_pos = c[0]
        horiz_pos = c[1]
        board[vert_pos][horiz_pos] = None

def update_active_shape(dir: int):
    """
    Clear the active shape from the board, update it's position, and redraw it.
    """
    clear_active_shape()

    if dir == 0:
        attempt_move_down()
    elif dir == 1:
        attempt_move_left()
    elif dir == 2:
        attempt_move_right()

    add_shape_to_board(active_shape)

def jump_down():
    """
    Move the active shape down until it cannot go any further. This action
    is invoked by pressing the space key.
    """
    clear_active_shape()
    can_move_down = True

    while can_move_down:
        can_move_down = attempt_move_down()

def attempt_move_down():
    # don't move if already on bottom edge of screen or there are block below
    for c in active_shape.coordinates:
        if c[0] >= BOARD_HEIGHT - 1 or (board[c[0] + 1][c[1]] != None and [c[0] + 1, c[1]] not in active_shape.coordinates):
            # When the active shape reaches a stopping point, save it to the board and 
            # spawn a new shape when the current shape stops.
            # It is necessary to add the shape to the board again here so that it gets saved to the board
            # after the new shape is spawned. Before this method gets called in update_active_shape(), the 
            # active shape is cleared from the board, so this adds it again.
            add_shape_to_board(active_shape)
            check_completed_rows() # check if a row is full
            spawn_shape()
            return False

    active_shape.move_down()
    return True

def check_completed_rows():
    """
    Check if a row has been filled. If it has, the row should be deleted 
    and all filled blocks above that row should be shifted down.
    """
    for i in range(len(board)):
        row_complete = True

        for j in range(len(board[i])):
            if board[i][j] == None:
                row_complete = False
                break
        
        # if the row was completed, shift all blocks above it down by one
        if row_complete:
            for k in range(i, 0, -1):
                for j in range(len(board[k])):
                    board[k][j] = board[k - 1][j]

def save_board_to_file():
    with open('board.txt', 'w') as f:
        for i in range(len(board)):
            for j in range(len(board[i])):
                tile = '-' if board[i][j] == None else 'X'
                f.write(tile + ' ')
            f.write('\n')

def attempt_move_left():
    # don't move if already on left edge of screen
    for c in active_shape.coordinates:
        if c[1] <= 0 or (board[c[0]][c[1] - 1] != None and [c[0], c[1] - 1] not in active_shape.coordinates):
            return

    active_shape.move_left()

def attempt_move_right():
    # don't move if already on right edge of screen
    for c in active_shape.coordinates:
        if c[1] >= BOARD_WIDTH - 1 or (board[c[0]][c[1] + 1] != None and [c[0], c[1] + 1] not in active_shape.coordinates):
            return

    active_shape.move_right()

def rotate_and_update():
    """
    Clear the shape from the board, rotate it, and redraw it.
    """
    clear_active_shape()
    active_shape.rotate()
    add_shape_to_board(active_shape)

def main_loop():
    global game_over

    # timer for updating the active shape's position
    pygame.time.set_timer(MOVEEVENT, t)

    init_board()
    spawn_shape()

    left_pressed = False
    right_pressed = False

    while not game_over:
        draw_game_board()

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    update_active_shape(LEFT)
                elif event.key == pygame.K_RIGHT:
                    update_active_shape(RIGHT)
                elif event.key == pygame.K_UP:
                    rotate_and_update()
                elif event.key == pygame.K_DOWN:
                    update_active_shape(DOWN)
                elif event.key == pygame.K_SPACE:
                    jump_down()

            if event.type == MOVEEVENT:
                update_active_shape(DOWN)

            if event.type == pygame.QUIT:
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]: # escape to quit the game
            game_over = True

        pygame.display.update()

if __name__ == '__main__':
    pygame.init()
    main_loop()
    pygame.quit()
    quit()