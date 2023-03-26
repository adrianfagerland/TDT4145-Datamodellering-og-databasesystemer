import sqlite3
import curses
import re
import datetime
import threading

import user_stories
import train


# Antar norske mobilnummer, består av 8 siffer

def init(conn):
    stdscr = init_screen()
    stdscr.clear()
    min_lines = 17
    prev_lines = 0
    min_columns = 115
    prev_columns = 0
    try:
        while True:
            try:
                current_lines, current_columns = stdscr.getmaxyx()

                if current_lines < min_lines and not (current_lines == prev_lines) or current_columns < min_columns and not (current_columns == prev_columns):
                    stdscr.clear()
                    stdscr.addstr(
                        0, 0, "Please make the terminal window bigger.")
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
    finally:
        end_screen(stdscr)


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


def print_menu(stdscr: curses.window, selected, menu_items):
    stdscr.addstr(0, 0, "Velg et alternativ:",
                  curses.color_pair(1) | curses.A_BOLD)

    for index, item in enumerate(menu_items):
        if index == selected:
            attr = curses.color_pair(2) | curses.A_REVERSE
        else:
            attr = curses.color_pair(3)

        stdscr.addstr(index*2 + 2, 0, f"{index + 1}: {item}", attr)

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
    stdscr.clear()
    print_menu(stdscr, selected, menu_items)

    stop_event = threading.Event()
    screen_lock = threading.Lock()
    train_thread = threading.Thread(
        target=train.train_animation, args=(stdscr, stop_event, screen_lock))
    train_thread.daemon = True
    train_thread.start()

    while True:
        key = stdscr.getch()

        if key == 27 or key == ord("q"):
            stop_event.set()
            train_thread.join()
            return 6
        elif key == curses.KEY_UP:
            selected = (selected - 1) % len(menu_items)
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(menu_items)
        elif key in (curses.KEY_ENTER, ord("\n"), ord("\r")):
            stop_event.set()
            train_thread.join()
            return selected + 1
        elif key in range(ord("1"), ord("6") + 1):
            stop_event.set()
            train_thread.join()
            return key - ord("0")

        with screen_lock:
            print_menu(stdscr, selected, menu_items)


def selectable_menu(stdscr: curses.window, prompt, options: list):
    curses.curs_set(0)
    curses.noecho()
    selected_login_type = 0
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, prompt, curses.color_pair(1))
        for i, display_text in enumerate(options):
            if i == selected_login_type:
                stdscr.addstr(i+2, 0, f"{display_text}",
                              curses.color_pair(2) | curses.A_REVERSE)
            else:
                stdscr.addstr(
                    i+2, 0, f"{display_text}", curses.color_pair(3))
        stdscr.refresh()

        c = stdscr.getch()
        if c == curses.KEY_UP and selected_login_type > 0:
            selected_login_type -= 1
        elif c == curses.KEY_DOWN and selected_login_type < len(options) - 1:
            selected_login_type += 1
        elif c == curses.KEY_ENTER or c == 10 or c == 13:
            return options[selected_login_type]


def velg_stasjon(cursor: sqlite3.Cursor, stdscr: curses.window, prompt: str, exclude: str = ""):
    stdscr.clear()
    curses.curs_set(2)
    cursor.execute("""
        SELECT Stasjonnavn
        FROM Stasjon""")
    stations = [row[0] for row in cursor.fetchall() if row[0] not in exclude]
    return selectable_menu(stdscr, prompt, stations)


def velg_avreisestasjon(cursor: sqlite3.Cursor, stdscr: curses.window):
    return velg_stasjon(cursor, stdscr, "Velg avreisestasjon:")


def velg_ankomststasjon(cursor: sqlite3.Cursor, stdscr: curses.window, startstasjon):
    return velg_stasjon(cursor, stdscr, "Velg ankomststasjon:", startstasjon)


def input_ukedag(stdscr: curses.window):
    prompt = "Velg ukedag: "
    ukedager = ["Mandag", "Tirsdag", "Onsdag",
                "Torsdag", "Fredag", "Lørdag", "Søndag"]
    return selectable_menu(stdscr, prompt, ukedager).capitalize()


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
            stdscr.addstr(
                1, 0, "Epostadressen er allerede i bruk. Prøv igjen.", curses.color_pair(4))
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
            stdscr.addstr(
                1, 0, "Telefonnummeret er allerede i bruk. Prøv igjen.", curses.color_pair(4))
            stdscr.refresh()
            stdscr.getch()
            stdscr.clear()


def get_kundenummer(cursor):
    cursor.execute("SELECT MAX(Kundenummer) FROM Kunde;")
    result = cursor.fetchone()[0]
    kundenummer = 1 if result is None else int(result) + 1
    return kundenummer


