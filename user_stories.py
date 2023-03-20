import sqlite3
import interface
import curses


def handle(cursor, choice, stdscr):
    functions = {1: get_togruter_by_stasjon_and_day, 2: search_togruter,
                 3: register_kunde, 4: find_and_buy_billetter, 5: get_kunde_reise_info}

    functions[choice](cursor, stdscr)

# c) Hent togruter som er innom en gitt stasjon på en gitt ukedag
def get_togruter_by_stasjon_and_day(cursor: sqlite3.Cursor, stdscr: curses.window):
    stasjon = interface.input_stasjon(cursor, stdscr)
    ukedag = interface.input_ukedag(stdscr)

    query = f"""
        SELECT t1.TogruteID, t1.Stasjon AS EndStasjon, t2.Ankomst AS CurrentStasjonAnkomst, t2.Avgang AS CurrentStasjonAvgang
        FROM Togrutetabell t1
        INNER JOIN Togrutetabell t2 ON t1.TogruteID = t2.TogruteID
        WHERE t1.Stasjonnummer = (
            SELECT MAX(Stasjonnummer)
            FROM Togrutetabell
            WHERE TogruteID = t1.TogruteID
        )
        AND LOWER(t2.Stasjon) = LOWER(?)
        AND EXISTS (
            SELECT 1
            FROM Togrute
            WHERE TogruteID = t1.TogruteID AND {ukedag} = 1
        )
    """
    cursor.execute(query, (stasjon,))

    # Skriv ut resultatene
    stdscr.clear()
    rows = cursor.fetchall()
    
    if rows:
        togrute_id_width = max(max(len(row[0]), len('TogruteID')) for row in rows) + 6
        endestasjon_width = max(max(len(row[1]), len(stasjon), len('Endestasjon')) for row in rows) + 6
        avgang_ankomst_width = max(max(len(row[2]), len(row[3]), len('Avgang/Ankomst')) for row in rows) + 6

        header = f"{'TogruteID':<{togrute_id_width}}{'Endestasjon':<{endestasjon_width}}{'Avgang/Ankomst':<{avgang_ankomst_width}}"
        stdscr.addstr(0, 0, header, curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(1, 0, "-" * (len(header)))


    # TODO fix avgang/ankomst
    for idx, row in enumerate(rows):
        if row[1].lower() == stasjon:
            result_row = f"{row[0]:<{togrute_id_width}}{row[1]:<{endestasjon_width}}{row[2]:<{avgang_ankomst_width}}"
        else:
            result_row = f"{row[0]:<{togrute_id_width}}{row[1]:<{endestasjon_width}}{row[3]:<{avgang_ankomst_width}}"
        stdscr.addstr(idx + 3, 0, result_row, curses.color_pair(3))

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
