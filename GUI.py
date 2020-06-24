import pygame
from tkinter import *
from tkinter import messagebox
from SudokuSolver import valid, solve
from SudokuAPI import generateSudoku
import time
pygame.font.init()

WINDOW_WIDTH = 540
WINDOW_HEIGHT = 600
SQUARE_SIZE = 60
ROWS = 9
COLS = 9

sudoku = generateSudoku()

class Grid:

    def __init__(self, board):
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT - 60
        self.squares = [[Square(board[i][j], i, j) for j in range(COLS)] for i in range(ROWS)]
        self.model = [[self.squares[i][j].value for j in range(COLS)] for i in range(ROWS)]
        self.selected = None
        solve(self.model)

    def update_model(self):
        self.model = [[self.squares[i][j].value for j in range(COLS)] for i in range(ROWS)]

    def place(self, value):
        row, col = self.selected
        if self.squares[row][col].value == 0:
            self.squares[row][col].set_value(value)
            self.update_model()

            if valid(self.model, (row, col), value) and solve(self.model):
                return True
            else:
                self.squares[row][col].set_value(0)
                self.squares[row][col].set_temp(0)
                self.update_model()
                return False

    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(ROWS + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0, 0, 0), (0, i * SQUARE_SIZE), (self.width,i * SQUARE_SIZE), thick)
            pygame.draw.line(win, (0, 0, 0), (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, self.height), thick)

        # Draw Cubes
        for i in range(ROWS):
            for j in range(COLS):
                self.squares[i][j].draw(win)

    def select(self, row, col):
        # Reset all other
        for i in range(ROWS):
            for j in range(COLS):
                self.squares[i][j].selected = False

        self.squares[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.squares[row][col].value == 0:
            self.squares[row][col].set_temp(0)

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            x = (pos[0] // SQUARE_SIZE)
            y = (pos[1] // SQUARE_SIZE)
            return (int(y), int(x))
        else:
            return None

    def sketch(self, val):
        row, col = self.selected
        self.squares[row][col].set_temp(val)

    def is_finished(self):
        for i in range(ROWS):
            for j in range(COLS):
                if self.squares[i][j].value == 0:
                    return False
        return True

class Square:
    size = SQUARE_SIZE

    def __init__(self, value, row , col):
        self.temp = 0
        self.value = value
        self.row = row
        self.col = col
        self.selected = False

    def draw(self, win):
        fnt_value = pygame.font.SysFont("comicsans", 40)
        fnt_sketch = pygame.font.SysFont("comicsans", 30)

        x = self.col * self.size
        y = self.row * self.size

        if self.value != 0:
            text = fnt_value.render(str(self.value), 1, (128, 128, 128))
            win.blit(text, (x + SQUARE_SIZE / 3, y + SQUARE_SIZE / 3))
        if self.temp != 0:
            text = fnt_sketch.render(str(self.temp), 1, (0, 255, 0))
            x_pos = x + ((SQUARE_SIZE / 3) * ((self.temp - 1) % 3)) + 3
            y_pos = y + (SQUARE_SIZE / 3 * ((self.temp - 1 ) // 3)) + 1
            win.blit(text, (x_pos, y_pos))

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, self.size, self.size), 3)

    def set_value(self, value):
        self.value = value

    def set_temp(self, temp):
        self.temp = temp


    def get_value(self):
        return self.value


def redraw_window(win, board, time, strikes):
    win.fill((255,255,255))
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
    win.blit(text, (540 - 160, 560))
    text = fnt.render( str(strikes) + " / 3 Errors", 1 , (0,0,0))
    win.blit(text, (150, 560))
    # Draw Strikes
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))
    # Draw grid and board
    board.draw(win)


def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat


def solve_visual(win, board, playtime, strikes):
    if not find_empty_square(board):
        return True
    else:
        row, col = find_empty_square(board)
        value = board.model[row][col]
        board.selected = row, col
        board.place(value)
        redraw_window(win, board, playtime, strikes)
        pygame.display.update()
        if solve_visual(win, board, playtime, strikes):
            return True
    return False


def find_empty_square(board):
    for i in range(0,9):
        for j in range(0,9):
            if board.squares[i][j].get_value() == 0:
                return (i,j)
    return None

def check_gameover(win, board, strikes):
    end_menu(win)
    if strikes == 3:
        print("Game over, too many errors")
        Tk().wm_withdraw()  # to hide the main window
        messagebox.showinfo('Sorry!', 'You made too many mistakes, try again!')
        return True
    if board.is_finished():
        print("Game over")
        Tk().wm_withdraw()  # to hide the main window
        messagebox.showinfo('Congrats!', 'You finished the sudoku successfully! Congrats!')
        return True
    return False


def end_menu(win):
    b = Button(Tk(), text="New Sudoku", command=main)
    b.pack()


def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku")
    board = Grid(sudoku)
    key = None
    run = True
    start = time.time()
    strikes = 0
    while run:

        play_time = round(time.time() - start)
        if check_gameover(win, board, strikes):
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.squares[i][j].temp != 0 and board.squares[i][j].value == 0:
                        if board.place(board.squares[i][j].temp):
                            board.squares[i][j].temp = 0
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None


                if event.key == pygame.K_s:
                    solve_visual(win, board, play_time, strikes)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key and board.squares[board.selected[0]][board.selected[1]].value == 0:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()


main()
pygame.quit()