def input_dato(stdscr: curses.window):
    stdscr.clear()
    curses.curs_set(2)
    prompt = "Skriv inn dato (yyyy-mm-dd): "
    while True:
        curses.echo()
        stdscr.addstr(0, 0, prompt)
        stdscr.refresh()
        dato = stdscr.getstr().decode('utf-8')
        curses.noecho()
        try:
            # Sjekker om dato er på riktig format. Datetime garanterer at datoen er en reell dato.
            datetime.datetime.strptime(dato, '%Y-%m-%d')
            return dato
        except ValueError:
            stdscr.addstr(1, 0, "Ugyldig datoen. Prøv igjen.",
                          curses.color_pair(4))
            stdscr.refresh()
            stdscr.getch()
            stdscr.clear()


# input-funksjon for tider på formatet hh:mm
def input_klokkeslett(stdscr: curses.window):
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
        if re.fullmatch(tidformat, tid):  # Sjekker om tid er på riktig format.
            return tid
        else:
            stdscr.addstr(
                1, 0, "Ugyldig format på tiden. Prøv igjen.", curses.color_pair(4))
            stdscr.refresh()
            stdscr.getch()
            stdscr.clear()


def login(conn: sqlite3.Connection, stdscr: curses.window):
    cursor = conn.cursor()

    login_types = ["Mobilnummer", "Kundenummer"]
    prompt = "Hvordan vil du logge inn?"
    login_type = selectable_menu(stdscr, prompt, login_types)

    stdscr.clear()
    curses.curs_set(2)
    curses.echo()
    while True:
        stdscr.addstr(0, 0, f"Skriv inn ditt {login_type.lower()}: ")
        stdscr.refresh()
        kunde_id = stdscr.getstr().decode('utf-8').lower()
        query = f"""
        SELECT Kundenummer FROM Kunde 
        WHERE {login_type} = ?
        """
        cursor.execute(query, (kunde_id,))

        # Skriv ut resultatene
        stdscr.clear()
        result = cursor.fetchone()
        curses.noecho()

        if result:
            kundenummer = result[0]
            return kundenummer
        else:
            stdscr.addstr(
                1, 0, f"Finner ingen kunde for dette {login_type}et. Prøv igjen.", curses.color_pair(4))
            stdscr.refresh()
            stdscr.getch()
            stdscr.clear()


def input_reisedato(cursor: sqlite3.Cursor, stdscr: curses.window):
    stdscr.clear()
    curses.curs_set(2)
    prompt = "Skriv inn ønsket avreisedato (yyyy-mm-dd): "
    datoformat = re.compile("\d{4}-\d{2}-\d{2}")

    while True:
        curses.echo()
        stdscr.addstr(0, 0, prompt)
        stdscr.refresh()
        dato = stdscr.getstr().decode('utf-8')
        curses.noecho()
        # Sjekker om dato er på riktig format. Garanterer ikke at datoen er en reell dato.
        if re.fullmatch(datoformat, dato):
            try:
                # Funker dette?
                input_dato = datetime.datetime.strptime(
                    dato, "%Y-%m-%d").date()
                if input_dato >= datetime.date.today():
                    return dato
                else:
                    stdscr.addstr(
                        1, 0, "Datoen kan ikke være i fortid. Prøv igjen.", curses.color_pair(4))
                    stdscr.refresh()
                    stdscr.getch()
                    stdscr.clear()
            except ValueError:
                stdscr.addstr(1, 0, "Ugyldig dato. Prøv igjen.",
                              curses.color_pair(4))
                stdscr.refresh()
                stdscr.getch()
                stdscr.clear()
        else:
            stdscr.addstr(
                1, 0, "Ugyldig format på datoen. Prøv igjen.", curses.color_pair(4))
            stdscr.refresh()
            stdscr.getch()
            stdscr.clear()


def make_billettID(cursor: sqlite3.Cursor):
    cursor.execute("SELECT MAX(BillettID) FROM Billett;")
    result = cursor.fetchone()[0]
    billettID = 1 if result is None else int(result) + 1
    return billettID


def make_kundeordrenummer(cursor: sqlite3.Cursor):
    cursor.execute("SELECT MAX(Kundeordrenummer) FROM Kundeordre;")
    result = cursor.fetchone()[0]
    kundeordrenummer = 1 if result is None else int(result) + 1
    return kundeordrenummer


def get_kjopsdato():
    now = datetime.datetime.now()  # Få dagens dato
    kjopsdato = now.strftime("%Y-%m-%d")  # Konverter datoen til ønsket format

    return kjopsdato  # Returner datoen


