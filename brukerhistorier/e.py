import sqlite3
import curses

import interface

# e) Registrer en ny kunde i kunderegisteret


def register_kunde(conn: sqlite3.Connection, stdscr: curses.window):
    cursor = conn.cursor()
    navn = interface.input_kundenavn(stdscr)
    epost = interface.input_epost(cursor, stdscr)
    mobilnummer = interface.input_mobilnummer(cursor, stdscr)
    kundenummer = interface.get_kundenummer(cursor)
    stdscr.clear()
    cursor.execute("INSERT INTO Kunde (Kundenummer, Kundenavn, Epostadresse, Mobilnummer) VALUES (?, ?, ?, ?)",
                   (kundenummer, navn, epost, mobilnummer))
    conn.commit()
    # Skriv ut resultatene

    if cursor.rowcount == 1:
        stdscr.clear()
        stdscr.addstr(f"""Kunde registrert!
        Kundenavn: {navn}
        Epostadresse: {epost}
        Mobilnummer: {mobilnummer}
        Kundenummer: {kundenummer}
        """)
    else:
        stdscr.clear()
        stdscr.addstr("Noe gikk galt. Prøv igjen")

    stdscr.getch()  # Wait for user to press a key before returning to the menu
