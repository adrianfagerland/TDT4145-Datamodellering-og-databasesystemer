import sqlite3
import interface
import curses


def handle(conn: sqlite3.Connection, choice, stdscr):
    functions = {1: get_togruter_by_stasjon_and_day, 2: search_togruter,
                 3: register_kunde, 4: find_and_buy_billetter, 5: get_kunde_reise_info}

    functions[choice](conn, stdscr)

# c) Hent togruter som er innom en gitt stasjon på en gitt ukedag
def get_togruter_by_stasjon_and_day(conn: sqlite3.Connection, stdscr: curses.window):
    cursor = conn.cursor()
    stasjon = interface.input_stasjon(cursor, stdscr)
    ukedag = interface.input_ukedag(stdscr)

    query = f"""
        SELECT t1.TogruteID, t1.Stasjon AS EndStasjon, t2.Ankomst AS CurrentStasjonAnkomst, t2.Avgang AS CurrentStasjonAvgang
        FROM Togrutetabell t1
        INNER JOIN   ON t1.TogruteID = t2.TogruteID
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


    for idx, row in enumerate(rows):
        if row[1].lower() == stasjon:
            result_row = f"{row[0]:<{togrute_id_width}}{row[1]:<{endestasjon_width}}{row[2]:<{avgang_ankomst_width}}"
        else:
            result_row = f"{row[0]:<{togrute_id_width}}{row[1]:<{endestasjon_width}}{row[3]:<{avgang_ankomst_width}}"
        stdscr.addstr(idx + 3, 0, result_row, curses.color_pair(3))

    stdscr.refresh()

    stdscr.getch()  # Wait for user to press a key before returning to the menu







































# d) Søk etter togruter mellom en startstasjon og en sluttstasjon på en gitt dato og tidspunkt.
#    Resultatet inkludere reiser samme dag fra og med tidspunktet og reiser neste dag. 
#    Resultatet skal være sortert etter avgangstidspunkt.

def search_togruter(conn: sqlite3.Connection, stdscr: curses.window):
    cursor = conn.cursor()
    AvreiseStasjon = interface.input_stasjon(cursor, stdscr)
    AnkomstStasjon = interface.input_stasjon(cursor, stdscr)
    Dato = interface.input_dato(cursor, stdscr)
    Tid = interface.input_klokkeslett(cursor, stdscr)

    query = f"""
            SELECT tr.TogruteID, start.Stasjon AS AvreiseStasjon, 
                tgf.Togruteforekomstdato AS AvreiseDato, start.Avgang AS AvreiseTid, 
                slutt.Stasjon AS AnkomstStasjon, slutt.Ankomst AS AnkomstTid 
            FROM Togrute tr 
            JOIN Togrutetabell start ON tr.TogruteID = start.TogruteID 
            JOIN Togrutetabell slutt ON tr.TogruteID = slutt.TogruteID 
            JOIN Togruteforekomst tgf ON tr.TogruteID = tgf.Rute 
            WHERE start.Stasjon = ? AND slutt.Stasjon = ? 
                AND tgf.Togruteforekomstdato BETWEEN ? AND DATEADD(day, 1, ?) 
            ORDER BY AvreiseDato, AvreiseTid ASC;
            """

    params = (AvreiseStasjon, AnkomstStasjon, Dato, Tid,)
    cursor.execute(query, params)

    ### Skriver resultattabellen i terminalen ###
    stdscr.clear()
    rows = cursor.fetchall()

    if rows:
        TogruteID_width      =  max(max(row[0], len('TogruteID')) for row in rows) + 6
        AvreiseStasjon_width =  max(max(row[1], len('AvreiseStasjon'), len(AvreiseStasjon)) for row in rows) + 6
        AvreiseDato_width    =  max(max(row[2], len('AvreiseDato')) for row in rows) + 6
        AvreiseTid_width     =  max(max(row[3], len('AvreiseTid')) for row in rows) + 6
        AnkomstStasjon_width =  max(max(row[4], len('AnkomstStasjon'), len(AnkomstStasjon)) for row in rows) + 6
        AnkomstDato_width    =  max(max(row[5], len('AnkomstDato')) for row in rows) + 6
        AnkomstTid_width     =  max(max(row[5], len('AnkomstDato')) for row in rows) + 6

        header = f"""{'TogruteID':<{TogruteID_width}}
                     {'AvreiseStasjon':<{AvreiseStasjon_width}}
                     {'AvreiseDato':<{AvreiseDato_width}}
                     {'AvreiseTid':<{AvreiseTid_width}}
                     {'AnkomstStasjon':<{AnkomstStasjon_width}}
                     {'AnkomstDato':<{AnkomstDato_width}}
                     {'AnkomstTid':<{AnkomstTid_width}}"""
        stdscr.addstr(0, 0, header, curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(1, 0, "-" * (len(header)))

        for idx, row in enumerate(rows):
            result_row = f"""{row[0]:<{TogruteID_width}}
                             {row[1]:<{AvreiseStasjon_width}}
                             {row[2]:<{AvreiseDato_width}}
                             {row[3]:<{AvreiseTid_width}}
                             {row[4]:<{AnkomstStasjon_width}}
                             {row[5]:<{AnkomstDato_width}}
                             {row[6]:<{AnkomstTid_width}}"""
            stdscr.addstr(idx + 3, 0, result_row, curses.color_pair(3))

        stdscr.refresh()
        stdscr.getch()
    else:
        stdscr.addstr(0, 0, "Ingen resultater", curses.color_pair(2))
        stdscr.refresh()
        stdscr.getch()








































# e) Registrer en ny kunde i kunderegisteret
def register_kunde(conn: sqlite3.Connection, stdscr: curses.window):
    cursor = conn.cursor()
    navn = interface.input_kundenavn(stdscr)
    epost = interface.input_epost(cursor, stdscr)
    mobilnummer = interface.input_mobilnummer(cursor, stdscr)
    kundenummer = interface.get_kundenummer(cursor)
    stdscr.clear()
    cursor.execute("INSERT INTO Kunde (Kundenummer, Kundenavn, Epostadresse, Mobilnummer) VALUES (?, ?, ?, ?)", (kundenummer, navn, epost, mobilnummer))
    conn.commit()
    # Skriv ut resultatene

    if cursor.rowcount == 1:
        #kundenummer = cursor.execute("SELECT (Kundenummer) FROM Kunde;")
        stdscr.clear()
        stdscr.addstr(f"""Kunde registrert!
        Kundenavn: {navn}
        Epostadresse: {epost}
        Mobilnummer: {mobilnummer}
        Kundenummer: {kundenummer}
        """)  
    else :
        stdscr.clear()
        stdscr.addstr("Noe gikk galt. Prøv igjen")

    stdscr.getch()  # Wait for user to press a key before returning to the menu

# g) Finn ledige billetter for en oppgitt strekning på en ønsket togrute og kjøp billetter
def find_and_buy_billetter(conn, kunde, togrute, reisedato, startstasjon, sluttstasjon, antall_billetter):
    pass
    # Implementer SQL-spørringen og returner resultatene


# h) Finn all informasjon om kjøp for fremtidige reiser for en gitt kunde
def get_kunde_reise_info(conn, kunde_id):
    
    pass
