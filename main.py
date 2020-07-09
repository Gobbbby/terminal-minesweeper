import curses
import numpy as np


BOARDSIZE = 16
MINESNUM = 20
renderBoard = [['  ' for _ in range(BOARDSIZE)] for _ in range(BOARDSIZE)]
board = np.zeros((BOARDSIZE, BOARDSIZE), dtype='int32')
mines = np.empty((MINESNUM, 2), dtype='int32')

for i in range(MINESNUM):
    if i == 0:
        mines[i][0], mines[i][1] = np.random.randint(BOARDSIZE), np.random.randint(BOARDSIZE)
    else:
        corChoice = np.arange(BOARDSIZE)
        mines[i][0] = np.random.choice(corChoice)
        used = np.array([], dtype='int32')
        for mineCor in mines:
            if mineCor[0] == mines[i][0]:
                np.append(used, mineCor[1])
        mines[i][1] = np.random.choice(np.delete(corChoice, used))

for i in range(MINESNUM):
    mX, mY = mines[i][0], mines[i][1]
    board[mY][mX] = 10
    for x in range(-1, 2):
        for y in range(-1, 2):
            if -1 < mY+y < BOARDSIZE and -1 < mX+x < BOARDSIZE: board[mY+y][mX+x] += 1

def floodfill(y, x):
    if board[y][x] == 0:
        renderBoard[y][x] = '0 '

        for opX in [0, +1, -1]:
            for opY in [0, +1, -1]:
                if x+opX > -1 and x+opX < BOARDSIZE and y+opY > -1 and y+opY < BOARDSIZE and renderBoard[y+opY][x+opX] == '  ':
                    renderBoard[y+opY][x+opX] = str(board[y+opY][x+opX]) + ' ' if board[y+opY][x+opX] < 10 else '  '
                    floodfill(y+opY, x+opX)


endGame = {'win': False, 'lose': False}
flagging = [False]
flaggedNum = [0]

def step(y, x):
    if BOARDSIZE < x < BOARDSIZE+6 and 5 < y < 8:
        if flagging[0]:
            flagging[0] = False
        else:
            flagging[0] = True

    if -1 < y < BOARDSIZE and -1 < x < BOARDSIZE:
        if not flagging[0]:
            if renderBoard[y][x] != 'F ':
                if board[y][x] > 10:
                    renderBoard[y][x] = 'M '
                    endGame['lose'] = True
                elif board[y][x] == 0:
                    floodfill(y, x)
                else:
                    renderBoard[y][x] = str(board[y][x]) + ' '
        elif renderBoard[y][x] == '  ':
            renderBoard[y][x] = 'F '
            flaggedNum[0] += 1
        elif renderBoard[y][x] == 'F ':
            renderBoard[y][x] = '  '
            flaggedNum[0] -= 1
    
    if [cell for row in renderBoard for cell in row].count('  ') + [cell for row in renderBoard for cell in row].count('F ') == MINESNUM:
        endGame['win'] = True


labelsDistance = 4+BOARDSIZE*2

def render(stdscr):
    try:
        for yProgress, row in enumerate(renderBoard):
            for xProgress, cell in enumerate(row):
                if cell == '  ' or cell == 'F ':
                    stdscr.addstr(1+yProgress, 2+xProgress*2, cell, curses.color_pair((xProgress+yProgress)%2+1))
                else:
                    stdscr.addstr(1+yProgress, 2+xProgress*2, cell if cell != '0 ' else '  ', curses.color_pair(3))
    except(curses.error):
        return

    stdscr.addstr(1, labelsDistance, 'MINESWEEPER', curses.A_UNDERLINE)
    stdscr.addstr(2, labelsDistance, f'Size: {BOARDSIZE}x{BOARDSIZE}')
    stdscr.addstr(3, labelsDistance, f'Mines: {MINESNUM}')
    stdscr.addstr(4, labelsDistance, f'Flagged: {flaggedNum[0]}')
    stdscr.addstr(6, labelsDistance, 'Mode:', curses.A_UNDERLINE)
    stdscr.addstr(7, labelsDistance, ' Digging ', curses.A_NORMAL if flagging[0] else curses.A_REVERSE)
    stdscr.addstr(8, labelsDistance, ' Flagging ', curses.A_REVERSE if flagging[0] else curses.A_NORMAL)

    if True in endGame.values():
        yDistance = round(BOARDSIZE/2) + (1 if BOARDSIZE % 2 == 1 else 0)
        progress = round(100 - ([cell for row in renderBoard for cell in row].count('  ') + sum([1 for row in range(BOARDSIZE) for cell in range(BOARDSIZE) if renderBoard[row][cell] == 'F ' and board[row][cell] > 10]) + 1 if endGame['lose'] else 0) / BOARDSIZE**2 * 100, 1)
        stdscr.addstr(yDistance-1, BOARDSIZE-6, ' you lose... :( ' if endGame['lose'] else ' YOU WIN!!! :)  ', curses.A_BOLD)
        stdscr.addstr(yDistance, BOARDSIZE-6, f' Score: {progress}%' + ' '*(7-len(str(progress))), curses.A_BOLD)
        stdscr.addstr(yDistance+1, BOARDSIZE-6, ' click to exit. ', curses.A_BOLD)


def getMouse():
    try:
        _, x, y, *_ = curses.getmouse()
        return y-1, (x-2)//2
    except(curses.error):
        return -1, -1


def main(stdscr):
    curses.curs_set(0)
    x = curses.mousemask(1)
    stdscr.clear()
    curses.init_pair(1, 0, 40)
    curses.init_pair(2, 7, 28)
    curses.init_pair(3, 0, 101)
    while True:
        render(stdscr)
        key = stdscr.getch()
        while True in endGame.values():
            if key: exit()
        if key == curses.KEY_MOUSE:
            y, x = getMouse()
            stdscr.clear()
            step(y, x)
            stdscr.refresh()

stdscr = curses.initscr()
curses.wrapper(main)