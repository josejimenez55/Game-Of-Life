from random import random
import curses
import time
# test change
def update_grid(window, grid):
    for col in range(curses.COLS - 2):
        for row in range(curses.LINES - 3):
            if grid[row][col]:
                window.addstr(row+1, col+1, ' ', curses.A_REVERSE) #str(grid[row][col])
            else:
                window.addstr(row+1, col+1, '.')
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

    generation = 0 # number of generations

    stdscr.addstr(rows - 1, 2, 'q: exit')
    stdscr.addstr(rows - 1, 15, 'Space: Pause')
    stdscr.addstr(rows - 1, cols - 17, 'Generation: ')
    stdscr.refresh()

    small_box = curses.newwin(rows - 1, cols, 0, 0)
    small_box.box()
    small_box.refresh()

    # create random grid (with padding for wrap-around)
    grid = [[(int(random() * 10) % 2) for _ in range(cols + 2)] for _ in range(rows + 2)]
    temp_grid = [[0 for _ in range(cols + 2)] for _ in range(rows + 2)]
    #grid = [[1,0] * (cols / 2) for _ in range(rows)]
    update_grid(small_box, grid)

    while(True):
        c = stdscr.getch()

	generation = generation + 1
    	stdscr.addstr(rows - 1, cols - 5, str(generation))

        # copy edges for wrap-around
        for column in range(1, cols-1):
            grid[0][column] = grid[-2][column] # top
            grid[-1][column] = grid[1][column] # bottom

        for r in range(1, rows-1):
            grid[r][0] = grid[r][-2] # left
            grid[r][-1] = grid[r][1] # right

        # corners
        grid[0][0] = grid[-2][-2] # top left
        grid[-1][0] = grid[1][-2] # bottom left
        grid[0][-1] = grid[-2][1] # top right
        grid[-1][-1] = grid[1][1] # bottom right

        #grid = [[(int(random() * 10) % 2) for _ in range(cols)] for _ in range(rows)]
        for column in range(1, cols-1):
            for r in range(1, rows-1):
                neighbor_count = 0

                if grid[r-1][column-1]: # top left
                    neighbor_count = neighbor_count + 1
                if grid[r-1][column]: # above
                    neighbor_count = neighbor_count + 1
                if grid[r][column-1]: # left
                    neighbor_count = neighbor_count + 1
                if grid[r][column+1]: # right
                    neighbor_count = neighbor_count + 1
                if grid[r-1][column+1]: # top right
                    neighbor_count = neighbor_count + 1
                if grid[r+1][column+1]: # bottom right
                    neighbor_count = neighbor_count + 1
                if grid[r+1][column]: # below
                    neighbor_count = neighbor_count + 1
                if grid[r+1][column-1]: # bottom left
                    neighbor_count = neighbor_count + 1

                if neighbor_count < 2 and grid[r][column]:
                    temp_grid[r][column] = 0 # cell dies due to starvation
               	elif (neighbor_count == 2 or neighbor_count == 3) and grid[r][column]:
                    temp_grid[r][column] = 1 #neighbor_count # cell lives on if alive and has between 2 and 3 neighbors
                elif neighbor_count > 3:
                    temp_grid[r][column] = 0 # cell dies due to overpopulation
                elif neighbor_count == 3 and grid[r][column] == 0:
		            temp_grid[r][column] = 1 #neighbor_count # cell is born due to reproduction

        #temp = grid
        grid = temp_grid
        temp_grid = [[0 for _ in range(cols + 2)] for _ in range(rows + 2)]

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
