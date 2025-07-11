import pygame
import time
import copy

pygame.init()
pygame.font.init()


class Grid:
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.win = win
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.model = None
        self.selected = None
        self.update_model()
        self.solved_board = self.get_solved_board()

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if val == self.solved_board[row][col]:
                return True
            else:
                self.cubes[row][col].set(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self):
        gap = self.width / 9
        for i in range(self.rows + 1):
            thick = 4 if i % 3 == 0 else 1
            pygame.draw.line(self.win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    def select(self, row, col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        if self.selected:
            row, col = self.selected
            self.cubes[row][col].set(0)
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def find_empty(self, bo):
        for i in range(len(bo)):
            for j in range(len(bo[0])):
                if bo[i][j] == 0:
                    return (i, j)
        return None

    def solve_gui(self):
        self.update_model()
        find = self.find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.is_valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.win, True)
                pygame.display.update()
                pygame.time.delay(30)

                if self.solve_gui():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(30)
        return False

    def get_solved_board(self):
        model = copy.deepcopy(self.model)
        self.solve_logic(model)
        return model

    def solve_logic(self, bo):
        find = self.find_empty(bo)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.is_valid(bo, i, (row, col)):
                bo[row][col] = i
                if self.solve_logic(bo):
                    return True
                bo[row][col] = 0
        return False

    def is_valid(self, bo, num, pos):
        for i in range(len(bo[0])):
            if bo[pos[0]][i] == num and pos[1] != i:
                return False
        for i in range(len(bo)):
            if bo[i][pos[1]] == num and pos[0] != i:
                return False
        box_x, box_y = pos[1] // 3, pos[0] // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if bo[i][j] == num and (i, j) != pos:
                    return False
        return True


class Cube:
    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("Consolas", 40)
        gap = self.width / 9
        x, y = self.col * gap, self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x + 5, y + 5))
        elif self.value != 0:
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("Consolas", 40)
        gap = self.width / 9
        x, y = self.col * gap, self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)
        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        color = (0, 255, 0) if g else (255, 0, 0)
        pygame.draw.rect(win, color, (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def redraw_window(win, board, play_time, strikes):
    win.fill((255, 255, 255))
    fnt = pygame.font.SysFont("Consolas", 20)
    text = fnt.render("Time: " + format_time(play_time), 1, (0, 0, 0))
    win.blit(text, (540 - 160, 560))
    text = fnt.render("Strikes: " + "X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))
    fnt_small = pygame.font.SysFont("Consolas", 16)
    instructions = fnt_small.render("LEFT_CLICK+number+ENTER | SPACE to solve | C to clear", 1, (100, 100, 100))
    win.blit(instructions, (20, 580))
    board.draw()


def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    return f"{minute:02}:{sec:02}"


def main():
    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Interactive Sudoku Solver")
    board = Grid(9, 9, 540, 540, win)
    run = True
    start = time.time()
    strikes = 0
    key = None

    while run:
        play_time = round(time.time() - start)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7,
                                 pygame.K_8, pygame.K_9]:
                    key = int(pygame.key.name(event.key))
                if event.key == pygame.K_c:
                    board = Grid(9, 9, 540, 540, win)
                    strikes = 0
                    start = time.time()
                if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    board.clear()
                    key = None
                if event.key == pygame.K_SPACE:
                    board.solve_gui()
                if event.key == pygame.K_RETURN:
                    if board.selected:
                        i, j = board.selected
                        if board.cubes[i][j].temp != 0:
                            if not board.place(board.cubes[i][j].temp):
                                strikes += 1
                            key = None
                            board.solved_board = board.get_solved_board()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key is not None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()


if __name__ == "__main__":
    main()
