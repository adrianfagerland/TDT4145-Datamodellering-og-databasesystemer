import sqlite3
import curses

import interface

# h) Finn all informasjon om kjøp for fremtidige reiser for en gitt kunde.
#    Tabellen vil se slik ut: KundeID, TogruteID, AvreiseDato, AvreiseTid, AnkomstDato, [ulike typer passasjerer?]

def get_kunde_reise_info(conn: sqlite3.Connection, stdscr: curses.window):
    cursor = conn.cursor()
    kunde_id = interface.input_kundenummer(cursor, stdscr)

    query = """

            """
    
    params = (kunde_id,)
    cursor.execute(query, params)

    ### Skriver resultattabellen i terminalen ###
    stdscr.clear()
    rows: list[str] = cursor.fetchall()

    if rows: #Her er det foreløpig bare dilldall. Erstatt all kode.
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
        stdscr.addstr(0, 0, "Ingen fremtidige reiser", curses.color_pair(2))
        stdscr.refresh()
        stdscr.getch()
