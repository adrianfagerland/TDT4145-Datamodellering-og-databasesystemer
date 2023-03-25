import datetime
import sqlite3
import curses

import interface
from datetime import datetime

# g) Finn ledige billetter for en oppgitt strekning på en ønsket togrute og kjøp billetter


def find_and_buy_billetter(conn: sqlite3.Connection, stdscr: curses.window):
    cursor = conn.cursor()
    togrute = interface.input_togrute(cursor, stdscr)
    reisedato = interface.input_reisedato(cursor, stdscr)  
    startstasjon = interface.input_startstasjon(cursor, stdscr, togrute)
    sluttstasjon = interface.input_sluttstasjon(cursor, stdscr, togrute, startstasjon)
    billettID = interface.make_billettID(cursor)  
    kundeordrenummer = interface.make_kundeordrenummer(cursor)  
    #kjopsdato = interface.get_kjopsdato()  
    billettype = interface.velg_billettype(cursor, stdscr)
    vognnummer = interface.input_vognnummer(cursor, stdscr, togrute, billettype)
    if billettype == "sete":
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
                AND Vognnummer = ?
            ),
            OpptatteSeter AS (
                SELECT Setenummer, Vogntypenavn, Vognnummer
                FROM Setebillett
                JOIN Billett ON Setebillett.BillettID = Billett.BillettID
                WHERE Ordrenummer IN (
                    SELECT Kundeordrenummer
                    FROM Kundeordre
                    WHERE Rute = ? AND Reisedato = ? AND Vognnummer = ?
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
        (togrute, vognnummer, togrute, reisedato, vognnummer, startstasjon, startstasjon, startstasjon, sluttstasjon))

    if billettype == "seng":
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
            WHERE Rute = ? AND Reisedato = ?
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
    
    antallBilletter = interface.input_billetter(cursor, stdscr)  
    while True: 
        results = cursor.fetchall()    
        billettPrint = ""
        antallTilgjengeligeBilletter = 0
        for row in results:
            antallTilgjengeligeBilletter += 1
            setenummer = row[0]
            radnummer = row[2]
            vognnummer = row[3]
            billettPrint += (f"Vognnummer: {vognnummer}, Setenummer: {setenummer}, Radnummer: {radnummer}\n")
            if antallBilletter == antallTilgjengeligeBilletter: 
                break
        if antallBilletter == antallTilgjengeligeBilletter: 
                break
        antallBilletter = interface.input_prøvNyeBilletter(cursor, stdscr)  
    prompt = "Her er " + str(antallTilgjengeligeBilletter) + " tilgjengelige billetter:\n"
    stdscr.clear
    stdscr.addstr(0, 0, prompt + billettPrint + "\nTrykk enter for å komme videre til innlogging for å bestille disse billettene")
    stdscr.getch()  # Wait for user to press a key before returning to the menu
    kundenummer = interface.find_kundenummer(cursor, stdscr)

    cursor.execute("""
    SELECT Togoppsett
    FROM Togrute
    WHERE TogruteID = ?
    """, (togrute,))
    togoppsett = cursor.fetchone()[0]

    kjopsdato = datetime.now().date()  # Legg til denne linjen for å få kjøpsdatoen
    kjopsdato_str = kjopsdato.strftime("%Y-%m-%d")  # Konverter kjopsdato til en streng

    kjopstidspunkt = datetime.now().time()  # Legg til denne linjen for å få kjøpstidspunktet
    kjopstidspunkt_str = kjopstidspunkt.strftime("%H:%M:%S")  # Konverter kjopstidspunkt til en streng

    endPromt = ""
    cursor.execute("""
        INSERT INTO Kundeordre (Kundeordrenummer, Kjøpsdato, Kjøpstidspunkt, Kunde, Rute, Reisedato)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (kundeordrenummer, kjopsdato_str, kjopstidspunkt_str, kundenummer, togrute, reisedato))

    for i in range(antallBilletter):
        billettID += 1
        cursor.execute("""
            INSERT INTO Billett (BillettID, Påstigning, Avstigning, Ordrenummer, Vogn, Togoppsett)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (billettID, startstasjon, sluttstasjon, kundeordrenummer, vognnummer, togoppsett))

        endPromt += "\nNy billett registrert"


        if billettype == "sete":
            cursor.execute("""
                SELECT Sittetypenavn
                FROM Sete
                WHERE Setenummer = ?
            """, (setenummer,))
            vogntypenavn = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO Setebillett (BillettID, Setenummer, Vogntypenavn)
                VALUES (?, ?, ?)
            """, (billettID, setenummer, vogntypenavn))
            conn.commit()   

        elif billettype == "seng":
            cursor.execute("""
                INSERT INTO Sengeplassbillett (BillettID, Sengeplassnummer, Kupenr, Vognnummer)
                VALUES (?, ?, ?, ?)
            """, (billettID, sengeplassnummer, kupenr, vognnummer))
            conn.commit()   
    stdscr.addstr(0, 0, endPromt)

    if cursor.rowcount == antallTilgjengeligeBilletter:
        stdscr.clear()
        stdscr.addstr(f"""Ordre registrert!
        """)
    else:
        stdscr.clear()
        stdscr.addstr("Noe gikk galt. Prøv igjen")
    stdscr.getch()  # Wait for user to press a key before returning to the menu


