from random import random
import curses
import time

def update_grid(window, grid):
    for col in range(curses.COLS - 2):
        for row in range(curses.LINES - 3):
            if grid[row][col]:
                window.addstr(row+1, col+1, str(grid[row][col]), curses.A_REVERSE)
            else:
                window.addstr(row+1, col+1, ' ')
    window.refresh()


def main():
    # create and initialize curses window
    stdscr = curses.initscr()
    #curses.start_color()
    curses.noecho()
    curses.cbreak() 
    curses.curs_set(0)

    cols = curses.COLS # number of columns in screen
    rows = curses.LINES # rows

    stdscr.addstr(rows - 1, 2, 'q: exit')
    stdscr.addstr(rows - 1, 15, 'Space: Pause')
    stdscr.refresh()
    small_box = curses.newwin(rows - 1, cols, 0, 0)
    small_box.box()
    small_box.refresh()

    # create random grid
    grid = [[(int(random() * 10) % 2) for _ in range(cols)] for _ in range(rows)]
    temp_grid = [[0 for _ in range(cols)] for _ in range(rows)]
    #grid = [[1,0] * (cols / 2) for _ in range(rows)]
    update_grid(small_box, grid)

    while(True):
        c = stdscr.getch()

        #grid = [[(int(random() * 10) % 2) for _ in range(cols)] for _ in range(rows)]
        for column in range(cols):
            for r in range(rows):
                neighbor_count = 0
                r_original = r
                column_original = column

                neighbor_count = neighbor_count + grid[r-1][column-1] # top left
                neighbor_count = neighbor_count + grid[r-1][column] # above
                neighbor_count = neighbor_count + grid[r][column-1] # left
                # right
                if column == len(grid[0]) - 1:
                    column = -1
                neighbor_count = neighbor_count + grid[r][column+1]

                neighbor_count = neighbor_count + grid[r-1][column+1] # top right
                
                # bottom right
                if r == len(grid) - 1:
                    r = -1
                neighbor_count = neighbor_count + grid[r+1][column+1]
                column = column_original
                # below
                neighbor_count = neighbor_count + grid[r+1][column]
                # bottom left
                neighbor_count = neighbor_count + grid[r+1][column-1]

                r = r_original
                if neighbor_count < 2:
                    temp_grid[r][column] = 0 # cell dies due to starvation
               	elif neighbor_count <= 3 and grid[r][column]:
		    #pass
                    temp_grid[r][column] = neighbor_count # cell lives on if alive and has between 2 and 3 neighbors
                elif neighbor_count > 3:
                    temp_grid[r][column] = 0 # cell dies due to overpopulation
                elif neighbor_count == 3:
		    temp_grid[r][column] = neighbor_count # cell is born due to reproduction

        temp = grid
        grid = temp_grid
        temp_grid = temp
        update_grid(small_box, grid)
        if(c == ord('q')):
            break
    

    #time.sleep(2)

    #c = stdscr.getch()

    curses.nocbreak()
    curses.echo()
    curses.endwin()


if __name__ == "__main__":
    main()
