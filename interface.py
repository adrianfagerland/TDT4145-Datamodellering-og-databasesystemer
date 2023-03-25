import sqlite3
import curses
import user_stories
import re



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



def get_menu_choice(stdscr: curses.window):
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

        if key == 27 or key == ord("q"):
            return 6
        elif key == curses.KEY_UP:
            selected = (selected - 1) % len(menu_items)
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(menu_items)
        elif key in (curses.KEY_ENTER, ord("\n"), ord("\r")):
            return selected + 1
        elif key in range(ord("1"), ord("6") + 1):
            return key - ord("0")

        print_menu(stdscr, selected, menu_items)



def init(conn):
    stdscr = init_screen()
    stdscr.clear()
    min_lines = 10
    prev_lines = 0
    while True:
        try:
            current_lines, _ = stdscr.getmaxyx()
            
            if current_lines < min_lines and not (current_lines == prev_lines):
                stdscr.clear()
                stdscr.addstr(0, 0, "Please make the terminal window bigger.")
                stdscr.getch()
                stdscr.refresh()
                prev_lines = current_lines
            else:
                stdscr.clear()
                curses.curs_set(0)
                choice = get_menu_choice(stdscr)
                if choice == 6:
                    break
                user_stories.handle(conn, choice, stdscr)
                    
                # Clear the screen before showing the menu again
                stdscr.clear()
                prev_lines = current_lines
        except curses.error:
            stdscr.clear()
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
    stdscr.clear()
    prompt = "Velg ukedag: "
    curses.curs_set(0)
    ukedager = ["mandag", "tirsdag", "onsdag", "torsdag", "fredag", "lørdag", "søndag"]
    stdscr.addstr(0, 0, prompt)  # Changed to row 0
    stdscr.refresh()
    selected = 0
    while True:
        for idx, ukedag in enumerate(ukedager):
            if idx == selected:
                attr = curses.color_pair(2) | curses.A_REVERSE
            else:
                attr = curses.color_pair(3)

            stdscr.addstr(idx + 1, 0, ukedag, attr)

        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected = (selected - 1) % len(ukedager)
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(ukedager)
        elif key in (curses.KEY_ENTER, ord("\n"), ord("\r")):
            return ukedager[selected]

        stdscr.refresh()



def input_kundenavn(stdscr: curses.window):
    stdscr.clear()
    curses.curs_set(2)
    prompt = "Skriv inn kundenavn: "
    curses.echo()
    stdscr.addstr(0, 0, prompt)
    stdscr.refresh()
    kundenavn = stdscr.getstr().decode('utf-8')
    curses.noecho()
    return kundenavn



def input_epost(cursor: sqlite3.Cursor, stdscr: curses.window):
    stdscr.clear()
    curses.curs_set(2)
    prompt = "Skriv inn e-post: "
    cursor.execute("SELECT LOWER(Epostadresse) FROM Kunde;")
    epostadresser = [row[0] for row in cursor.fetchall()]

    while True:
        curses.echo()
        stdscr.addstr(0, 0, prompt)
        stdscr.refresh()
        epostadresse = stdscr.getstr().decode('utf-8').lower()
        curses.noecho()

        if epostadresse not in epostadresser:
            return epostadresse
        else:
            stdscr.addstr(1, 0, "Epostadressen er allerede i bruk. Prøv igjen.", curses.color_pair(4))
            stdscr.refresh()
            stdscr.getch()
            stdscr.clear()



def input_mobilnummer(cursor: sqlite3.Cursor, stdscr: curses.window):
    stdscr.clear()
    curses.curs_set(2)
    prompt = "Skriv inn telefonnummer: "
    cursor.execute("SELECT LOWER(Mobilnummer) FROM Kunde;")
    telefonnummre = [row[0] for row in cursor.fetchall()]

    while True:
        curses.echo()
        stdscr.addstr(0, 0, prompt)
        stdscr.refresh()
        telefonnummer = stdscr.getstr().decode('utf-8').lower()
        curses.noecho()

        if telefonnummer not in telefonnummre:
            return telefonnummer
        else:
            stdscr.addstr(1, 0, "Telefonnummeret er allerede i bruk. Prøv igjen.", curses.color_pair(4))
            stdscr.refresh()
            stdscr.getch()
            stdscr.clear()



def get_kundenummer(cursor):
    cursor.execute("SELECT MAX(Kundenummer) FROM Kunde;")
    result = cursor.fetchone()[0]
    kundenummer = 1 if result is None else result + 1
    return kundenummer



# input-funkskjon for datoer på formatet yyyy-mm-dd
def input_dato(cursor: sqlite3.Cursor, stdscr: curses.window):
    stdscr.clear()
    curses.curs_set(2)
    prompt = "Skriv inn dato (yyyy-mm-dd): "
    datoformat = re.compile("\d{4}-\d{2}-\d{2}")

    while True:
        curses.echo()
        stdscr.addstr(0, 0, prompt)
        stdscr.refresh()
        dato = stdscr.getstr().decode('utf-8')
        curses.noecho()
        if re.fullmatch(datoformat, dato): # Sjekker om dato er på riktig format. Garanterer ikke at datoen er en reell dato.
            return dato
        else:
            stdscr.addstr(1, 0, "Ugyldig format på datoen. Prøv igjen.", curses.color_pair(4))
            stdscr.refresh()
            stdscr.getch()
            stdscr.clear()
    

# input-funksjon for tider på formatet hh:mm
def input_klokkeslett(cursor: sqlite3.Cursor, stdscr: curses.window):
    stdscr.clear()
    curses.curs_set(2)
    prompt = "Skriv inn tid (hh:mm): "
    tidformat = re.compile("^([0-1][0-9]|2[0-3]):([0-5][0-9])$")

    while True:
        curses.echo()
        stdscr.addstr(0, 0, prompt)
        stdscr.refresh()
        tid = stdscr.getstr().decode('utf-8', 'ignore')
        curses.noecho()
        if re.fullmatch(tidformat, tid): # Sjekker om tid er på riktig format.
            return tid
        else:
            stdscr.addstr(1, 0, "Ugyldig format på tiden. Prøv igjen.", curses.color_pair(4))
            stdscr.refresh()
            stdscr.getch()
            stdscr.clear()