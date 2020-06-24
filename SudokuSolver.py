import time

sudoku = [
    [0,0,4,3,0,0,2,0,9],
    [0,0,5,0,0,9,0,0,1],
    [0,7,0,0,6,0,0,4,3],
    [0,0,6,0,0,2,0,8,7],
    [1,9,0,0,0,7,4,0,0],
    [0,5,0,0,8,3,0,0,0],
    [6,0,0,0,0,0,1,0,5],
    [0,0,3,5,0,8,6,9,0],
    [0,4,2,9,1,0,3,0,0],
]

ROWS = 9
COLS = 9
BOARD_SIZE = len(sudoku[0])


def print_board(board):
    for i in range(BOARD_SIZE):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - -")
        for j in range(BOARD_SIZE):
            if j % 3 == 0 and j != 0:
                print("| ", end="")
            print(str(board[i][j]) + " ", end="")
        print()


def find_empty_square(board):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == 0:
                return (i, j) #row , col
    return None


def valid(board, pos, input):
    # Check row
    for i in range(BOARD_SIZE):
        if board[pos[0]][i] == input and pos[1] != i:
            return False

    # Check column
    for i in range(BOARD_SIZE):
        if board[i][pos[1]] == input and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == input and (i, j) != pos:
                return False

    return True


def solve(board):
    if not find_empty_square(board):
        return True
    else:
        row, col = find_empty_square(board)
        for i in range(1,10):
            if valid(board, (row, col), i):
                board[row][col] = i
                if solve(board):
                    #print_board(board)
                    return True
                board[row][col] = 0
    return False


solve(sudoku)