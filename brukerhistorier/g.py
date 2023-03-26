import datetime
import sqlite3
import curses
from datetime import datetime
import random

import interface
from .d import search_togruter_between_stations_for_date

# g) Finn ledige billetter for en oppgitt strekning på en ønsket togrute og kjøp billetter


def find_and_buy_billetter(conn: sqlite3.Connection, stdscr: curses.window):
    cursor = conn.cursor()

    togrute, startstasjon, reisedato, _, sluttstasjon, _ = search_togruter_between_stations_for_date(
        conn, stdscr, True)

    #billettID = interface.make_billettID(cursor)
    kundeordrenummer = interface.make_kundeordrenummer(cursor)
    #kjopsdato = interface.get_kjopsdato()
    billettype = interface.velg_billettype(cursor, stdscr)
    vognnummer = interface.input_vognnummer(
        cursor, stdscr, togrute, billettype)

    kjopsdato = datetime.now().date()
    kjopsdato_str = kjopsdato.strftime("%Y-%m-%d")

    kjopstidspunkt = datetime.now().time()
    kjopstidspunkt_str = kjopstidspunkt.strftime("%H:%M")

    if billettype == "sete":
        cursor.execute("""
        WITH Setevogner AS (
SELECT Vognnummer, AvType
FROM Vogn
WHERE Togoppsett = (
    SELECT Togoppsett
    FROM Togrute
    WHERE TogruteID = ? AND Vognnummer = ?
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
    JOIN Kundeordre ON Billett.Ordrenummer = Kundeordre.Kundeordrenummer
    JOIN Togrutetabell as Av ON Kundeordre.Rute = Av.TogruteID AND Billett.Avstigning = Av.Stasjon
    JOIN Togrutetabell as Pa ON Kundeordre.Rute = Pa.TogruteID AND Billett.Påstigning = Pa.Stasjon
    JOIN Togrutetabell as PaStasjon ON Kundeordre.Rute = PaStasjon.TogruteID AND PaStasjon.Stasjon = ?
    JOIN Togrutetabell as AvStasjon ON Kundeordre.Rute = AvStasjon.TogruteID AND AvStasjon.Stasjon = ?
    WHERE Kundeordre.Reisedato = ? AND Kundeordre.Rute = ?
    AND (Av.Stasjonnummer BETWEEN PaStasjon.Stasjonnummer AND AvStasjon.Stasjonnummer
        OR Pa.Stasjonnummer BETWEEN PaStasjon.Stasjonnummer AND AvStasjon.Stasjonnummer)
    AND NOT (Av.Stasjonnummer = PaStasjon.Stasjonnummer OR Pa.Stasjonnummer = AvStasjon.Stasjonnummer AND NOT (Av.Stasjonnummer = AvStasjon.Stasjonnummer AND Pa.Stasjonnummer = PaStasjon.Stasjonnummer))
    AND Billett.Vogn = ?
),
LedigeSeter AS (
    SELECT Setenummer, Sittetypenavn, Vognnummer
    FROM Sete
    JOIN Setevogner ON Sete.Sittetypenavn = Setevogner.AvType
    WHERE (Setenummer, Vognnummer) NOT IN (
        SELECT Setenummer, Vognnummer
        FROM OpptatteSeter
    )
)
SELECT * FROM LedigeSeter;
        """,
                       (togrute, vognnummer, startstasjon, sluttstasjon, reisedato, togrute, vognnummer))

        antallTilgjengeligeBilletter = 0
        results = cursor.fetchall()
        for row in results:
            antallTilgjengeligeBilletter += 1
        antallBilletter = interface.input_billetter(
            cursor, stdscr, antallTilgjengeligeBilletter, billettype)
        counter = 0
        billettPrint = ""
        for row in results:
            counter += 1
            setenummer = row[0]
            radnummer = row[1]
            vognnummer = row[2]
            billettPrint += (
                f"Vognnummer: {vognnummer}, Setenummer: {setenummer}, Radnummer: {radnummer}\n")
            if counter == antallBilletter:
                break
        prompt = "Her er " + str(antallBilletter) + \
            " tilgjengelige billetter:\n"
        stdscr.clear()
        stdscr.addstr(0, 0, prompt + billettPrint +
                      "\nTrykk enter for å komme videre til innlogging for å bestille disse billettene")
        stdscr.getch()  # Wait for user to press a key before returning to the menu
        kundenummer = interface.login(conn, stdscr)

        cursor.execute("""
        SELECT Togoppsett
        FROM Togrute
        WHERE TogruteID = ?
        """, (togrute,))
        togoppsett = cursor.fetchone()[0]

        endPromt = ""
        cursor.execute("""
            INSERT INTO Kundeordre (Kundeordrenummer, Kjøpsdato, Kjøpstidspunkt, Kunde, Rute, Reisedato)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (kundeordrenummer, kjopsdato_str, kjopstidspunkt_str, kundenummer, togrute, reisedato))

        for i in range(antallBilletter):
            unique_billettID = False
            max_attempts = 10  # Legg til en begrensning på antall forsøk
            attempts = 0

            while not unique_billettID and attempts < max_attempts:
                cursor.execute("SELECT MAX(BillettID) FROM Billett")
                max_billettID = cursor.fetchone()[0]

                if attempts < max_attempts - 1:
                    billettID = str(int(max_billettID) +
                                    1) if max_billettID else '1'
                else:
                    # Bruk et tilfeldig tall mellom 1 og 99999 som BillettID i siste forsøk
                    billettID = str(random.randint(1, 99999))

                cursor.execute(
                    "SELECT COUNT(*) FROM Billett WHERE BillettID = ?", (billettID,))
                count = cursor.fetchone()[0]
                if count == 0:
                    unique_billettID = True
                attempts += 1  # Øk antall forsøk

            if attempts == max_attempts and not unique_billettID:
                #print("Kunne ikke finne et unikt BillettID etter", max_attempts, "forsøk. Avbryter.")
                break

            cursor.execute("""
                INSERT INTO Billett (BillettID, Påstigning, Avstigning, Ordrenummer, Vogn, Togoppsett)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (billettID, startstasjon, sluttstasjon, kundeordrenummer, vognnummer, togoppsett))

            endPromt += "\nNy billett registrert"

            if billettype == "sete":
                setenummer = results[i][0]
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

        stdscr.addstr(0, 0, endPromt)

        conn.commit()
        stdscr.getch()  # Wait for user to press a key before returning to the menu

    if billettype == "seng":
        cursor.execute("""
        WITH Sengevogner AS (
        SELECT Vognnummer, AvType
        FROM Vogn
        WHERE Togoppsett = (
            SELECT Togoppsett
            FROM Togrute
            WHERE TogruteID = ? AND Vognnummer = ?
        )
        AND AvType IN (
            SELECT Vogntypenavn
            FROM Vogntype
            WHERE Type = 'Sove'
        )
        ),
        OpptatteSenger AS (
            SELECT Sengenummer, Vogntypenavn, Vognnummer
            FROM Sengebillett
            JOIN Billett ON Sengebillett.BillettID = Billett.BillettID
            WHERE Ordrenummer IN (
                SELECT Kundeordrenummer
                FROM Kundeordre
                WHERE Rute = ? AND Reisedato = ? AND Vognnummer = ?
            )
        ),
        LedigeSenger AS (
            SELECT Sengenummer, Sovetypenavn, Kupenummer, Vognnummer
            FROM Seng
            JOIN Sengevogner ON Seng.Sovetypenavn = Sengevogner.AvType
            WHERE (Sengenummer, Vognnummer) NOT IN (
                SELECT Sengenummer, Vognnummer
                FROM OpptatteSenger
            )
        )
        SELECT * FROM LedigeSenger;
        """,
                       (togrute, vognnummer, togrute, reisedato, vognnummer))
        antallTilgjengeligeBilletter = 0
        results = cursor.fetchall()
        for row in results:
            antallTilgjengeligeBilletter += 1
        antallBilletter = interface.input_billetter(
            cursor, stdscr, antallTilgjengeligeBilletter, billettype)
        counter = 0
        billettPrint = ""
        for row in results:
            counter += 1
            sengenummer = row[0]
            kupenummer = row[2]
            vognnummer = row[3]
            billettPrint += (
                f"Vognnummer: {vognnummer}, Sengenummer: {sengenummer}, Kupénummer: {kupenummer}\n")
            if counter == antallBilletter:
                break
        prompt = "Her er " + str(antallBilletter) + \
            " tilgjengelige billetter:\n"
        stdscr.clear()
        stdscr.addstr(0, 0, prompt + billettPrint +
                      "\nTrykk enter for å komme videre til innlogging for å bestille disse billettene")
        stdscr.getch()  # Wait for user to press a key before returning to the menu
        kundenummer = interface.login(conn, stdscr)

        cursor.execute("""
        SELECT Togoppsett
        FROM Togrute
        WHERE TogruteID = ?
        """, (togrute,))
        togoppsett = cursor.fetchone()[0]

        endPromt = ""
        cursor.execute("""
            INSERT INTO Kundeordre (Kundeordrenummer, Kjøpsdato, Kjøpstidspunkt, Kunde, Rute, Reisedato)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (kundeordrenummer, kjopsdato_str, kjopstidspunkt_str, kundenummer, togrute, reisedato))

        for i in range(antallBilletter):
            unique_billettID = False
            max_attempts = 10  # Legg til en begrensning på antall forsøk
            attempts = 0

            while not unique_billettID and attempts < max_attempts:
                cursor.execute("SELECT MAX(BillettID) FROM Billett")
                max_billettID = cursor.fetchone()[0]

                if attempts < max_attempts - 1:
                    billettID = str(int(max_billettID) +
                                    1) if max_billettID else '1'
                else:
                    # Bruk et tilfeldig tall mellom 1 og 99999 som BillettID i siste forsøk
                    billettID = str(random.randint(1, 99999))

                cursor.execute(
                    "SELECT COUNT(*) FROM Billett WHERE BillettID = ?", (billettID,))
                count = cursor.fetchone()[0]
                if count == 0:
                    unique_billettID = True
                attempts += 1  # Øk antall forsøk

            if attempts == max_attempts and not unique_billettID:
                #print("Kunne ikke finne et unikt BillettID etter", max_attempts, "forsøk. Avbryter.")
                break

            cursor.execute("""
                INSERT INTO Billett (BillettID, Påstigning, Avstigning, Ordrenummer, Vogn, Togoppsett)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (billettID, startstasjon, sluttstasjon, kundeordrenummer, vognnummer, togoppsett))

            endPromt += "\nNy billett registrert"

            sengenummer = results[i][0]
            cursor.execute("""
                SELECT Sovetypenavn
                FROM Seng
                WHERE Sengenummer = ?
            """, (sengenummer,))
            vogntypenavn = cursor.fetchone()[0]

            cursor.execute("""
            
                INSERT INTO Sengebillett (BillettID, Sengenummer, Vogntypenavn)
                VALUES (?, ?, ?)
            """, (billettID, sengenummer, vognnummer))
        if antallBilletter % 2 == 1:
            unique_billettID = False
            while not unique_billettID:
                cursor.execute("SELECT MAX(BillettID) FROM Billett")
                max_billettID = cursor.fetchone()[0]
                billettID = str(int(max_billettID) +
                                1) if max_billettID else '1'

                cursor.execute(
                    "SELECT COUNT(*) FROM Billett WHERE BillettID = ?", (billettID,))
                count = cursor.fetchone()[0]
                if count == 0:
                    unique_billettID = True
            try:
                cursor.execute("""
                    INSERT INTO Billett (BillettID, Påstigning, Avstigning, Ordrenummer, Vogn, Togoppsett)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (billettID, startstasjon, sluttstasjon, kundeordrenummer, vognnummer, togoppsett))

                endPromt += "\nNy billett registrert"

                sengenummer += 1
                cursor.execute("""
                
                    INSERT INTO Sengebillett (BillettID, Sengenummer, Vogntypenavn)
                    VALUES (?, ?, ?)
                """, (billettID, sengenummer, vognnummer))
            except Exception as e:
                print(
                    f"Fikk ikke booket hele kupéen for oddetalls billett: {e}")

        stdscr.addstr(0, 0, endPromt)

        conn.commit()
        stdscr.getch()  # Wait for user to press a key before returning to the menu
