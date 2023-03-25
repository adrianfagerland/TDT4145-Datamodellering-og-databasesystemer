import sqlite3
import curses
import interface

# h) Finn all informasjon om kjøp for fremtidige reiser for en gitt kunde

#For en bruker skal man kunne finne all informasjon om de kjøpene hen har gjort for fremtidige reiser.


def get_kunde_reise_info(conn: sqlite3.Connection, stdscr: curses.window):
    cursor = conn.cursor()
    kunde_id = interface.input_kundenummer(cursor, stdscr)
    cursor.execute("SELECT * FROM Kunde WHERE Kundenummer = ?", (kunde_id,))
    kunde = cursor.fetchone()
    if kunde is None:
        stdscr.clear()
        stdscr.addstr("Fant ingen kunde med det kundenummeret")
        stdscr.getch()
        return
    cursor.execute("SELECT * FROM Billett WHERE Kundenummer = ?", (kunde_id,))
    billetter = cursor.fetchall()
    if billetter is None:
        stdscr.clear()
        stdscr.addstr("Fant ingen billetter for kunde med det kundenummeret")
        stdscr.getch()
        return
    stdscr.clear()
    stdscr.addstr(f"""Kunde: {kunde[1]}
    Epost: {kunde[2]}
    Mobilnummer: {kunde[3]}
    """)
    for billett in billetter:
        cursor.execute("SELECT * FROM Togt WHERE Togtnummer = ?", (billett[1],))
        togt = cursor.fetchone()
        cursor.execute("SELECT * FROM TogtRute WHERE Togtnummer = ?", (billett[1],))
        togrute = cursor.fetchone()
        cursor.execute("SELECT * FROM TogtRuteStasjon WHERE Togtrutenummer = ?", (togrute[0],))
        togrutestasjoner = cursor.fetchall()
        cursor.execute("SELECT * FROM Stasjon WHERE Stasjonskode = ?", (togrutestasjoner[0][1],))
        startstasjon = cursor.fetchone()
        cursor.execute("SELECT * FROM Stasjon WHERE Stasjonskode = ?", (togrutestasjoner[-1][1],))
        sluttstasjon = cursor.fetchone()
        stdscr.addstr(f"""Billett: {billett[0]}
        Togt: {togt[0]}
        Reisedato: {billett[2]}
        Startstasjon: {startstasjon[1]}
        Sluttstasjon: {sluttstasjon[1]}
        Antall billetter: {billett[3]}
        """)
    stdscr.getch()
