import sqlite3
import curses

import interface

# d) Søk etter togruter mellom en startstasjon og en sluttstasjon


def search_togruter(conn: sqlite3.Connection, stdscr: curses.window):
    cursor = conn.cursor()
    print("Angi en startstasjon: \n")
    startstasjon = interface.input_stasjon(cursor, stdscr)
    print("\nAngi en sluttstasjon: \n")
    sluttstasjon = interface.input_stasjon(cursor, stdscr)
    print("\nAngi en dato: \n")
    dato = interface.input_date()
    print("\Angi et klokkeslett: \n")
    klokkeslett = interface.input_time(conn, stdscr)

    query = f"""
        SELECT t1.TogruteID, t1.Stasjon AS EndStasjon, t2.Ankomst AS CurrentStasjonAnkomst, t2.Avgang AS CurrentStasjonAvgang
        """
