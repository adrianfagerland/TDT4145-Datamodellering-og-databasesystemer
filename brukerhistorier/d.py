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
    DatoPlusEnDag = (datetime.strptime(Dato, '%Y-%m-%d') + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

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
            ORDER BY AvreiseDato, AvreiseTid ASC;
            """
## Brukte denne DATEADD(day, 1, ?) etter And i nest siste linje.

    params = (AvreiseStasjon, AnkomstStasjon, Dato, DatoPlusEnDag,)
    cursor.execute(query, params)

    ### Skriver resultattabellen i terminalen ###
    stdscr.clear()
    rows = cursor.fetchall()

    if rows:
        TogruteID_width      =  max(max(len(row[0]), len('TogruteID')) for row in rows) + 6
        AvreiseStasjon_width =  max(max(len(row[1]), len('AvreiseStasjon'), len(AvreiseStasjon)) for row in rows) + 6
        AvreiseDato_width    =  max(max(len(row[2]), len('AvreiseDato')) for row in rows) + 6
        AvreiseTid_width     =  max(max(len(row[3]), len('AvreiseTid')) for row in rows) + 6
        AnkomstStasjon_width =  max(max(len(row[4]), len('AnkomstStasjon'), len(AnkomstStasjon)) for row in rows) + 6
#        AnkomstDato_width    =  max(max(len(row[5]), len('AnkomstDato')) for row in rows) + 6 skal egentlig v're row[5], men tar den vekk midlertidig
        AnkomstTid_width     =  max(max(len(row[5]), len('AnkomstTid')) for row in rows) + 6

        header = f"""{'TogruteID':<{TogruteID_width}}
                     {'AvreiseStasjon':<{AvreiseStasjon_width}}
                     {'AvreiseDato':<{AvreiseDato_width}}
                     {'AvreiseTid':<{AvreiseTid_width}}
                     {'AnkomstStasjon':<{AnkomstStasjon_width}}

                     {'AnkomstTid':<{AnkomstTid_width}}"""# {'AnkomstDato':<{AnkomstDato_width}} skal egentlig staa i den tomme linjen.
        stdscr.addstr(0, 0, header, curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(1, 0, "-" * (len(header)))

        for idx, row in enumerate(rows):
            if row[1].lower() == stasjon:
                result_row = f"""{row[0]:<{TogruteID_width}}
                                 {row[1]:<{AvreiseStasjon_width}}
                                 {row[2]:<{AvreiseDato_width}}
                                 {row[3]:<{AvreiseTid_width}}
                                 {row[4]:<{AnkomstStasjon_width}}
                                 
                                 {row[5]:<{AnkomstTid_width}}"""
            else:
                result_row = f"""{row[0]:<{TogruteID_width}}
                             {row[1]:<{AvreiseStasjon_width}}
                             {row[2]:<{AvreiseDato_width}}
                             {row[3]:<{AvreiseTid_width}}
                             {row[4]:<{AnkomstStasjon_width}}
                             
                             {row[5]:<{AnkomstTid_width}}"""#{row[5]:<{AnkomstDato_width}} skal egentlig staa i den tomme linjen.
            stdscr.addstr(idx + 3, 0, result_row, curses.color_pair(3))

        stdscr.refresh()
        stdscr.getch()
    else:
        stdscr.addstr(0, 0, "Ingen resultater", curses.color_pair(2))
        stdscr.refresh()
        stdscr.getch()
