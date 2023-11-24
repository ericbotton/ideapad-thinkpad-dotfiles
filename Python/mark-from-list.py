import curses
""" with list "mark_items" show list and select from list """
"""   return marked items "

def mark_items(strings):
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    screen.keypad(1)
    marked = [False] * len(strings)
    current = 0
    while True:
        screen.clear()
        for i, string in enumerate(strings):
            if marked[i]:
                screen.addstr(i, 0, string, curses.A_REVERSE)
            else:
                screen.addstr(i, 0, string)
        screen.move(current, 0)
        char = screen.getch()
        if char == curses.KEY_UP:
            current = max(0, current - 1)
        elif char == curses.KEY_DOWN:
            current = min(len(strings) - 1, current + 1)
        elif char == ord(' '):
            marked[current] = not marked[current]
        elif char == ord('\n'):
            break
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()
    return [string for i, string in enumerate(strings) if marked[i]]

strings = ['apple', 'banana', 'cherry', 'date']
marked_strings = mark_items(strings)
print(marked_strings)
