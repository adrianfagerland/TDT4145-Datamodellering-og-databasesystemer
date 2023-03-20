import sqlite3
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
            user_stories.handle(cursor, choice, stdscr)

            # Clear the screen before showing the menu again
            stdscr.clear()
    finally:
        end_screen(stdscr)

def input_stasjon(cursor: sqlite3.Cursor, stdscr: curses.window):

    stdscr.clear()
    curses.curs_set(2)
    prompt = "Skriv inn stasjon: "
    cursor.execute("SELECT LOWER(Stasjonnavn) FROM Stasjon;")
    stations = [row[0] for row in cursor.fetchall()]

    while True:
        curses.echo()
        stdscr.addstr(0, 0, prompt)
        stdscr.refresh()
        stasjon = stdscr.getstr().decode('utf-8').lower()
        curses.noecho()

        if stasjon in stations:
            return stasjon
        else:
            stdscr.addstr(1, 0, "Ugyldig stasjon. Prøv igjen.", curses.color_pair(4))
            stdscr.refresh()
            stdscr.getch()
            stdscr.clear()


def input_ukedag(stdscr):
    prompt = "Velg ukedag: "
    curses.curs_set(0)
    ukedager = ["mandag", "tirsdag", "onsdag", "torsdag", "fredag", "lørdag", "søndag"]
    stdscr.addstr(2, 0, prompt)  # Changed to row 0
    stdscr.refresh()
    selected = 0
    while True:
        for idx, ukedag in enumerate(ukedager):
            if idx == selected:
                attr = curses.color_pair(2) | curses.A_REVERSE
            else:
                attr = curses.color_pair(3)

            stdscr.addstr(idx + 3, 0, ukedag, attr)  # Changed from idx + 2 to idx + 1

        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected = (selected - 1) % len(ukedager)
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(ukedager)
        elif key in (curses.KEY_ENTER, ord("\n"), ord("\r")):
            return ukedager[selected]

        stdscr.refresh()
