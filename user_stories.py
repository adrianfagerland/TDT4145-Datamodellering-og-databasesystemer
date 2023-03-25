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


    for idx, row in enumerate(rows):
        if row[1].lower() == stasjon:
            result_row = f"{row[0]:<{togrute_id_width}}{row[1]:<{endestasjon_width}}{row[2]:<{avgang_ankomst_width}}"
        else:
            result_row = f"{row[0]:<{togrute_id_width}}{row[1]:<{endestasjon_width}}{row[3]:<{avgang_ankomst_width}}"
        stdscr.addstr(idx + 3, 0, result_row, curses.color_pair(3))

    stdscr.refresh()

    stdscr.getch()  # Wait for user to press a key before returning to the menu


# d) Søk etter togruter mellom en startstasjon og en sluttstasjon

#def search_togruter(conn, startstasjon, sluttstasjon, dato, klokkeslett):
def search_togruter(cursor: sqlite3.Cursor, stdscr: curses.window):

    pass
    # Implementer SQL-spørringen og returner resultatene


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
def find_and_buy_billetter(conn: sqlite3.Connection, stdscr: curses.window):
    cursor = conn.cursor()
    #kunde = interface.find_kundenummer(cursor, stdscr) #implementert
    togrute = interface.input_togrute(cursor, stdscr) #implementert
    reisedato = interface.input_reisedato(cursor, stdscr) #implementert
    startstasjon = interface.input_startstasjon(cursor, stdscr, togrute)
    sluttstasjon = interface.input_sluttstasjon(cursor, stdscr, togrute, startstasjon) 
    billettID = interface.make_billettID(cursor) #implementert
    kundeordrenummer = interface.make_kundeordrenummer(cursor) #implementert
    kjopsdato = interface.get_kjopsdato() #implementert
    billetttype = interface.velg_billettype(cursor, stdscr)
    antallBilletter = interface.input_billetter(cursor, stdscr) #implementert
    if billetttype == "sete":
        cursor.execute("""
        WITH Sittevogner AS (
        SELECT Vognnummer, AvType
        FROM Vogn
        WHERE Togoppsett = (
            SELECT Togoppsett
            FROM Togrute
            WHERE TogruteID = ? 
        )
        AND AvType IN (
            SELECT Vogntypenavn
            FROM Vogntype
            WHERE Type = 'Sitte'
        )
    ),
    OpptatteSeter AS (
        SELECT Setenummer, Vogntypenavn, Vognnummer
        FROM Setebillett
        JOIN Billett ON Setebillett.BillettID = Billett.BillettID
        WHERE Ordrenummer IN (
            SELECT Kundeordrenummer
            FROM Kundeordre
            WHERE Rute = ? AND Reisedato = ? AND 
        ) AND (
            (Billett.Påstigning < ? AND Billett.Avstigning > ?)
            OR (Billett.Påstigning >= ? AND Billett.Påstigning < ?)
        )
    ),
    LedigeSeter AS (
        SELECT Setenummer, Sittetypenavn, Radnummer, Vognnummer
        FROM Sete
        JOIN Sittevogner ON Sete.Sittetypenavn = Sittevogner.AvType
        WHERE (Setenummer, Sittetypenavn) NOT IN (
            SELECT Setenummer, Vogntypenavn
            FROM OpptatteSeter
        )
    )
    SELECT * FROM LedigeSeter;
    """,
    (togrute, togrute, reisedato, startstasjon, startstasjon, startstasjon, sluttstasjon))
    if billetttype == "seng":
        cursor.execute("""
        WITH Sengevogner AS (
        SELECT Vognnummer, AvType
        FROM Vogn
        WHERE Togoppsett = (
            SELECT Togoppsett
            FROM Togrute
            WHERE TogruteID = ?
        )
        AND AvType IN (
            SELECT Vogntypenavn
            FROM Vogntype
            WHERE Type = 'Senge'
        )
    ),
    OpptatteKupe AS (
        SELECT Kupenr, Vognnummer
        FROM Sengeplassbillett
        JOIN Billett ON Sengeplassbillett.BillettID = Billett.BillettID
        WHERE Ordrenummer IN (
            SELECT Kundeordrenummer
            FROM Kundeordre
            WHERE Rute = ? AND Reisedato = ? AND Vogn
        )
    ),
    LedigeSenge AS (
        SELECT Sengeplassnummer, Sengetypenavn, Kupenr, Vognnummer
        FROM Sengeplass
        JOIN Sengevogner ON Sengeplass.Sengetypenavn = Sengevogner.AvType
        WHERE (Kupenr, Vognnummer) NOT IN (
            SELECT Kupenr, Vognnummer
            FROM OpptatteKupe
        )
    )
    SELECT * FROM LedigeSenge;
    """)
    tilgjengelig = [row[0] for row in cursor.fetchall()]
    prompt = "Her er " + str(antallBilletter) + " tilgjengelige billetter:"
    for i in range(antallBilletter):
        prompt += "\nTest" + str(tilgjengelig[1])
    

    stdscr.getch()  # Wait for user to press a key before returning to the menu


# h) Finn all informasjon om kjøp for fremtidige reiser for en gitt kunde
def get_kunde_reise_info(conn, kunde_id):
    
    pass
