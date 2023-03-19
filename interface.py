import sys
import curses
import user_stories


def init_screen():
    stdscr = curses.initscr()
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_WHITE, -1)
    curses.init_pair(3, curses.COLOR_BLUE, -1)
    curses.init_pair(4, curses.COLOR_RED, -1)
    curses.cbreak()
    curses.noecho()
    curses.curs_set(0)
    stdscr.keypad(True)

    return stdscr


def end_screen(stdscr):
    stdscr.keypad(False)
    curses.echo()
    curses.nocbreak()
    curses.endwin()


def print_menu(stdscr, selected, menu_items):
    stdscr.clear()
    stdscr.addstr(0, 0, "Velg et alternativ:", curses.color_pair(1) | curses.A_BOLD)

    for index, item in enumerate(menu_items):
        if index == selected:
            attr = curses.color_pair(2) | curses.A_REVERSE
        else:
            attr = curses.color_pair(3)

        stdscr.addstr(index + 2, 0, f"{index + 1}: {item}", attr)

    stdscr.refresh()


def get_menu_choice(stdscr):
    menu_items = [
        "Hent togruter for en stasjon på en gitt ukedag",
        "Søk etter togruter mellom to stasjoner",
        "Registrer en ny kunde",
        "Finn ledige billetter og kjøp",
        "Vis informasjon om fremtidige reiser for en kunde",
        "Avslutt programmet",
    ]

    selected = 0
    print_menu(stdscr, selected, menu_items)

    while True:
        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected = (selected - 1) % len(menu_items)
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(menu_items)
        elif key in (curses.KEY_ENTER, ord("\n"), ord("\r")):
            return selected + 1
        elif key in range(ord("1"), ord("6") + 1):
            return key - ord("0")

        print_menu(stdscr, selected, menu_items)



def init(cursor):
    stdscr = init_screen()

    try:
        while True:
            choice = get_menu_choice(stdscr)
            if choice == 6:
                break
            user_stories.handle(cursor, choice)

            # Clear the screen before showing the menu again
            stdscr.clear()
    finally:
        end_screen(stdscr)
