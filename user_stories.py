import interface
import curses


def handle(cursor, choice, stdscr):
    functions = {1: get_togruter_by_stasjon_and_day, 2: search_togruter,
                 3: register_kunde, 4: find_and_buy_billetter, 5: get_kunde_reise_info}
    
    functions[choice](cursor, stdscr)

# c) Hent togruter som er innom en gitt stasjon på en gitt ukedag
def get_togruter_by_stasjon_and_day(cursor, stdscr):
    stasjon = interface.input_stasjon(cursor, stdscr)
    ukedag = interface.input_ukedag(stdscr)

    query = f"""
        SELECT TogruteID, Operatør, Togoppsett
        FROM Togrute
        WHERE {ukedag} = 1
        AND TogruteID IN (
            SELECT TogruteID
            FROM Togrutetabell
            WHERE Stasjon = ?
        )
    """

    # Utfør spørringen og hent resultatene
    cursor.execute(query, (stasjon,))

    # Skriv ut resultatene
    stdscr.clear()
    result_header = f"Togruter som er innom stasjonen {stasjon} på {ukedag.capitalize()}:"
    stdscr.addstr(0, 0, result_header, curses.color_pair(1) | curses.A_BOLD)
    stdscr.refresh()

    rows = cursor.fetchall()
    for idx, row in enumerate(rows):
        result_row = f"TogruteID: {row[0]}, Operatør: {row[1]}, Togoppsett: {row[2]}"
        stdscr.addstr(idx + 1, 0, result_row, curses.color_pair(3))
        stdscr.refresh()

    stdscr.getch()  # Wait for user to press a key before returning to the menu
    
# d) Søk etter togruter mellom en startstasjon og en sluttstasjon
def search_togruter(conn, startstasjon, sluttstasjon, dato, klokkeslett):
    pass
    # Implementer SQL-spørringen og returner resultatene

# e) Registrer en ny kunde i kunderegisteret
def register_kunde(conn, navn, epost, mobilnummer):
    pass
    # Implementer SQL-spørringen og returner resultatene

# g) Finn ledige billetter for en oppgitt strekning på en ønsket togrute og kjøp billetter
def find_and_buy_billetter(conn, kunde, togrute, reisedato, startstasjon, sluttstasjon, antall_billetter):
    pass
    # Implementer SQL-spørringen og returner resultatene

# h) Finn all informasjon om kjøp for fremtidige reiser for en gitt kunde
def get_kunde_reise_info(conn, kunde_id):
    pass
    # Implementer SQL-spørringen og returner resultatene