def get_kjopstidspunkt():
    now = datetime.datetime.now()  # Få dagens dato og tid
    # Konverter tidspunktet til ønsket format
    kjopstidspunkt = now.strftime("%H:%M")

    return kjopstidspunkt


def input_billetter(cursor: sqlite3.Cursor, stdscr: curses.window, antallTilgjengeligeBilletter, billettype):
    stdscr.clear()
    curses.curs_set(2)
    reserverasjon = ""
    if billettype == "seng":
        reserverasjon = "senger"
    if billettype == "sete":
        reserverasjon = "seter"
    prompt = f"Det er {antallTilgjengeligeBilletter} ledige {reserverasjon}. Skriv inn antall billetter du vil kjøpe: "
    while True:
        curses.echo()
        stdscr.addstr(0, 0, prompt)
        stdscr.refresh()
        antall_str = stdscr.getstr().decode('utf-8').lower().strip()
        curses.noecho()

        try:
            antall = int(antall_str)
            if antall <= antallTilgjengeligeBilletter and antall > 0:
                return antall
            else:
                stdscr.addstr(
                    1, 0, "Du må kjøpe et positivt antall billetter, og ikke flere enn det er tilgjengelig. Prøv igjen.", curses.color_pair(4))
                stdscr.refresh()
                stdscr.getch()
                stdscr.clear()
        except ValueError:
            stdscr.addstr(
                1, 0, "Du må skrive inn et gyldig antall. Prøv igjen.", curses.color_pair(4))
            stdscr.refresh()
            stdscr.getch()
            stdscr.clear()


def input_togrute(cursor: sqlite3.Cursor, stdscr: curses.window):
    stdscr.clear()
    curses.curs_set(2)
    cursor.execute("SELECT (TogruteID) FROM Togrute;")
    ruter = [row[0] for row in cursor.fetchall()]
    prompt = "Potensielle togruter: "
    for rute in ruter:
        prompt += rute + ", "
    prompt += "\nVelg togrute: "

    while True:
        curses.echo()
        stdscr.addstr(0, 0, prompt)
        stdscr.refresh()
        valgtRute = stdscr.getstr().decode('utf-8')
        curses.noecho()

        if valgtRute in ruter:
            return valgtRute
        else:
            stdscr.addstr(1, 0, "Ugyldig rute. Prøv igjen.",
                          curses.color_pair(4))
            stdscr.refresh()
            stdscr.getch()
            stdscr.clear()


def velg_billettype(cursor: sqlite3.Cursor, stdscr: curses.window):
    prompt = "Velg billettype:"
    options = ["Seng", "Sete"]
    return selectable_menu(stdscr, prompt, options).lower()


def input_vognnummer(cursor: sqlite3.Cursor, stdscr: curses.window, togrute, type):
    stdscr.clear()
    curses.curs_set(2)
    if type == "sete":
        cursor.execute("""
        SELECT V.Vognnummer, V.AvType
        FROM Vogn AS V
        JOIN Vogntype AS VT ON V.AvType = VT.Vogntypenavn
        WHERE V.Togoppsett = (
            SELECT Togoppsett
            FROM Togrute
            WHERE TogruteID = ?
        ) AND VT.Type = 'Sitte'
        ORDER BY V.Vognnummer;
        """,
                       (togrute,))
    if type == "seng":
        cursor.execute("""
        SELECT V.Vognnummer, V.AvType
        FROM Vogn AS V
        JOIN Vogntype AS VT ON V.AvType = VT.Vogntypenavn
        WHERE V.Togoppsett = (
            SELECT Togoppsett
            FROM Togrute
            WHERE TogruteID = ?
        ) AND VT.Type = 'Sove'
        ORDER BY V.Vognnummer;
        """,
                       (togrute,))

    vogner = cursor.fetchall()
    prompt = "Tilgjengelige vogner er følgende:"

    for vogn in vogner:
        prompt += (f"Vognnummer: {vogn[0]}, Vogntype: {vogn[1]}")
    prompt += "\nSkriv hvilket vognnummer du vil reise med: "

    while True:
        try:
            curses.echo()
            stdscr.addstr(0, 0, prompt)
            stdscr.refresh()
            vognnummer = stdscr.getstr().decode('utf-8').lower()
            curses.noecho()

            if int(vognnummer) in vogner[0]:
                return vognnummer
            else:
                stdscr.addstr(1, 0, "Ugyldig vognnummer. Prøv igjen.",
                              curses.color_pair(4))
                stdscr.refresh()
                stdscr.getch()
                stdscr.clear()
        except Exception as e:
            stdscr.addstr(1, 0, f"En feil oppstod: {e}",
                          curses.color_pair(4))
            stdscr.refresh()
            stdscr.getch()
            stdscr.clear()
