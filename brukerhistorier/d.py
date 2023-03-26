import sqlite3
import curses
import datetime

import interface

# d) Søk etter togruter mellom en startstasjon og en sluttstasjon på en gitt dato og tidspunkt.
#    Resultatet skal inkludere reiser samme dag (fra og med tidspunktet) og reiser neste dag.
#    Resultatet skal være sortert etter avgangstidspunkt.

# Vi har antatt ingen togreise vil gå over 3 dager, da norges lengste teoretiske togreise vil vare i rundt 18 timer


def get_togruter_between_stations_for_date(conn: sqlite3.Connection, stdscr: curses.window):
    cursor = conn.cursor()
    AvreiseStasjon = interface.input_avreisestasjon(cursor, stdscr)
    # Hva med hvis avreise stasjon==ankomst stasjon?
    AnkomstStasjon = interface.input_ankomststasjon(
        cursor, stdscr, AvreiseStasjon)
    Dato = interface.input_dato(stdscr)
    Tid = interface.input_klokkeslett(stdscr)
    DatoPlusEnDag = (datetime.datetime.strptime(
        Dato, '%Y-%m-%d') + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    DatoMinusEnDag = (datetime.datetime.strptime(
        Dato, '%Y-%m-%d') - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    query = f"""
            SELECT tr.TogruteID, start.Stasjon AS AvreiseStasjon, 
                tgf.Togruteforekomstdato AS AvreiseDato, start.Avgang AS AvreiseTid, 
                slutt.Stasjon AS AnkomstStasjon, slutt.Ankomst AS AnkomstTid
            FROM Togrute tr 
            JOIN Togrutetabell start ON tr.TogruteID = start.TogruteID 
            JOIN Togrutetabell slutt ON tr.TogruteID = slutt.TogruteID 
            JOIN Togruteforekomst tgf ON tr.TogruteID = tgf.Rute 
            WHERE LOWER(start.Stasjon) = LOWER(?) AND LOWER(slutt.Stasjon) = LOWER(?) 
                AND (tgf.Togruteforekomstdato = ? OR tgf.Togruteforekomstdato = ? OR (tgf.Togruteforekomstdato = ? AND SUBSTR(start.avgang, -2) == "+1"))
                AND (start.avgang >= ? OR tgf.Togruteforekomstdato = ?)
                AND (start.stasjonnummer < slutt.stasjonnummer)
            ORDER BY AvreiseDato, AvreiseTid ASC;
            """

    params = (AvreiseStasjon, AnkomstStasjon, Dato,
              DatoPlusEnDag, DatoMinusEnDag, Tid, DatoPlusEnDag)
    cursor.execute(query, params)

    ### Skriver resultattabellen i terminalen ###
    stdscr.clear()
    return cursor.fetchall()


def search_togruter_between_stations_for_date(conn: sqlite3.Connection, stdscr: curses.window, selectable=False):
    rows = get_togruter_between_stations_for_date(conn, stdscr)
    if rows:
        return show_train_routes_between_stations_for_date(stdscr, rows, selectable)
    else:
        stdscr.addstr(0, 0, "Ingen resultater", curses.color_pair(2))
        stdscr.refresh()
        stdscr.getch()
        return []


def show_train_routes_between_stations_for_date(stdscr: curses.window, rows, selectable):
    stdscr.clear()
    curses.curs_set(0)

    TogruteID_width = max(
        max(len(row[0]), len('TogruteID')) for row in rows) + 6
    AvreiseDato_width = max(
        max(len(row[2]), len('AvreiseDato')) for row in rows) + 6
    AvreiseTid_width = max(
        max(len(row[3]), len('AvreiseTid')) for row in rows) + 6
    AnkomstDato_width = max(
        max(len(row[2]), len('Ankomstdato')) for row in rows) + 6
    AnkomstTid_width = max(
        max(len(row[5]), len('AnkomstTid')) for row in rows)

    header = f"{'TogruteID':<{TogruteID_width}}{'Avreisedato':<{AvreiseDato_width}}{'Avreisetid':<{AvreiseTid_width}}{'Ankomstdato':<{AnkomstDato_width}}{'Ankomsttid':<{AnkomstTid_width}}"
    stdscr.addstr(0, 0, f"Togruter mellom {rows[0][1]} og {rows[0][4]}:", curses.color_pair(
        2) | curses.A_BOLD)
    stdscr.addstr(2, 0, header, curses.color_pair(1))
    stdscr.addstr(3, 0, "-" * (len(header)))

    selected_row = 0

    for idx, row in enumerate(rows):
        AnkomstDato = (datetime.datetime.strptime(
            row[2], '%Y-%m-%d') + datetime.timedelta(days=int(row[5].split("+")[1] if "+" in row[5] else 0))).strftime('%Y-%m-%d')
        AvreiseDato = (datetime.datetime.strptime(
            row[2], '%Y-%m-%d') + datetime.timedelta(days=int(row[3].split("+")[1] if "+" in row[3] else 0))).strftime('%Y-%m-%d')
        result_row = f"{row[0]:<{TogruteID_width}}{AvreiseDato:<{AvreiseDato_width}}{row[3].split('+')[0]:<{AvreiseTid_width}}{AnkomstDato:<{AnkomstDato_width}}{row[5].split('+')[0]:<{AnkomstTid_width}}"
        stdscr.addstr(idx + 4, 0, result_row, curses.color_pair(3))

        if selectable and idx == selected_row:
            stdscr.addstr(idx + 4, 0, result_row,
                          curses.color_pair(3) | curses.A_REVERSE)
        else:
            stdscr.addstr(idx + 4, 0, result_row, curses.color_pair(3))

    if selectable:
        while True:
            key = stdscr.getch()
            if key == curses.KEY_UP and selected_row > 0:
                selected_row -= 1
            elif key == curses.KEY_DOWN and selected_row < len(rows) - 1:
                selected_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                return rows[selected_row]

            stdscr.clear()
            stdscr.addstr(0, 0, f"Togruter mellom {rows[0][1]} og {rows[0][4]}:", curses.color_pair(
                2) | curses.A_BOLD)
            stdscr.addstr(2, 0, header, curses.color_pair(1))
            stdscr.addstr(3, 0, "-" * (len(header)))
            for idx, row in enumerate(rows):
                AnkomstDato = (datetime.datetime.strptime(
                    row[2], '%Y-%m-%d') + datetime.timedelta(days=int(row[5].split("+")[1] if "+" in row[5] else 0))).strftime('%Y-%m-%d')
                AvreiseDato = (datetime.datetime.strptime(
                    row[2], '%Y-%m-%d') + datetime.timedelta(days=int(row[3].split("+")[1] if "+" in row[3] else 0))).strftime('%Y-%m-%d')
                result_row = f"{row[0]:<{TogruteID_width}}{AvreiseDato:<{AvreiseDato_width}}{row[3].split('+')[0]:<{AvreiseTid_width}}{AnkomstDato:<{AnkomstDato_width}}{row[5].split('+')[0]:<{AnkomstTid_width}}"
                if idx == selected_row:
                    stdscr.addstr(idx + 4, 0, result_row,
                                  curses.color_pair(3) | curses.A_REVERSE)
                else:
                    stdscr.addstr(idx + 4, 0, result_row, curses.color_pair(3))
            stdscr.refresh()
    else:
        stdscr.getch()
        curses.curs_set(0)
        stdscr.refresh()
        return [None]*6
