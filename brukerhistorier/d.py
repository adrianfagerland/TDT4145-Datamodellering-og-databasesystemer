import sqlite3
import curses
import datetime

import interface

# d) Søk etter togruter mellom en startstasjon og en sluttstasjon på en gitt dato og tidspunkt.
#    Resultatet inkludere reiser samme dag fra og med tidspunktet og reiser neste dag.
#    Resultatet skal være sortert etter avgangstidspunkt.


def search_togruter(conn: sqlite3.Connection, stdscr: curses.window):
    cursor = conn.cursor()
    AvreiseStasjon = interface.input_stasjon(cursor, stdscr)
    AnkomstStasjon = interface.input_stasjon(cursor, stdscr)
    Dato = interface.input_dato(cursor, stdscr)
    Tid = interface.input_klokkeslett(cursor, stdscr)
    DatoPlusEnDag = (datetime.datetime.strptime(
        Dato, '%Y-%m-%d') + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    query = f"""
            SELECT tr.TogruteID, start.Stasjon AS AvreiseStasjon, 
                tgf.Togruteforekomstdato AS AvreiseDato, start.Avgang AS AvreiseTid, 
                slutt.Stasjon AS AnkomstStasjon, slutt.Ankomst AS AnkomstTid
            FROM Togrute tr 
            JOIN Togrutetabell start ON tr.TogruteID = start.TogruteID 
            JOIN Togrutetabell slutt ON tr.TogruteID = slutt.TogruteID 
            JOIN Togruteforekomst tgf ON tr.TogruteID = tgf.Rute 
            WHERE LOWER(start.Stasjon) = LOWER(?) AND LOWER(slutt.Stasjon) = LOWER(?) 
                AND (tgf.Togruteforekomstdato = ? OR tgf.Togruteforekomstdato = ?)
                AND (start.avgang >= ? OR tgf.Togruteforekomstdato = ?)
            ORDER BY AvreiseDato, AvreiseTid ASC;
            """
# Brukte denne DATEADD(day, 1, ?) etter And i nest siste linje.

    params = (AvreiseStasjon, AnkomstStasjon, Dato,
              DatoPlusEnDag, Tid, DatoPlusEnDag,)
    cursor.execute(query, params)

    ### Skriver resultattabellen i terminalen ###
    stdscr.clear()
    rows: list[str] = cursor.fetchall()

    if rows:
        TogruteID_width = max(
            max(len(row[0]), len('TogruteID')) for row in rows) + 6
        AvreiseDato_width = max(
            max(len(row[2]), len('AvreiseDato')) for row in rows) + 6
        AvreiseTid_width = max(
            max(len(row[3]), len('AvreiseTid')) for row in rows) + 6
        AnkomstDato_width = max(
            max(len(row[2]), len('Ankomstdato')) for row in rows) + 6
        AnkomstTid_width = max(
            max(len(row[5]), len('AnkomstTid')) for row in rows) + 6

        header = f"{'TogruteID':<{TogruteID_width}}{'Avreisedato':<{AvreiseDato_width}}{'Avreisetid':<{AvreiseTid_width}}{'Ankomstdato':<{AnkomstDato_width}}{'Ankomsttid':<{AnkomstTid_width}}"
        stdscr.addstr(0, 0, f"Togruter mellom {rows[0][1]} og {rows[0][4]}:", curses.color_pair(
            2) | curses.A_BOLD)
        stdscr.addstr(2, 0, header, curses.color_pair(1))
        stdscr.addstr(3, 0, "-" * (len(header)))

        for idx, row in enumerate(rows):
            AnkomstDato = (datetime.datetime.strptime(
                row[2], '%Y-%m-%d') + datetime.timedelta(days=int(row[5].split("+")[1] if "+" in row[5] else 0))).strftime('%Y-%m-%d')
            result_row = f"{row[0]:<{TogruteID_width}}{row[2]:<{AvreiseDato_width}}{row[3]:<{AvreiseTid_width}}{AnkomstDato:<{AnkomstDato_width}}{row[5].split('+')[0]:<{AnkomstTid_width}}"
            stdscr.addstr(idx + 4, 0, result_row, curses.color_pair(3))

        curses.curs_set(0)
        stdscr.refresh()
        stdscr.getch()
    else:
        stdscr.addstr(0, 0, "Ingen resultater", curses.color_pair(2))
        stdscr.refresh()
        stdscr.getch()
